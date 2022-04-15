from importlib.resources import path
import os
import subprocess
from multiprocessing import Pool

# def run_realtime_video():
#     os.system("./build/examples/openpose/openpose.bin --net_resolution 128x128")

# def run_saved_video(path):
#     os.system("./build/examples/openpose/openpose.bin --net_resolution 128x128 --video " + 
#     path)

run_realtime_video = "./build/examples/openpose/openpose.bin --net_resolution 128x128"
run_saved_video = "./build/examples/openpose/openpose.bin --net_resolution 128x128 --video /home/subramanian/Videos/Webcam/sample1.webm"


def run_process(commands):                                                             
    os.system('{}'.format(commands))      

def main():

    commands = (run_realtime_video, run_saved_video)
    
    try:
        pool = Pool(processes=2)                                                        
        pool.map(run_process, commands)
    except:
        print("Unable to Start Threads")
    print("\nCOMPLETED\n")

if __name__=="__main__":
    main()
