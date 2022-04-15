import cv2
import pyopenpose as op
import sys
import signal
import time
from absl import app, flags, logging
from absl.flags import FLAGS

flags.DEFINE_boolean('face', False, 'Toggle face display.')
flags.DEFINE_boolean('hand', False, 'Toggle hand display.')

class Detector():
    def __init__(self):
        cap = cv2.VideoCapture(0)
        if not (cap.isOpened()):
            print("Could not open video device")

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
        self.cap = cap 

        # Please refer to this link(https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/01_demo.md)
        # under the "Main Flags" section to adjust the flags parameters.
        params = dict()
        params["model_folder"] = "./models/"
        params["net_resolution"] = "128x128"
        # params["face"] = FLAGS.face
        # params["hand"] = FLAGS.hand  
        self.params = params

        opWrp = op.WrapperPython()
        opWrp.configure(self.params)
        opWrp.start()   
        self.opWrp = opWrp
        self.datum = op.Datum()    

    def __del__(self):
        print("Release video capture")
        self.cap.release()
        cv2.destroyAllWindows()

    def capture(self):
        while(True): 
            s_time = time.time()
            ret, frame = self.cap.read()
            #print(frame.shape)
            op_frame = self.run_op(frame)
            cv2.imshow('Video Capture with OpenPose',op_frame)
            self.display_msg()
            time_period = time.time() - s_time 
            fps = 1/time_period
            print("fps: " + str(fps))
            if cv2.waitKey(33) & 0xFF == ord('q'):
                break

    def capture_1(self):
        while(True):
            s_time = time.time()
            ret, frame = self.cap.read()
            #print(frame.shape)
            op_frame = self.run_op(frame)
            cv2.imshow('Video Capture with OpenPose',op_frame)
            self.display_msg()
            print("--- %s seconds ---" % (time.time() - s_time))
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break
             
    def capture_norm(self):
        while(True): 
            ret, frame = self.cap.read()
            cv2.imshow('Video Capture',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
   
    def run_op(self, frame):
        self.datum.cvInputData = frame
        self.opWrp.emplaceAndPop(op.VectorDatum([self.datum]))  
        return self.datum.cvOutputData 
    
    def display_msg(self):
        print("Body keypoints: \n" + str(self.datum.poseKeypoints))
        # print("Face keypoints: \n" + str(self.datum.faceKeypoints))
        # print("Left hand keypoints: \n" + str(self.datum.handKeypoints[0]))
        # print("Right hand keypoints: \n" + str(self.datum.handKeypoints[1]))               

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

def main(_argv):
    signal.signal(signal.SIGINT, signal_handler)
    dt = Detector()
    # Normal video capture with Openpose
    dt.capture() 
    
    # Uncomment the code below if you only need one capture of openpose image
    #dt.capture_1() 
    
    # Uncomment the code below if you want to check for the video camera capture.
    # dt.capture_norm()   

if __name__=="__main__":
    try:
        app.run(main)
    except SystemExit:
        pass