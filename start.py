import numpy as np
import cv2
import sys, Image, ImageDraw
import colorsys
import div1 as one

count=0
cap = cv2.VideoCapture(0) #cap is an object that stores the camera properties. Cap is used to retrieve camera options.

while(cap.isOpened()):
	# Capture frame-by-frame
	ret, frame = cap.read() #reads a frame and returns to ret, frame.

	frame = one.flip_frame(cap, frame)

	count=count+1 #Keep count of the no. of frames being analysed.

	image_clusters = one.find_clusters(frame)

	one.form_rectangles(image_clusters, frame)

	one.display_grids(frame)

	coord = one.find_largest(image_clusters, frame)

	one.track_coordinates(coord)

	# Display the resulting frame
	cv2.imshow('frame name',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		print count
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
