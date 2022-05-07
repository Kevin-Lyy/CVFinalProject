import cv2
import numpy as np
import imutils
import PIL
from PIL import Image
import matplotlib.pyplot as plt
from PIL import ImageColor

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

def delta_color(pixel):
    red = []
    green = []
    blue = []
    RGB = []
    for std_lego_color in Lego_colors:
        #if pixel[0] < std_lego_color[0] + 5 and pixel[0]  > std_lego_color[0] - 5 and pixel[1] < std_lego_color[1] + 5 and pixel[1]  > std_lego_color[1] - 5 and pixel[2] < std_lego_color[2] + 5 and pixel[2]  > std_lego_color[2] - 5:
        Rcolor = abs(pixel[0] - std_lego_color[0])
        red.append(Rcolor)
        Gcolor = abs(pixel[1] - std_lego_color[1])
        green.append(Gcolor)
        Bcolor = abs(pixel[2] - std_lego_color[2])
        blue.append(Bcolor)
        RGB.append(Rcolor+Gcolor+Bcolor)
    closest = min(RGB)
    return (red[closest],green[closest],blue[closest])


def reColorLego():
    img = Image.open("mosaic.jpg")
    img = img.convert("RGB")
    colors = img.getdata()
    new_image = []
    for pixel in colors:
        closest_color = delta_color(pixel)
        new_image.append(closest_color)

            
            
    img.putdata(new_image)
    img.save("reColor.jpg")

            

            



LegoDatabase()

convertToPixels(image="threshold.jpg",size=(70,70))

reColorLego()



