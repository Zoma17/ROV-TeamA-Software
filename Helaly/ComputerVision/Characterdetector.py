import numpy as np 
import cv2
import pytesseract

cap = cv2.VideoCapture(0)
 
while(True):
    ret, frame = cap.read()
    frame3=frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    roi = frame [0:200,0:200]
    cv2.rectangle(frame3, (0,0), (200, 200), (255,0,0), 2)
    #retval, frame = cv2.threshold(frame, 140, 255, cv2.THRESH_BINARY)
    retval, roi = cv2.threshold(roi, 140, 255, cv2.THRESH_BINARY)
    

    if cv2.waitKey(1) & 0xFF == ord('e'):
       
        text = pytesseract.image_to_string(roi)
        print(text)
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
    
 
    
    cv2.imshow('frame2',frame3)
    cv2.imshow('frame',roi)
    

cap.release()
cv2.destroyAllWindows()