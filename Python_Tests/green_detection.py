from PIL import Image
import numpy as np
import cv2

def transfrom_image(img, height, width, treshold):
	counter = 0
	mean_height = 0
	output = img.copy()
	for row in range(height):
	    for col in range(width):
	    	r, g, b = img[col, row]
	    	if (g > r + treshold) and (g > b + treshold):
	    		output[col, row] = 255,255,255
	    	else:
	    		output[col, row] = 0,0,0
	    		mean_height += row
	    		counter +=  1
	mean_height = mean_height / max(counter,1)
	return output, mean_height

cam = cv2.VideoCapture(1)
if cam.read()[0]==False:
	cam = cv2.VideoCapture(0)
h = cam.get(3)
w = cam.get(4)
width = int(w)
height = int(h)
resize_val = 5
img = cam.read()[1] 
img = cv2.flip(img, 1)
mean_height = 0

while True:
    if not cam.isOpened():
        print('Unable to load camera.')
        pass

    img = cam.read()[1] 
    img = cv2.flip(img, 1)
    
    frame = cam.read()[1]
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    new_h=int(height/resize_val)
    new_w=int(width/resize_val)
    out = cv2.resize(frame, (new_h, new_w))
    out, mean_height = transfrom_image(out, new_h, new_w, 25)
    out = cv2.resize(out, (height, width))
    print(mean_height);
    cv2.imshow('Detected',cv2.flip(out, 1))

cam.release()
cv2.destroyAllWindows()
