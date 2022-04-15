import sys
import cv2
import os
from sys import platform
import argparse
import time

try:
    print("Running!")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Set this to the python folder inside the build directory
    sys.path.append('/home/subramanian/Documents/VA/openpose/build/python');
    # Import pyopenpose
    from openpose import pyopenpose as op

    # Parsing the arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_known_args()

    # Creating a parameter dictionary
    params = dict()
    params["model_folder"] = "/home/subramanian/Documents/VA/openpose/models" # This should point to the models folder

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

    opWrp = op.WrapperPython()
    opWrp.configure(params)
    opWrp.start()  
    datum = op.Datum() # Contains keypoints and other information

    # Create capture stream
    cap = cv2.VideoCapture("/home/subramanian/Videos/Webcam/sample1.webm")
    if not (cap.isOpened()):
        print("Could not open video device")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
   

    # Run Detections
    while(True): 
        s_time = time.time()
        ret, frame = cap.read()
        # cv2.waitKey(50) # Can use this to delay the frames

        datum.cvInputData = frame
        opWrp.emplaceAndPop(op.VectorDatum([datum]))  
        op_frame = datum.cvOutputData 

        
        cv2.imshow('Video Capture with OpenPose',op_frame)
        print("Body keypoints: \n" + str(datum.poseKeypoints))

        time_period = time.time() - s_time 
        fps = 1/time_period
        print("fps: " + str(fps))
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break

    
except Exception as e:
    print(e)
    sys.exit(-1)