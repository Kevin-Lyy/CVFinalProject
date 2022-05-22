import cv2
image1 = cv2.imread("images/ducc.png")
thresh_val = 40
image1[image1 < thresh_val] = 0


ret,thresh4 = cv2.threshold(image1,127,255,cv2.THRESH_TRUNC)

cv2.imwrite("threshold.jpg", thresh4)

# De-allocate any associated memory usage 
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
