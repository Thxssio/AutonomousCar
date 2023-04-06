#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import time
from cv_bridge import CvBridge
import cv2
bridge = CvBridge()


def drive():
    velocity_publisher = rospy.Publisher('/catvehicle/cmd_vel_safe', Twist, queue_size=10)
    vel_msg = Twist()

    # Init Twist values
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

    # Get parameters from input
    while not rospy.is_shutdown():
        speed = float(input("Type a speed:"))
        angle = float(input("Type an angle:"))
        isForward = int(input("Is Forward:"))

        vel_msg.angular.z = angle

        if(isForward):
            vel_msg.linear.x = abs(speed)
        else:
            vel_msg.linear.x = -abs(speed)

        velocity_publisher.publish(vel_msg)
        time.sleep(2)


def callback(data):
    frame = bridge.imgmsg_to_cv2(data, "bgr8")
    '''
    TODO:Implementation
    '''
    cv2.imshow("win", frame)
    cv2.waitKey(10)

def receive():
    rospy.Subscriber("/catvehicle/camera_front/image_raw_front", Image, callback)
    rospy.spin()

if __name__ == "__main__":
    rospy.init_node("receiveImage" , anonymous=True)
    try:
        receive()
        drive()

    except rospy.ROSInterruptException: pass