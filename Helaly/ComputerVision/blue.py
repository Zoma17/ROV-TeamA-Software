import cv2
import numpy as np

im =  cv2.imread("g7c.png", 1);
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
lower_blue = np.array([105, 16, 0])
upper_blue = np.array([240, 255, 170])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
res = cv2.bitwise_and(im, im, mask=mask)
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
        break
    elif len(approx)==4:
        print("Rectangle")
        break

cv2.drawContours(im, cnts, -1, (0, 255, 0), 3)







cv2.imshow("image2",im) ;
cv2.waitKey()
cv2.destroyAllWindows();

