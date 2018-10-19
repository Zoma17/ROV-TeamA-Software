import cv2
import numpy as np


#Copied from Python Programming.net
def draw_lines(img, lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(img, (coords[0],coords[1]), (coords[2],coords[3]), [255,255,255], 3)
    except:
        pass





im =  cv2.imread("LGR.png", 1);


imred=im;
imblue=im;
imyellow=im;


hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

#blue ranges
lower_blue = np.array([105, 16, 0])
upper_blue= np.array([240, 255, 170])

#red ranges
lower_red = np.array([0, 100, 100])
upper_red = np.array([180, 255, 255])

#yellow ranges
lower_yellow = np.array([20, 90, 100])
upper_yellow= np.array([255, 255, 255])


maskyellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
maskred=mask = cv2.inRange(hsv, lower_red, upper_red)
maskblue=mask = cv2.inRange(hsv, lower_blue, upper_blue)

#try for red
res = cv2.bitwise_and(imred, imred, mask=maskred)
kernel = np.ones((5,5), np.uint8)
closing = cv2.morphologyEx(res, cv2.MORPH_CLOSE, kernel)
opening = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel)
processed_img = cv2.GaussianBlur(opening, (3,3), 0 )
processed_img =cv2.cvtColor(processed_img,cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(processed_img, 30, 200)
cnts,h  = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # if our approximated contour has four points, then
    # we can assume that we have found our screen
    if len(approx) == 3:
        print("Triangle")
        print("Red")
        break
    elif len(approx)==4:
        print("Rectangle")
        print("Red")
        break


#try for blue
res = cv2.bitwise_and(im, im, mask=maskblue)
kernel = np.ones((5,5), np.uint8)
closing = cv2.morphologyEx(res, cv2.MORPH_CLOSE, kernel)
opening = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel)
processed_img = cv2.GaussianBlur(opening, (3,3), 0 )
processed_img =cv2.cvtColor(processed_img,cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(processed_img, 30, 200)
cnts,h  = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # if our approximated contour has four points, then
    # we can assume that we have found our screen
    if len(approx) == 3:
        print("Triangle")
        print("blue")
        break
    elif len(approx)==4:
        print("Rectangle")
        print("blue")
        break

#try for yellow
res = cv2.bitwise_and(im, im, mask=maskyellow)
kernel = np.ones((5,5), np.uint8)
closing = cv2.morphologyEx(res, cv2.MORPH_CLOSE, kernel)
opening = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel)
processed_img = cv2.GaussianBlur(opening, (3,3), 0 )
processed_img =cv2.cvtColor(processed_img,cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(processed_img, 30, 200)
cnts,h  = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # if our approximated contour has four points, then
    # we can assume that we have found our screen
    if len(approx) == 3:
        print("Triangle")
        print("yellow")
        break
    elif len(approx)==4:
        print("Rectangle")
        print("yellow")
        break


