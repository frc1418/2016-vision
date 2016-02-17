import sys
#sys.path.append('/Users/riceb/Library/Python/3.5/lib/python/site-packages')
import numpy as np
import cv2

'''
This program will take an image,
look for a color on that image
filter everything that is not that color
return a binary mask of the shapes that color creates
'''
def threshold_range(im, lo, hi):
    unused, t1 = cv2.threshold(im, lo, 255, type=cv2.THRESH_BINARY)
    unused, t2 = cv2.threshold(im, hi, 255, type=cv2.THRESH_BINARY_INV)
    return cv2.bitwise_and(t1, t2)

img = cv2.imread('RealFullField/90.jpg')
cv2.imshow('image', img)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

h, s, v = cv2.split(hsv)
a, b = 2, 1
h = threshold_range(h, 49, 180)
s = threshold_range(s, 0, 218)
#cv2.imshow('s', s)
v = threshold_range(v, 76, 238)
combined = cv2.bitwise_and(h, cv2.bitwise_and(s,v))
#img2 = combined.copy()
contours, v = cv2.findContours(combined, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print ('but wait there is more',  len(contours))
ncontours = []
for contour in contours:
    if(cv2.contourArea(contour) > 300):
        print(cv2.contourArea(contour))
        ncontours.append(contour)

cv2.drawContours(img, ncontours, -1, (0,0,255), 2)
cv2.imshow('image', img)
cv2.waitKey(0)
