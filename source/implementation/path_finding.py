# -*- coding: UTF-8 -*-
'''
Find Path implementation
~~~~~~~~

第一阶段任务
通过结合move模块完成运动，结合network模块完成方向预测，通过config文件中的权值和偏差来初始化网络
'''

## Library
# Standard library
import time
import sys

# Third party library
import numpy as np
import cv2

# my library - configuration
# sys.path.append("/home/pi/Documents/Github/Smart-Car/source/config")
# sys.path.append("/home/pi/Documents/Github/Smart-Car/source/component")
sys.path.append("../config")
sys.path.append("../component")
# import move
import network
import image_preprocess as imgprocess
import common as common_config


## Main function
# major variables
cap = cv2.VideoCapture(0)
mo = move.Move()
net = network.load("../config/result/0316-93%")

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # Change frame to gray level image and do some trasition
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(gray,(64,48),interpolation=cv2.INTER_CUBIC)
    new_img = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i][j] = 0 if img[i][j] < 220 else 255
    new_img = new_img.ravel()
    new_img = [y/255.0 for y in new_img]
    new_img = np.reshape(new_img, (3072, 1))

    # decide direction
    direction = np.argmax(net.feedforward(new_img))

    # Choose direction or quit
    input_key = cv2.waitKey(1) & 0xFF
    if input_key == ord('q'):
        break
    if direction == 0:
        mo.forward(common_config.SLEEP_TIME)
    elif direction == 1:
        mo.turn_left(common_config.SLEEP_TIME)
    elif direction == 2:
        mo.turn_right(common_config.SLEEP_TIME)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
print "Finish recording"

# shutdown the car
mo.stop()
mo.shutdown()
print "Car shutdown"

