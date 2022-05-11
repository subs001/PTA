# PTA
Physiotherapy assistant to aid in performing physical exercises

This project makes use of the OpenPose posture tracking library to track movements performed in two separate video feeds, one realtime and the other a chosen video of the exercise the user wishes to follow along with.

The tkinter python library was used to develop a basic GUI to allow the user to interface with our software. The user can select the directory to load the videos from, after which they can choose the video to play. This then opens up the realtime video stream, and the user can observe how well they are performing the exercise.

![image](https://user-images.githubusercontent.com/79127258/167829738-cd8b44e0-5a50-483e-ad6f-cf4e47b3e511.png)

A score is output which reperesents the similarity between the two people performing the exercises. This has been done based on cosine similarity.
![img1](https://user-images.githubusercontent.com/79127258/167834883-2e348828-f5bf-4399-ad95-94af69b50100.png)


We have also implemented a check to determine whether the correct body parts are being used for the exercise. This ensurest that the user performs it in the same manner as done in the reference video.
![img2](https://user-images.githubusercontent.com/79127258/167834987-a5cb6a84-5d11-45e7-96f9-5a4332e50361.png)

At the end of the exercise, the user can view a graph containing the summary of their scores over time.
![Score](https://user-images.githubusercontent.com/79127258/167870249-fcdd2803-f74b-4164-b73b-3567f0029acb.png)
