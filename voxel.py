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
    return list(zip(*line(x1,y1,x2,y2)))

'''
returns the image col corresponding to the point on the projected image line
'''
def image_line_to_col(image_line, c, l, width):
    return c*width/len(image_line)

def projection_line(col, layer, image, theta):
    width, height = image.size
    rad = math.radians(90-theta)
    cw = width/2
    coordinates = []
    cos_value = math.cos(rad)
    sin_value = math.sin(rad)
    if(cos_value!=0):
        # CASE1: x = 0
        x = 0
        length = -col/cos_value
        y = int(layer + length*sin_value)
        if(y >= 0 and y < width):
            coordinates.append((x,y))
        # CASE2: x = width -1
        x = width -1
        length = -col/cos_value
        y = int(layer + length*sin_value)
        if(y >= 0 and y < width):
            coordinates.append((x,y))
    if(sin_value!=0):
        # CASE3: y = 0
        y = 0
        length = -col/sin_value
        x = int(col + length*cos_value)
        if (x >= 0 and y < width):
            coordinates.append((x,y))
        # CASE4: y = width -1
        y = width- 1
        length = -col/sin_value
        x = int(col + length*cos_value)
        if (x >= 0 and y < width):
            coordinates.append((x,y))
    coordinates = list(set(coordinates))
    if len(coordinates) == 1:
        return [[coordinates[0][0],coordinates[0][1]]]
    if len(coordinates) == 2:
        return zip(*line(coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1]))
    return []

def line_intersection(lineA, lineB):
    return list(set(lineA).intersection(set(lineB)))

def delta_color(colorA, colorB):
    return pow(pow((colorA[0]-colorB[0]),2) + pow((colorA[1]-colorB[1]),2) + pow((colorA[2]-colorB[2]),2), 0.5)

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

def voxel_coloring(images, angles, threshold=20):
    image_lines = [image_line(images[i], angles[i]) for i in range(len(images))]
    num_images = len(images)
    width, height = images[0].size
    voxels = np.zeros([width, height, width, 3])
    for layer in range(width):
        print(layer, end=" ")
        for r in range(height):
            for c in range(width):
                colors = []
                coords = []
                #project voxel onto the images
                for i in range(num_images):
                    projected = projection_line(c,layer, images[i], angles[i])
                    projected_point = line_intersection(projected, image_lines[i])
                    if len(projected_point) == 1:
                        adjusted_point = [int(projected_point[0][0]*((width-1)/len(image_lines[i]))), r]
                        colors.append(images[i].getpixel(tuple(adjusted_point)))
                        coords.append(adjusted_point)
                #if consistent color then color voxel and remove from images
                if len(coords) == num_images and len(colors) > 0 and consistent(colors, threshold):
                    voxels[layer][r][c] = average_color(colors)
                    for i in range(num_images):
                        images[i].putpixel(coords[i], (0,0,0))
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
    scaled_width, scaled_height = reconstruction_size(images[0], 1000)
    images = [i.resize((scaled_width, scaled_height), Image.Resampling.BILINEAR) for i in images]
    #INSERT IMAGE RECOLOR
    voxels = voxel_coloring(images, angles)
    np.save("voxels_1000", voxels)

driver(["36_r0.png", "36_r60.png", "36_r120.png", "36_r180.png", "36_r240.png", "36_r300.png"], [0,60,120,180,240,300])
