import numpy as np

body_part_dict = {

        1: "Neck",
        2: "RShoulder",
        3: "RElbow",
        4: "RWrist",
        5: "LShoulder",
        6: "LElbow",
        7: "LWrist",
        8: "MidHip",
        9: "RHip",
        10: "RKnee",
        11: "RAnkle",
        12: "LHip",
        13: "LKnee",
        14: "LAnkle",


        21: "LHeel",

        24: "RHeel",
        25: "Background"
        }

def get_bodyparts(keypoints):
    arr = []
    for i in keypoints:
        if np.sum(i) > 0:
            arr.append(1)
        else:
            arr.append(0)
    return arr

def comp_limbs(k1, k2):
    arr1 = get_bodyparts(k1)
    arr2 = get_bodyparts(k2)
    for i in range(len(arr2)):
        if arr2[i] == 1 and arr1[i] == 0:
            return False
    return True