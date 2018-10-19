import numpy as np
import cv2




def receive():
    cap = cv2.VideoCapture('udpsrc port=10000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
 
    while True:

        ret,frame = cap.read()
        cap_send = cap;
        if not ret:
            print('empty frame')
            continue 
            
        out_send = cv2.VideoWriter('appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=127.0.0.1 port=7000',cv2.CAP_GSTREAMER,0, 20, (320,240), True)
        out_send.write(frame)
        cv2.imshow('receive', frame)
        if cv2.waitKey(1)&0xFF == ord('q'):
            break


   


receive();



   