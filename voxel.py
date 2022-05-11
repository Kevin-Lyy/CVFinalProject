import cv2
import math
import numpy as np
import imutils
from skimage.draw import line
from PIL import Image
import matplotlib.pyplot as plt

LEGO_VOXEL_WIDTH = 7.8
LEGO_VOXEL_HEIGHT = 9.6
LEGO_VOXEL_SCALE = LEGO_VOXEL_HEIGHT/LEGO_VOXEL_WIDTH

'''
calculates the line that goes through the center of the voxel box
of length width of the image oriented at angle theta
in the column, layer parameter space
returns all the points on the line
'''
def image_line(image, theta):
    width, height = image.size
    rad = math.radians(theta)
    cw = width/2
    x1 = int(cw + cw*math.cos(rad))
    y1 = int(cw + cw*math.sin(rad))
    x2 = int(cw - cw*math.cos(rad))
    y2 = int(cw - cw*math.sin(rad))
    print("Image line for ", theta, ": ",x1,y1,x2,y2)
    return ((x1,y1),(x2,y2))
    #return list(zip(*line(x1,y1,x2,y2)))

'''
returns the image col corresponding to the point on the projected image line
'''
def image_line_to_col(image_line, c, l, width):
    return c*width/len(image_line)

def projection_line(col, layer, image, theta):
    width, height = image.size
    rad = math.radians(theta)
    coordinates = []
    cos_value = math.cos(rad)
    sin_value = math.sin(rad)
    if(sin_value!=0):
        # CASE1: x = 0
        x = 0
        y = int(-cos_value*(x-col)/sin_value + layer)
        if(y >= 0 and y < width):
            coordinates.append((x,y))
        # CASE2: x = width -1
        x = width -1
        y = int(-cos_value*(x-col)/sin_value + layer)
        if(y >= 0 and y < width):
            coordinates.append((x,y))
    if(cos_value!=0):
        # CASE3: y = 0
        y = 0
        x = int(-(y-layer)*sin_value/cos_value + col)
        if (x >= 0 and x < width):
            coordinates.append((x,y))
        # CASE4: y = width -1
        y = width- 1
        x = int(-(y-layer)*sin_value/cos_value + col)
        if (x >= 0 and x < width):
            coordinates.append((x,y))
    coordinates = list(set(coordinates))
    print("Projection Line for ", col, " ", layer, ": ", coordinates)
    if len(coordinates) == 1:
        return coordinates+coordinates
    if len(coordinates) == 2:
        return coordinates
        #return zip(*line(coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1]))
    return []

#def line_intersection(lineA, lineB):
#    return list(set(lineA).intersection(set(lineB)))

def line_intersection(lineA, lineB, width):
    print(lineA, lineB)
    x1 = lineA[0][0]
    y1 = lineA[0][1]
    x2 = lineA[1][0]
    y2 = lineA[1][1]
    x3 = lineB[0][0]
    y3 = lineB[0][1]
    x4 = lineB[1][0]
    y4 = lineB[1][1]
    det = ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) )
    if det == 0: return []
    px= ( (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4) ) / det
    py= ( (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4) ) / det
    #if px > 0 and px < width and py > 0 and py < width:
    return (int(px),int(py))
    #return []

def delta_color(colorA, colorB):
    R = pow(pow((colorA[0]-colorB[0]),2),0.5)
    G = pow(pow((colorA[1]-colorB[1]),2),0.5)
    B = pow(pow((colorA[2]-colorB[2]),2),0.5)
    return (R+G+B)/3

def consistent(colors, threshold):
    for i in range(len(colors)):
        for j in range(i+1, len(colors)):
            if delta_color(colors[i], colors[j]) > threshold:
                return False
    return True

def average_color(colors):
    color = [0,0,0]
    for i in range(len(colors)):
        color[0] += colors[i][0]
        color[1] += colors[i][1]
        color[2] += colors[i][2]
    color[0] = int(color[0]/len(colors))
    color[1] = int(color[1]/len(colors))
    color[2] = int(color[2]/len(colors))
    return color

def rect_points(coordA, coordB):
    points = [[coordA[0], i] for i in range(coordB[1],coordA[1])]
    points += [[i, coordA[1]] for i in range(coordA[0],coordB[0])]
    points += [[coordB[0], i] for i in range(coordA[1],coordB[1],-1)]
    points += [[i, coordB[1]] for i in range(coordB[0],coordA[0],-1)]
    return points

def background_threshold(color, t):
    return color[0] < t and color[1] < t and color[2] < t

def voxel_coloring(images, angles, threshold=20):
    image_lines = [image_line(images[i], angles[i]) for i in range(len(images))]
    num_images = len(images)
    width, height = images[0].size
    #voxels = []
    #voxels = np.zeros([width, height, width, 3])
    voxels = np.full([width, height, width, 3], 255)
    cw = int((width-1)/2)
    coordA = [0, width-1] #xz coordinates
    coordB = [width-1, 0] #xz coordinates

    #loop through rect layers
    while(coordB[0]-coordA[0] > 1):
        # through voxels in each layer
        for row in range(height):
        #for row in range(32,33):
            for p in rect_points(coordA, coordB):
                vp = (p[0], row, p[1]) #(x,y,z) or (col,row,layer)
                coords = [] # store coordinates of point projected on images
                colors = [] # store colors of point projected on images
                image_indexes = [] # store index of relevant images
                for i in range(num_images):
                    projected = projection_line(p[0],p[1], images[i], angles[i])
                    projected_point = []
                    if projected != []:
                        projected_point = line_intersection(projected, image_lines[i], width)
                    print("Projected Point: ", projected_point)
                    if len(projected_point) == 2:
                        ac = int(math.dist(projected_point, image_lines[i][1]))
                        if ac < width:
                            adjusted_point = [ac, row]
                            print("Adjusted Point: ", adjusted_point)
                            image_indexes.append(i)
                            colors.append(images[i].getpixel(tuple(adjusted_point)))
                            coords.append(adjusted_point)
                    else:
                        image_indexes.append(i)
                        colors.append([0,0,0])
                for i in range(len(colors)):
                    if background_threshold(colors[i],40):
                        colors[i] = [0,0,0]
                print(colors)
                if len(colors) == 0 or [0,0,0] in colors:
                    voxels[p[1]][row][p[0]] = [0,0,0]
                elif (len(colors) > 0 and consistent(colors, threshold)) or len(colors) == 1:
                    color = average_color(colors)
                    #if color != [0,0,0]:
                    voxels[p[1]][row][p[0]] = color
                        #voxels.append([p[0], row, p[1], color[0], color[1], color[2]])
                    #for i in range(len(colors)):
                    #    if i in image_indexes:
                    #        images[i].putpixel(coords[i], (0,0,0))
                #if color != [0,0,0]: print(colors, end=" ")
        #set next layer coords
        coordA = [coordA[0]+1, coordA[1]-1]
        coordB = [coordB[0]-1, coordB[1]+1]
    #return np.array(voxels)
    return voxels

def reconstruction_size(image, max_height):
    im_width, im_height = image.size
    image = image.resize((im_width,int(im_height//LEGO_VOXEL_SCALE)), Image.Resampling.BILINEAR)
    new_im_height = int(max_height//LEGO_VOXEL_HEIGHT)
    scale = new_im_height/im_height
    new_im_width = int(im_width*scale)
    return new_im_width, new_im_height

def driver(images, angles):
    images = [Image.open(i) for i in images]
    scaled_width, scaled_height = reconstruction_size(images[0], 500)
    images = [i.resize((scaled_width, scaled_height), Image.Resampling.BILINEAR) for i in images]
    #INSERT IMAGE RECOLOR
    voxels = voxel_coloring(images, angles)
    points = []
    for layer in range(len(voxels)):
        for row in range(len(voxels[layer])):
            for col in range(len(voxels[layer][row])):
                color = voxels[layer][row][col]
                R = color[0]/255
                G = color[1]/255
                B = color[2]/255
                points.append([col, row, layer, R,G,B])
    points = np.array(points)
    np.save("voxels_500", voxels)
    np.save("points_500", points)

driver(["36_r0.png", "36_r60.png", "36_r120.png", "36_r180.png", "36_r240.png", "36_r300.png"], [0,60,120,180,240,300])
#driver(["36_r330.png", "36_r0.png", "36_r30.png"],[330,0,30])
#driver(["36_r330.png"],[330])
#driver(["36_r30.png"],[30])
#driver(["36_r0.png"],[0])

#driver(["36_r60.png"],[60])
#driver(["36_r120.png"],[120])
#driver(["36_r180.png"],[180])
#driver(["36_r240.png"],[240])
#driver(["36_r300.png"],[300])

#driver(["36_r0.png", "36_r30.png", "36_r60.png"],[0,30,60])
