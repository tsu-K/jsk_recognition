#!/usr/bin/env python

import numpy as np
import rospy
from jsk_recognition_msgs.msg import PeoplePoseArray


def callback(data):
    
    index2limbname = ["Nose",
                      "Neck",
                      "RShoulder",
                      "RElbow",
                      "RWrist",
                      "LShoulder",
                      "LElbow",
                      "LWrist",
                      "RHip",
                      "RKnee",
                      "RAnkle",
                      "LHip",
                      "LKnee",
                      "LAnkle",
                      "REye",
                      "LEye",
                      "REar",
                      "LEar",
                      "Bkg"]

    pose_array = []

    for limb in index2limbname:
    
        try:
            position = data.poses[0].poses[data.poses[0].limb_names.index(limb)].position
            pose_array.append([position.x, position.y, position.z])

        except:
            pose_array.append([np.nan])
            
    #print(pose_array)
    
def listener():

    rospy.init_node('pose_sub', anonymous=True)

    rospy.Subscriber("~input/pose", PeoplePoseArray, callback)
    rospy.spin()

if __name__=='__main__':
    listener()
