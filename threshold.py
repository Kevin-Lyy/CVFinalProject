import cv2
import numpy
import numpy as np
import imutils
import PIL
from PIL import Image
import matplotlib.pyplot as plt
from PIL import ImageColor
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


Lego_colors = []
def LegoDatabase():
    legos_colors = open('LegoColors.txt','r')
    colors = legos_colors.readlines()
    for color in colors:
        color = "#" + color.strip()
        color = ImageColor.getcolor(color,"RGB")
        Lego_colors.append(color)

def convertToPixels(image,size):
    img = Image.open("threshold.jpg")
    pixelated = img.resize(size,Image.BILINEAR)
    sizeUp = pixelated.resize(img.size,Image.NEAREST)
    sizeUp.save("mosaic.jpg")

def findDeltaE(color):
    color = sRGBColor(color[0],color[1],color[2])
    lab_color_1 = convert_color(color,LabColor)
    delta_e_list = []
    for stdcolor in Lego_colors:
        stdcolor = sRGBColor(stdcolor[0],stdcolor[1],stdcolor[2])
        lab_color_2 = convert_color(stdcolor,LabColor)
        delta_e = delta_e_cie2000(lab_color_1, lab_color_2)
        delta_e_list.append(delta_e)
    min_delta = min(delta_e_list)
    return Lego_colors[delta_e_list.index(min_delta)]


def reColorLego():
    img = PIL.Image.open("mosaic.jpg")
    img = img.convert("RGB")
    colors = img.getdata()
    new_image = []
    for pixel in colors:
        if(pixel[0] > 0 and pixel[1] > 0 and pixel[2] > 0):
            new_image.append(pixel)
        else:
            new_image.append(pixel)

    img.putdata(new_image)
    img.save("reColor.jpg")

            

LegoDatabase()

convertToPixels(image="threshold.jpg",size=(60,50))

reColorLego()



