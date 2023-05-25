#! /usr/bin/env python3

import math
from math import pi
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose2D
from tf.transformations import euler_from_quaternion


class Conversion() :

    def __init__(self, odom_topic_name : str = "/odom", \
                 pose2d_topic_name : str = "/pose2d",queue_size : int = 10):

        
        self.sub = rospy.Subscriber(odom_topic_name,Odometry,self.odom_callback)
        self.pub = rospy.Publisher(pose2d_topic_name, Pose2D,queue_size = queue_size)
        self.pose_ = Pose2D()
        

    def odom_callback(self,msg) :


        self.pose_.x = msg.pose.pose.position.x
        self.pose_.y = msg.pose.pose.position.y

        orientation = msg.pose.pose.orientation
        ori = [orientation.x, orientation.y, orientation.z, orientation.w]

        (roll, pitch, yaw) = euler_from_quaternion(ori)
        

        self.pose_.theta = yaw 


        self.pub.publish(self.pose_)


if __name__ == "__main__" :

    rospy.init_node("conversion_node")

    convert = Conversion()

    rospy.spin()

