import numpy as np
import cv2
import sys, Image, ImageDraw
import colorsys
import allproc as one
import math
import kNN

cap = cv2.VideoCapture(0) #cap is an object that stores the camera properties. Cap is used to retrieve camera options.

list_coord = []
xValues = []
yValues = []
count_points = 0
sumX = 0
sumY = 0
sumX2 = 0
sumXY = 0

while(cap.isOpened()):
	# Capture frame-by-frame
	ret, frame = cap.read() #reads a frame and returns to ret, frame.
	frame = one.flip_frame(cap, frame)
	image_clusters = one.find_clusters(frame, (20, 140, 140), (30, 255, 255))
	one.form_rectangles(image_clusters, frame)

	one.display_boundary(frame)
	coord = one.find_largest(image_clusters, frame)

	count_points, sumX, sumY, sumX2, sumXY, flag = one.line_distinguish(coord, count_points, sumX, sumY, sumX2, sumXY)
	if(flag):
		list_coord.append(coord)
		xValues.append(coord[0])
		yValues.append(coord[1])

	# Display the resulting frame
	cv2.imshow('frame name',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		# slope = one.find_the_line(count_points, sumX, sumY, sumX2, sumXY)
		# one.kNN_Classifier(slope)
		one.kNN_integration(xValues, yValues)
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
