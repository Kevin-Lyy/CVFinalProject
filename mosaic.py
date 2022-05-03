import cv2
import numpy as np
import imutils
from PIL import Image
import matplotlib.pyplot as plt

def convertToPixels(image,size):
    img = Image.open("threshold.jpg")
    pixelated = img.resize(size,Image.BILINEAR)
    sizeUp = pixelated.resize(img.size,Image.NEAREST)
    sizeUp.save("clean.jpg")


convertToPixels(image="threshold.jpg",size=(50,50))

