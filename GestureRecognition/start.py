import numpy as np
import cv2
import sys, Image, ImageDraw
import colorsys
import div1 as one

count=0
cap = cv2.VideoCapture(0) #cap is an object that stores the camera properties. Cap is used to retrieve camera options.

tracker = "z"
back_tracker = "z"

while(cap.isOpened()):
	# Capture frame-by-frame
	ret, frame = cap.read() #reads a frame and returns to ret, frame.

	frame = one.flip_frame(cap, frame)

	count=count+1 #Keep count of the no. of frames being analysed.

	image_clusters = one.find_clusters(frame)

	one.form_rectangles(image_clusters, frame)

	one.display_grids(frame)
	# one.display_track(frame)

	coord = one.find_largest(image_clusters, frame)

	grid_num = one.track_coordinates(coord)
	# print grid_num

	get_back_num = one.get_it_back(coord)
	# print get_back_num

	# Form a string by eliminating repeated grid_num or grid_back_num
	tracker = one.form_string(tracker, grid_num)
	back_tracker = one.form_string(back_tracker, get_back_num)

	tracker = one.check_tracker(tracker)
	back_tracker = one.check_back_tracker(back_tracker)

	print back_tracker

	# Display the resulting frame
	cv2.imshow('frame name',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		print tracker
		print count
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
