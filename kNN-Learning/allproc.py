import numpy as np
import cv2
import sys, Image, ImageDraw
import colorsys
import os
import math
import time
import easygui
import kNN

def flip_frame(cap, Img):
	Img = cv2.flip(Img, 1)
	width = cap.get(3) #Get the width of the frame.
	height = cap.get(4) #Get the height of the frame.
	return Img

def find_clusters(Img, col_st, col_end):
	Img = cv2.cvtColor(Img,cv2.COLOR_BGR2HSV) #convert the obtained image to HSV format and store it in "hsvformat"
	Img = cv2.GaussianBlur(Img, (5, 5), 0) #Blur the image to avoid error at the edges.
	Img = cv2.inRange(Img, np.array(col_st), np.array(col_end)) #threshhold to range given
	image_clusters = cv2.findContours(Img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0] #form list of clusters
	return image_clusters

def form_rectangles(image_clusters, Img):
	for i in image_clusters:
		rect = cv2.boundingRect(np.array(i)) #returns the diagnol coordinates of the rectange formed over set of points.
		cv2.rectangle(Img, (rect[0], rect[1]), ((rect[0]+rect[2]), (rect[1]+rect[3])), (230, 0, 80), 1) # (rect[0], rect[1]) = (x, y) of left-top coordinate of rectangle.

def display_boundary(Img):
	cv2.line(Img, (30, 30), (610, 30), (255, 0, 0), 1) #horizontal line 1
	cv2.line(Img, (30, 450), (610, 450), (255, 0, 0), 1) #horizontal line 2
	cv2.line(Img, (30, 30), (30, 450), (255, 0, 0), 1) #vertical line 1
	cv2.line(Img, (610, 30), (610, 450), (255, 0, 0), 1) #vertical line 2

def find_largest(image_clusters, Img):
	# num_x, num_y, den = 0
	num_x = 0
	num_y = 0
	den = 1
	for i in image_clusters:
		rect = cv2.boundingRect(np.array(i)) #Get all the rectangular points
		num_x = num_x + rect[2]*rect[3]*(rect[0] + rect[2]/2) #Sigma x multiplied by the rectangular area
		num_y = num_y + rect[2]*rect[3]*(rect[1] + rect[3]/2) #Sigma y multiplied by the rectangular area
		den = den + rect[2]*rect[3] #Sigma the rectangular areas.
	draw_circle(5, num_x/den, num_y/den, Img)
	coord = (num_x/den, num_y/den)
	return coord

def draw_circle(rad, x, y, Img):
	cv2.circle(Img, (x, y), rad, (0, 0, 255), 5)
	# print Img[y][x]

def line_distinguish(coord, count_points, sumX, sumY, sumX2, sumXY):
	flag = 0
	if (coord[0] > 30 and coord[1] > 30) and (coord[0] < 610 and coord[1] < 450):
		count_points = count_points + 1
		sumX = sumX + coord[0]
		sumY = sumY + coord[1]
		sumX2 = sumX2 + coord[0]*coord[0]
		sumXY = sumXY + coord[0]*coord[1]
		flag = 1
		# print coord
	return count_points, sumX, sumY, sumX2, sumXY, flag

def find_the_line(count_points, sumX, sumY, sumX2, sumXY): # http://faculty.cs.niu.edu/~hutchins/csci230/best-fit.htm
	if count_points == 0:
		return
	XMean = sumX/count_points
	YMean = sumY/count_points
	slope = float(sumXY - (sumX*YMean)) / float(sumX2 - (sumX*XMean))
	slope = math.atan(slope)
	slope = slope * 180/3.14
	# print XMean, YMean, sumXY, sumX, sumX2
	# print "The slope is", slope
	return slope

def kNN_Classifier(slope):
	group, labels = kNN.createDataset()
	distances = []
	for i in range(len(group)):
		if group[i] > slope:
			point_dist = group[i] - slope
		else:
			point_dist = slope - group[i]
		distances.append((point_dist, labels[i]))

	distances.sort()
	one = 0
	two = 0
	for i in range(3):
		if distances[i][1] == 'one':
			one = one + 1
		else:
			two = two + 1
	if one > two:
		print "Line 1"
	else:
		print "Line 2"

def findAngle(x1,y1,x2,y2):
    m1=y1/x1
    m2=y2/x2
    com1=m1-m2
    com2=m1*m2

    tanteta=com1/(1+com2)
    angle= math.degrees(math.atan(tanteta))
    return angle

def findDirection(xValues, yValues):
	clock = 0
	anticlock = 0
	for i in range(len(xValues)-1):
		ang = findAngle(xValues[i], yValues[i], xValues[i+1], yValues[i+1])
		if ang > 0:
			clock = clock + 1
		else :
			anticlock = anticlock + 1
	if clock > anticlock:
		return 1
	return -1

def kNN_integration(xValues, yValues):
	coefficients = np.polyfit(xValues, yValues, 2)
	group, labels = kNN.createDatasetIntegration()
	distances = []
	for i in range(len(group)):
		temp = math.pow((group[i][0]-coefficients[0]), 2) + math.pow((group[i][1]-coefficients[1]), 2) + math.pow((group[i][2]-coefficients[2]), 2)
		point_dist = math.sqrt(temp)
		distances.append((point_dist, labels[i]))

	distances.sort()
	one = 0
	two = 0
	for i in range(3):
		if distances[i][1] == 'one':
			one = one + 1
		else:
			two = two + 1
	print findDirection(xValues, yValues)
	if one > two:
		easygui.msgbox("Gesture 1")
	else:
		easygui.msgbox("Gesture 2")
