from PIL import Image
import numpy as np
import time
import cv2
import threading
from multiprocessing import Process

resize_val = 200

def build_squares(img):
	x, y, w, h = 200, 200, 10, 10
	d = 10
	imgCrop = None
	crop = None
	for i in range(5):
		for j in range(5):
			if np.any(imgCrop == None):
				imgCrop = img[y:y+h, x:x+w]
			else:
				imgCrop = np.hstack((imgCrop, img[y:y+h, x:x+w]))
			#print(imgCrop.shape)
			cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 1)
			x+=w+d
		if np.any(crop == None):
			crop = imgCrop
		else:
			crop = np.vstack((crop, imgCrop)) 
		imgCrop = None
		x = 200
		y+=h+d
	return crop


def mul_thread_action(img, output, col, row, tresholds):
	acc_b, acc_g, acc_r, t_b, t_g, t_r = tresholds
	r, g, b = img[col, row]
	if abs(r-int(acc_r)) > t_r/6 or abs(g-int(acc_g)) > t_g/6 or abs(b-int(acc_b)) > t_b/6:
	#if 100*g<r*60 or 100*g>r*90 or 100*b<r*50 or 100*b>r*90:
		output[col, row] = 0,0,0
	else:
		output[col, row] = 255,255,255

def transfrom_image(img, height, width, tresholds):
	
	#Tresholds format: acc_b, acc_g, acc_r
	counter = 0
	mean_height = 0
	threads = []
	output = img.copy()
	for row in range(height):
	    for col in range(width):
	    	#mul_thread_action(img, output, col, row, tresholds)
	    	acc_b, acc_g, acc_r, t_b, t_g, t_r = tresholds
	    	r, g, b = img[col, row]
	    	if abs(r-int(acc_r)) > t_r/6 or abs(g-int(acc_g)) > t_g/6 or abs(b-int(acc_b)) > t_b/6:
	    	#if 100*g<r*60 or 100*g>r*90 or 100*b<r*50 or 100*b>r*90:
	    		output[col, row] = 0,0,0
	    	else:
	    		output[col, row] = 255,255,255
	    		mean_height = mean_height + row
	    		counter = counter + 1
	    	#print(row*width+col)
	    	#t = Process(target=mul_thread_action, args=(img, output, col, row, tresholds,))
	    	#threads.append(t)
	    	#t.start()
	    	#while (len(threads)>200 and len(threads)!=0):
	    	#	print("JOINING")
	    	#	for a in threads:
	    	#		a.join()
	mean_height = mean_height / max(counter,1)
	return output, mean_height

def get_means(img, x, y, h, w):

	acc_r = 0
	acc_g = 0
	acc_b = 0

	min_r = 255
	max_r = 0

	min_g = 255
	max_g = 0

	min_b = 255
	max_b = 0

	for i in range(h):
		for j in range(w):
			r = img[y+i, x+j][0]
			g = img[y+i, x+j][1]
			b = img[y+i, x+j][2]

			acc_r = acc_r + r
			acc_b = acc_b + b
			acc_g = acc_g + g

			if r>max_r:
				max_r = r
			if r<min_r:
				min_r = r

			if g>max_g:
				max_g = g
			if g<min_g:
				min_g = g

			if b>max_b:
				max_b = b
			if b<min_b:
				min_b = b

	c = (h*w)
	acc_r = acc_r / c
	acc_g = acc_g / c
	acc_b = acc_b / c

	return acc_b, acc_g, acc_r, max_b-min_b, max_g-min_g, max_r-min_r

cam = cv2.VideoCapture(1)
if cam.read()[0]==False:
	cam = cv2.VideoCapture(0)
anterior = 0
h = cam.get(3)
w = cam.get(4)
width = int(w)
height = int(h)
flagPressedC = False
imgCrop = None
resize_val = 5
img = cam.read()[1] 
img = cv2.flip(img, 1)
a = get_means(img, 200, 200, 90, 90)
mean_height = 0

while True:
    if not cam.isOpened():
        print('Unable to load camera.')
        pass

    img = cam.read()[1] 
    img = cv2.flip(img, 1)

    #if not flagPressedS:
    	#imgCrop = build_squares(img)
    keypress = cv2.waitKey(1)
    if keypress == ord('c'):
    	print("Mask updated")
    	flagPressedC = True
    	a = get_means(img, 200, 200, 90, 90)
    if keypress == ord('s'):
    	flagPressedC = False
    
    frame = cam.read()[1]
    cv2.rectangle(img, (200,200), (200+90, 200+90), (0,255,0), 2)
    cv2.imshow("Set hand histogram", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if flagPressedC:
    	new_h=int(height/resize_val)
    	new_w=int(width/resize_val)
    	out = cv2.resize(frame, (new_h, new_w))
    	out, mean_height = transfrom_image(out, new_h, new_w, a)
    	out = cv2.resize(out, (height, width))
    	print(mean_height);
    	cv2.imshow('Detected',cv2.flip(out, 1))

cam.release()
cv2.destroyAllWindows()
