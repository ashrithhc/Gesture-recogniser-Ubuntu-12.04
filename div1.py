import numpy as np
import cv2
import sys, Image, ImageDraw
import colorsys
import os
import time

def flip_frame(cap, Img):
	Img = cv2.flip(Img, 1)
	width = cap.get(3) #Get the width of the frame.
	height = cap.get(4) #Get the height of the frame.
	# print width,height
	return Img

def find_clusters(Img):
	Img = cv2.cvtColor(Img,cv2.COLOR_BGR2HSV) #convert the obtained image to HSV format and store it in "hsvformat"

	Img = cv2.GaussianBlur(Img, (5, 5), 0) #Blur the image to avoid error at the edges.
	Img = cv2.inRange(Img, np.array((20, 125, 125)), np.array((30, 255, 255))) #threshhold to range given
	image_clusters = cv2.findContours(Img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0] #form list of clusters
	return image_clusters

def form_rectangles(image_clusters, Img):
	for i in image_clusters:
		rect = cv2.boundingRect(np.array(i)) #returns the diagnol coordinates of the rectange formed over set of points.
		cv2.rectangle(Img, (rect[0], rect[1]), ((rect[0]+rect[2]), (rect[1]+rect[3])), (230, 0, 80), 1)
		# (rect[0], rect[1]) = (x, y) of left-top coordinate of rectangle.
		# rect[2] = width, rect[3] = height

def display_grids(Img):
	cv2.line(Img, (0, 160), (640, 160), (255, 0, 0), 1) #horizontal line 1
	cv2.line(Img, (0, 320), (640, 320), (255, 0, 0), 1) #horizontal line 2
	cv2.line(Img, (160, 0), (160, 480), (255, 0, 0), 1) #vertical line 1
	cv2.line(Img, (320, 0), (320, 480), (255, 0, 0), 1) #vertical line 2
	cv2.line(Img, (480, 0), (480, 480), (255, 0, 0), 1) #vertical line 3

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

def track_coordinates(coord): # Returns the grid number of the object.
	# print coord[0], coord[1]
	if coord[1] < 160:
		if coord[0] < 160:
			return "a"
		elif coord[0] < 320:
			return "b"
		elif coord[0] < 480:
			return "c"
		else:
			return "d"
	elif coord[1] < 320:
		if coord[0] < 160:
			return "e"
		elif coord[0] < 320:
			return "f"
		elif coord[0] < 480:
			return "g"
		else:
			return "h"
	else:
		if coord[0] < 120:
			return "i"
		elif coord[0] < 240:
			return "j"
		elif coord[0] < 360:
			return "k"
		else:
			return "l"

def form_string(tracker, grid_num): #forms the string that contains the total object tracking.
	if len(tracker) == 0:
		return str(grid_num)
	elif str(grid_num) == tracker[len(tracker)-1] :
		return tracker
	else:
		return tracker + str(grid_num)

def check_tracker(tracker):
	if len(tracker) > 6:

		if tracker[-6:] == "abcdhl":
			os.system('google-chrome')
			# os.system('xdotool search "Google Chrome" windowactivate --sync key Ctrl+t')
			os.system('xdotool key ctrl+l')
			os.system('xdotool type "facebook.com"')
			os.system('xdotool key KP_Enter')
			return "z"

		elif tracker[-6:] == "lhdcba":
			os.system('rhythmbox')
			os.system('xdotool search "rhythmbox" windowactivate --sync key ctrl+space')
			return "z"

		elif tracker[-6:] == "aeijkl":
			os.system('gnome-terminal')
			os.system('xdotool type "sudo su"')
			os.system('xdotool key KP_Enter')
			time.sleep(1)
			os.system('xdotool type "helloworld"')
			os.system('xdotool key KP_Enter')
			return "z"

		else:
			return tracker
	else:
		return tracker