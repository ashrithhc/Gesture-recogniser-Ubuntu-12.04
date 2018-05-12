import numpy as np
import cv2
import sys, Image, ImageDraw
import colorsys

count=0
temp_x = temp_y = 0
arr_string = ""
cap = cv2.VideoCapture(0) #cap is an object that stores the camera properties. Cap is used to retrieve camera options.

while(cap.isOpened()):
	# Capture frame-by-frame
	ret, frame = cap.read() #reads a frame and returns to ret, frame.

	frame = cv2.flip(frame, 1) #flips the image give mirror-image.

	# Our operations on the frame come here
	width = cap.get(3) #Get the width of the frame.
	height = cap.get(4) #Get the height of the frame.
	print width,height
	count=count+1 #Keep count of the no. of frames being analysed.

	hsvformat = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #convert the obtained image to HSV format and store it in "hsvformat"

	img = hsvformat 

#	hsvformat = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#	ret,thresh = cv2.threshold(imgray,127,255,0)
#	image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	img = cv2.GaussianBlur(img, (5, 5), 0) #Blur the image to avoid error at the edges.
	img = cv2.inRange(img, np.array((20, 125, 125)), np.array((30, 255, 255))) #threshhold to range given
	image_clusters = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0] #form list of clusters
#	print cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	for i in image_clusters:
		rect = cv2.boundingRect(np.array(i))
		cv2.rectangle(frame, (rect[0], rect[1]), ((rect[0]+rect[2]), (rect[1]+rect[3])), (230, 0, 80), 1) # (rect[0], rect[1]) gives left-top point of rectangle. where as rect[2] gives width and rect[3] gives the height.
		if
		x = rect[0] + rect[2]/2
		y = rect[1] + rect[3]/2
		if (x-temp_x > y-temp_y) arr_string = arr_string + 'R'

#	for i in image_clusters:
#		for j in range(0, 640):
#			if (img.item(i, j, 2)>=100) and (img.item(i, j, 1)<=50) and (img.item(i, j, 0)<=50):
#				img.itemset((i, j, 2), 0)
#				img.itemset((i, j, 1), 255)
#				img.itemset((i, j, 0), 0)


	# Display the resulting frame
	cv2.imshow('frame name',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		print count
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
