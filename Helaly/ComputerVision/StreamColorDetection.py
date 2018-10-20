import numpy as np 
import cv2



#Copied from Python Programming.net
def draw_lines(img, lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(img, (coords[0],coords[1]), (coords[2],coords[3]), [255,255,255], 3)
    except:
        pass


cap = cv2.VideoCapture(0)


while(True):
    ret, frame = cap.read()
    cv2.rectangle(frame, (300,300), (700, 700), (255,0,0), 2)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([180, 255, 255])
    maskred=mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame, frame, mask=maskred)
    kernel = np.ones((5,5), np.uint8)
    closing = cv2.morphologyEx(res, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel)
    processed_img = cv2.GaussianBlur(opening, (3,3), 0 )
    roi = processed_img [300:700,300:700]
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
    cv2.drawContours(frame, cnts, -1, (0, 255, 0), 3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    cv2.imshow('frame',frame)
    cv2.imshow('frame2',roi)
    

cap.release()
cv2.destroyAllWindows()