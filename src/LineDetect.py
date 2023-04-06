#!/usr/bin/env python3


import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import time
from cv_bridge import CvBridge
import cv2
import numpy as np
import matplotlib.pyplot as plt
from time import sleep


bridge = CvBridge()



def callback(data):
    """
    def make_coordinates(frame, line_parameters):
        slope, intercept = line_parameters
        y1 = frame.shape[0]
        y2 = int(y1*(3/5))
        x1 = int((y1 - intercept)/slope)
        x2 = int((y2 - intercept)/slope)
        return np.array([x1, y1, x2, y2])
    
    def average_slope_intercept(frame, lines):
        left_fit = []
        right_fit = []
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))
        left_fit_average = np.average(left_fit, axis=0)
        right_fit_average = np.average(right_fit, axis=0)
        left_line = make_coordinates(frame, left_fit_average)
        right_line = make_coordinates(frame, right_fit_average)
        return np.array([left_line, right_line])"""




    def canny(frame):
        gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        canny = cv2.Canny(blur, 50, 150)
        return canny
    
    def display_lines(frame, lines):
        line_image = np.zeros_like(frame)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line.reshape(4)
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
        return line_image

    def region_of_interest(frame):
        height = frame.shape[0]
        polygons = np.array([
        [(0, height), (850, height), (650, 300)]
        ])
        mask = np.zeros_like(frame)
        cv2.fillPoly(mask, polygons, 255)
        masked_image = cv2.bitwise_and(frame, mask)
        return masked_image
    
    #frame = cv2.imread('image.png')
    frame = bridge.imgmsg_to_cv2(data, "bgr8")
    
    lane_image = np.copy(frame)
    canny_image = canny(lane_image)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    line_image = display_lines(lane_image, lines)
    combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)

    
    cv2.imshow("win", combo_image)
    cv2.waitKey(10)

def receive():
    rospy.Subscriber("/catvehicle/camera_front/image_raw_front", Image, callback)
    rospy.spin()

if __name__ == "__main__":
    rospy.init_node("receiveImage" , anonymous=True)
    try:
        receive()
        #drive()


    except rospy.ROSInterruptException: pass