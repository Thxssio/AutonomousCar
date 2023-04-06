import cv2
import numpy as np
import matplotlib.pyplot as plt

def canny(frame):
        gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        canny = cv2.Canny(blur, 50, 150)
        return canny
    
frame = cv2.imread('image.png')    
lane_image = np.copy(frame)
canny = canny(lane_image)

plt.imshow(canny)
plt.show()