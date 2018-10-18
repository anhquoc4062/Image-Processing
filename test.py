import sys
import cv2 as cv
import numpy as np

img = cv.imread('images/pic1.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
height, width, depth = img.shape
newX,newY = img.shape[1]/2, img.shape[0]/2
newimg = cv.resize(img,(int(newX),int(newY)))
cv.imshow("Show by CV2",newimg)
cv.waitKey(0)
cv.imwrite("resizeimg.jpg",newimg)