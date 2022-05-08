import cv2
import math
import numpy as np
import imutils
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
    cw = width/2
    x1 = cw + cw*math.cos(theta)
    y1 = cw + cw*math.sin(theta)
    x2 = cw - cw*math.cos(theta)
    y2 = cw - cw*math.sin(theta)
    return zip(line(ax,ay,bx,by))

'''
returns the image col corresponding to the point on the projected image line
'''
def image_line_to_col(image_line, c, l, width):
    return c*width/len(image_line)

def projection_line(col, layer, image, theta):
    width, height = image.size
    rad = math.radians(90-mod_theta)
    cw = width/2
    coordinates = []
    cos_value = math.cos(rad)
    sin_value = math.sin(rad)
    if(cos_value!=0):
        # CASE1: x = 0
        x = 0
        length = -c/cos_value
        y = l + length*sin_value
        if(y >= 0 and y < width):
            coordinates.append((x,y))
        # CASE2: x = width -1
        x = width -1
        length = -c/cos_value
        y = l + length*sin_value
        if(y >= 0 and y < width):
            coordinates.append((x,y))
    if(sin_value!=0):
        # CASE3: y = 0
        y = 0
        length = -c/sin_value
        x = c + length*cos_value
        if (x >= 0 and y < width):
            coordinates.append((x,y))
        # CASE4: y = width -1
        y = width- 1
        length = -c/sin_value
        x = c + length*cos_value
        if (x >= 0 and y < width):
            coordinates.append((x,y))
    coordinates = list(set(coordinates))
    if len(coordinates) == 1:
        return [[coordinates[0][0],coordinates[0][1]]]
    if len(coordinates) == 2:
        return zip(line(coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1]))
    return []

def line_intersection(lineA, lineB):
    return (intersection(set(lineA), set(lineB)))

def delta_color(colorA, colorB):
    return pow(pow((colorA[0]-colorB[0]),2) + pow((colorA[1]-colorB[1]),2) + pow((colorA[2]-colorB[2]),2), 0.5)

def voxel_coloring(images, angles):
    image_lines = [image_line(images[i], angles[i]) for i in len(images)]
    num_images = len(images)
    width, height = images[0].size
    voxels = np.zeros([width, height, width],ndim=3)
    for layer in range(width):
        for r in range(height):
            for c in range(width):
                voxel = layer[r][c]
                #project voxel onto the images
                for i in range(num_images):
                    projected = projection_line(c,layer, images[i], angles[i])
                    projected_point = line_intersection(projected, image_lines[0])
                    if len(projected_point) == 1:
                        projected_point[0][0] = projected_point[0][0]*width/len(image_line)
                    colors.append(images[i].getpixel(projected_point[0])
                #evaluate voxel consistency
                
                pass
            # color voxels
            # remember image pixels to mark
        # mark off pixels

def reconstruction_size(image, max_height):
    image = image.resize((width,height/LEGO_VOXEL_SCALE))
    im_width, im_height = image.size
    new_im_height = max_height/LEGO_VOXEL_HEIGHT
    scale = new_im_height/im_height
    new_im_width = im_width*scale
    return new_im_width, new_im_height

def driver(images, angles):
    images = [Image.open(i[0]) for i in images]
    scaled_width, scaled_height = reconstruction_size(images[0])
    images = [i.resize(scaled_width, scaled_height) for i in images]
    #INSERT IMAGE RECOLOR
    return voxel_coloring(images, angles)
