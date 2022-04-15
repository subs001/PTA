# PTA
Physiotherapy assistant to aid in performing physical exercises

temp.py: Driver code to run openpose on a video (path specified inside the .py file). Use --net_resolution 128x128 for GPU < 4GB ram

multi_cam.py: Code to run video and webcam feed simultaneously, and get keypoints for both. Uses threading

cam_detect.py: Driver code to run openpose on webcam and get console output of the keypoints using the python api

main_run.py: Runs two bash commands, one to open webcam and the other a video, and runs the openpose detection on both of them. Cannot be modified to output keypoints, purely used to run a video and webcam feed at the same time

