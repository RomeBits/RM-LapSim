import cv2 
import numpy as np
from sys import argv

if __name__ == '__main__':
    
    file = argv[1]

    img=cv2.imread(file)
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Source for finding just red pixels
    #   https://stackoverflow.com/questions/30331944/finding-red-color-in-image-using-python-opencv
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    mask = mask0+mask1

    # set my output img to zero everywhere except my mask
    output_img = img.copy()
    output_img[np.where(mask==0)] = 0

    cv2.imwrite('image_thres1.jpg', output_img)
