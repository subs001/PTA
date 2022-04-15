import numpy as np
import cv2
from multiprocessing import Process
import sys
import os
from sys import platform
import argparse
import time
import math
from scipy.spatial.distance import cosine, euclidean
from sklearn import preprocessing
from fastdtw import fastdtw
from scipy import interpolate
from operator import add
# Import pyopenpose

arr1 = []
arr2 = []

# Functions for Video Comparison
# Extract coordinates
def extract_coords(frame):
	x = np.array(frame[0::3])
	y = np.array(frame[1::3])
	return x, y

# Get euclidean distance between frame a, b
def frame_euc_dis(a, b):
	x1, y1 = extract_coords(a)
	x2, y2 = extract_coords(b)
	dist = np.sum((x1 - x2)**2 + (y1 - y2)**2)
	return dist

# Get cosine similarity between frame a, b
def frame_cos_dis(a, b):
	x1, y1 = extract_coords(a)
	x2, y2 = extract_coords(b)
	a_vec = []
	b_vec = []
	for x, y in zip(x1, y1):
		a_vec.append(x)
		a_vec.append(y)
	for x, y in zip(x2, y2):
		b_vec.append(x)
		b_vec.append(y)
	X = np.asarray([a_vec,
		b_vec], dtype=np.float)
	X_normalized = preprocessing.normalize(X, norm='l2')
	dist = cosine(X_normalized[0,:],X_normalized[1,:])
	#dist = np.dot(a_vec, b_vec)
	return dist

# what are these?
lines = {
	0: [1],
	1: [2,5,8,15,16,17,18],
	2: [3],
	3: [4],
	5: [6],
	6: [7],
	8: [9,12],
	9: [10],
	10: [11],
	11: [22,23,24],
	12: [13],
	13: [14],
	14: [19,20,21]
}

def frame_vec(fr):
	form = []
	for i in range(25):
		form.append({'x':fr[2*i],'y':fr[2*i+1],'conf':fr[2*i+2]})
	return form

def frame_cost(a,b):
	a_fr = frame_vec(a)
	b_fr = frame_vec(b)
	total_cost = 0.0
	total_conf = 0.0
	for st in lines:
		for end in lines[st]:
			a_vec = np.array([ a_fr[st]['x']-a_fr[end]['x'], a_fr[st]['y']-a_fr[end]['y'] ])
			b_vec = np.array([ b_fr[st]['x']-b_fr[end]['x'], b_fr[st]['y']-b_fr[end]['y'] ])
			if np.any(a_vec) and np.any(b_vec):
				conf = 1 - math.fabs((a_fr[st]['conf']-b_fr[st]['conf'])*(a_fr[end]['conf']-b_fr[end]['conf']))
				cost = cosine(a_vec,b_vec)*conf
				total_conf += conf
				total_cost += cost

	return total_cost/total_conf

def normalize(frames):
	return preprocessing.normalize(frames, norm='l2')

def remove_confidences(frames):
	return [[coord for i, coord in enumerate(frame) if (i+1)%3 != 0] for frame in frames]

def get_confidences(frames):
	return [[coord for i, coord in enumerate(frame) if (i+1)%3 == 0] for frame in frames]

def get_centroid(frames, coord):
	if coord == 'x':
		coords = np.array([[coord for i, coord in enumerate(frame) if i%3 == 0] for frame in frames])
	else:
		coords = np.array([[coord for i, coord in enumerate(frame) if i%3 == 1] for frame in frames])
	# Return the mean coord
	return np.sum(np.sum(coords, axis=0))/len(coords)

def get_first_hip(frames, coord):
	if coord == 'x':
		return frames[0][24]
	else:
		return frames[0][25]

def translate_video(frames, x_offset, y_offset):
	return [[(coord-x_offset) if i%3==0 else (coord-y_offset) 
	if i%3==1 else coord for i, coord in enumerate(frame)] for frame in frames]

def compare_videos(X, Y):
	X = normalize(X)
	Y = normalize(Y)
	dist, path = fastdtw(X, Y, radius=2, dist=frame_cost)
	return dist

# Function to start a stream from the webcam
def webcam_video(opWrp1): 
    opWrp1.start()  
    datum = op.Datum() # Contains keypoints and other information   
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
    while(True):
        s_time = time.time()
        ret, frame = cap.read()
        # cv2.waitKey(50) # Can use this to delay the frames

        datum.cvInputData = frame
        opWrp1.emplaceAndPop(op.VectorDatum([datum]))  
        op_frame = datum.cvOutputData 

        
        cv2.imshow('Video Capture with OpenPose',op_frame)
        # print("Body keypoints: \n" + str(datum.poseKeypoints))
        arr1.append(np.array(datum.poseKeypoints))
        print("Array 1: " ,len(arr1))

        time_period = time.time() - s_time 
        fps = 1/time_period
        print("fps: " + str(fps))
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
        # ret, frame = cap.read()
        # if ret == True:
        #     cv2.imshow('frame',frame)
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        #     else :
        #         break
    cap.release()
    cv2.destroyAllWindows()

# Function to display a local video
def local_video(opWrp2): 
    opWrp2.start()  
    datum = op.Datum() # Contains keypoints and other information   
    path = "/home/subramanian/Videos/Webcam/sample1.webm"
    cap = cv2.VideoCapture(path)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
    while(True):
        s_time = time.time()
        ret, frame = cap.read()
        cv2.waitKey(50)
        datum.cvInputData = frame
        opWrp2.emplaceAndPop(op.VectorDatum([datum]))  
        op_frame = datum.cvOutputData 

        
        cv2.imshow('Video Capture with OpenPose',op_frame)
        # print("Body keypoints: \n" + str(datum.poseKeypoints))
        arr2.append(np.array(datum.poseKeypoints))
        # print("Array 2: " ,len(arr2))
        print(compare_videos(arr1[0], arr2[0]))
        arr1.pop()
        arr2.pop()

        time_period = time.time() - s_time 
        fps = 1/time_period
        print("fps: " + str(fps))
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
        # if ret == True:
        #     cv2.imshow('frame_2',frame)
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        #     else :
        #         break     
    cap.release()
    cv2.destroyAllWindows()

# Main Function to create the threads and start the streams simultaneously
if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Set this to the python folder inside the build directory
    sys.path.append('/home/subramanian/Documents/VA/openpose/build/python');
    from openpose import pyopenpose as op

    # Parsing the arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_known_args()

    # Creating a parameter dictionary
    params = dict()
    params["model_folder"] = "/home/subramanian/Documents/VA/openpose/models" # This should point to the models folder
    params["net_resolution"] = "128x128"
    # If any other arguments were provided, we add them to the params dictionary as well
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item

    opWrp1 = op.WrapperPython()
    opWrp1.configure(params)
    opWrp2 = op.WrapperPython()
    opWrp2.configure(params)

    p1= Process(target = local_video, args = (opWrp1, ))
    p2= Process(target = webcam_video, args = (opWrp2, ))
    p1.start() 
    p2.start()

    p1.join()
    p2.join()