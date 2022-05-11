import math
import numpy as np
from scipy.spatial.distance import cosine, euclidean
from sklearn import preprocessing
from fastdtw import fastdtw
from scipy import interpolate
from operator import add

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
    X = [X.flatten()]
    Y = [Y.flatten()]
    X = normalize(np.array(X))
    Y = normalize(np.array(Y))
    dist, path = fastdtw(X, Y, radius=2, dist=frame_cost)
    return dist