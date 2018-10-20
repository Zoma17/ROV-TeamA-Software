import socket
import numpy as np 
import cv2
import pytesseract

#================== Socket =================================
host = '192.168.43.190'
port = 8000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
        s.bind((host, port))
        print('Waiting for QT Connection!')
except socket.error as m:
         print ('Bind failed. Error Code : ' + str(m[0]))
s.listen(5)
conn , addr = s.accept()
print ('Connected ya ray2')
#===========================================================

cap = cv2.VideoCapture(0)
msg = conn.recv(1024).decode()
if (msg) == 'e':
    flag= True
if not msg:
                conn.close()
                break
       

while flag :
   
    
       
    ret, frame = cap.read()
    frame3=frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    roi = frame [0:200,0:200]
    cv2.rectangle(frame3, (0,0), (200, 200), (255,0,0), 2)
    #retval, frame = cv2.threshold(frame, 140, 255, cv2.THRESH_BINARY)
    retval, roi = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
    #roi = cv2.Canny(roi, 30, 200)
          
            

    if cv2.waitKey(1) & 0xFF == ord('e'):
        text = pytesseract.image_to_string(roi)
         print(text)
            
 
    cv2.imshow('frame2',frame3)
    cv2.imshow('frame',roi)

        
    

cap.release()
cv2.destroyAllWindows()
        