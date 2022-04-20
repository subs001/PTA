import tkinter as tk
import tkinter.filedialog as tkFileDialog
import os
import cv2

def get_thumbnail(vid_dir):
    cap = cv2.VideoCapture(vid_dir)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 10-1)
    res, frame = cap.read()
    cv2.imwrite(vid_dir + "_thumbnail.jpg", frame)

def get_videos(vid_dir):
    for item in os.listdir(vid_dir):
        if item.endswith(('.mp3', '.avi', 'webm')):
            get_thumbnail(vid_dir + "/" + item)
            print(item)

root = tk.Tk()
root.title("Physiotherapy Assistant")
root.geometry("700x500")

root.directory = tkFileDialog.askdirectory()

btn = tk.Button(root, text = "Get Videos" ,
             fg = "red", command=(get_videos,root.directory))
# set Button grid
btn.grid(column=1, row=0)

get_videos(root.directory)


root.mainloop() 
# if__name__ == "__main__":


