import cv2
from PIL import Image
import pytesseract
import argparse
import numpy as np



im = cv2.imread("UH8.jpg", 1);
im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
# th3 = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
# kernel = np.ones((1, 1), np.uint8)
# erosion = cv2.dilate(th3,kernel,iterations = 1)
#
# opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)
# closing = cv2.morphologyEx(erosion, cv2.MORPH_CLOSE, kernel)
text = pytesseract.image_to_string(im)
print (text) ;
cv2.imshow("image",im) ;
cv2.waitKey()
cv2.destroyAllWindows();


