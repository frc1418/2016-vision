import sys
#sys.path.append('/Users/riceb/Library/Python/3.5/lib/python/site-packages')
import numpy as np
import cv2
import math

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

#no pictures for 34-54, 10
img = cv2.imread('RealFullField/79.jpg')
cv2.imshow('image', img)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

h, s, v = cv2.split(hsv)
a, b = 2, 1
h = threshold_range(h, 63, 105)
s = threshold_range(s, 7, 255)
v = threshold_range(v, 67, 242)
#cv2.imshow('s', s)
combined = cv2.bitwise_and(h, cv2.bitwise_and(s,v))
#img2 = combined.copy()
contours, v = cv2.findContours(combined, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print ('but wait there is more',  len(contours))

ncontours = []
for contour in contours:
    if(cv2.contourArea(contour) > 100):
        print(cv2.contourArea(contour))
        ncontours.append(contour)

#print ncontours

cv2.drawContours(img, contours, -1, (0,0,255), 1)

ucontours = []

for contour in ncontours:
    rect =  cv2.boundingRect(contour)
    #print rect
    pt1 = (rect[0], rect[1])
    pt2 = (rect[0]+rect[2], rect[1]+rect[3])

    rect = cv2.minAreaRect(contour)
    #print 'recty ', rect
    box = cv2.cv.BoxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img,[box],0,(0, 255, 0),1)

    perim = cv2.arcLength(contour, True)
    print 'prim 1- ', perim

    box = cv2.cv.BoxPoints(rect)
    temp1 = box[0]
    temp2 = box[1]
    temp3 = box[3]
    print "temp 1 - ", temp1
    print "temp 2 - ", temp2
    print "temp 3 - ", temp3
    rectL = math.sqrt(((temp2[1]-temp1[1])**2)+((temp2[0]-temp1[0])**2))
    rectW = math.sqrt(((temp3[1]-temp1[1])**2)+((temp3[0]-temp1[0])**2))
    print 'width - ', rectW
    rectP = rectL*2+rectW*2
    perim -= 2*rectW
    print 'prim 2 - ', perim
    print 'prim 3 - ', abs(perim - 4*rectL)
    print 'prim 4 - ', cv2.contourArea(contour)
    print 'rectA - ', rectL*rectW
    rectA = rectL*rectW
    print 'rectL - ', rectL
    print 'rectP - ', rectP

    if(abs(cv2.contourArea(contour)/rectA - .3) < .05):
        ucontours.append(contour)

print 'ucontours - ', len(ucontours)
cv2.drawContours(img, ucontours, -1, (200,0,255), 3)

cv2.imshow('image', img)
cv2.waitKey(0)
