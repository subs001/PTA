import cv2
import sys
import os
# from sys import platform
import argparse
from comparison import compare_videos
from limb_comp import comp_limbs
import numpy as np


# Path Variable
path = "/home/subramanian/Videos/Webcam/sample1.webm"
500
# Start opWrp and Return datum object
def startOpWrp(opWrp):
    opWrp.start()
    return op.Datum()

# Function to take in a frame and return a frame with openpose detections
def frame_detect(datum, opWrp, frame):
    datum.cvInputData = frame
    opWrp.emplaceAndPop(op.VectorDatum([datum]))  
    return datum.cvOutputData 

# Function set cv2 window parameters
def set_window_prop(cap):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 854)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Function to combine frames
def combine_frames(frame1, frame2):
    frame2Resized = cv2.resize(frame2,(frame1.shape[1], frame1.shape[0]))
    numpy_horizontal = np.hstack((frame1, frame2Resized))
    return numpy_horizontal

# get similarity percentage
def get_sim_percentage(score):
    new_score = (1/score)
    if new_score > 100:
        return 99
    else: 
        return round(new_score, 2)

def run_videos(opWrp1, opWrp2):
    cap1 = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(path)
    set_window_prop(cap1)
    set_window_prop(cap2)

    datum1 = startOpWrp(opWrp1)
    datum2 = startOpWrp(opWrp2)

    # correct_limbs = ""

    while(True):
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        opFrame1 = frame_detect(datum1, opWrp1, frame1)
        opFrame2 = frame_detect(datum2, opWrp2, frame2)

        final_frame = combine_frames(opFrame1, opFrame2)
        
        # cv2.imshow('Window 1',opFrame1)
        # cv2.imshow('Window 2',opFrame2)
        
        if (not datum1.poseKeypoints is None) and (not datum2.poseKeypoints is None):
            k1 = datum1.poseKeypoints[0]
            k2 = datum2.poseKeypoints[0]
            sim_score = str(compare_videos(k1, k2))
            percentage = get_sim_percentage(float(sim_score))
            if not comp_limbs(k1, k2):
                final_frame = cv2.putText(final_frame, "Please Use the Correct Body Part", (50,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
            final_frame = cv2.putText(final_frame, str(percentage) + "%", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)
        
        cv2.imshow("Physiotherapy Assistant: ", final_frame)
        
        if not ret1 or not ret2:
            print('Cant read the video , Exit!')
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
        cv2.waitKey(1)

    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Set this to the python folder inside the build directory
    sys.path.append('/home/subramanian/Documents/VA/openpose/build/python');
    try:
        from openpose import pyopenpose as op
    except:
        print("pyopenpose could not be imported. Check BUILD and PATH")

    # Parsing the arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_known_args()

    # Creating a parameter dictionary
    params = dict()
    params["model_folder"] = "/home/subramanian/Documents/VA/openpose/models" # This should point to the models folder
    params["net_resolution"] = "128x128"
    params["number_people_max"] = 1
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
    opWrp2 = op.WrapperPython()
    opWrp1.configure(params)
    opWrp2.configure(params)

    run_videos(opWrp1, opWrp2)
