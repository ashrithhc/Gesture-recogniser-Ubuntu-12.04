from numpy import *
import operator

def createDataset():
	group = array([35, 65, 85, -5, -35, -65])
	labels = ['one', 'one', 'one', 'two', 'two', 'two']
	return group, labels

def createDatasetIntegration():
	group = array([[ -2.80373832e-02,   1.82242991e+00,   5.68691589e+01], [ -2.59367142e-02,   2.30760949e+00,   3.53952336e+01], [  1.15763547e-02,  -5.07613077e-02,   5.34791760e+01], [  2.80373832e-02,  -2.66355140e+00,   6.67757009e+01], [ -1.20998606e-02,  -3.64504885e-01,   9.10102742e+01], [  7.55535125e-03,  -1.50064461e+00,   8.25024609e+01]])
	labels = ['one', 'one', 'one', 'two', 'two', 'two']
	return group, labels