# -*- coding: UTF-8 -*-

# third party library
import numpy as np
import cv2

# my library - configuration
import sys
sys.path.append("../config")
import common as common_config

#线性映射数组
def SubLinear():
    aSubLinear = np.zeros(256,np.int8)
    for i in range(256):
        if i<60:
            aSubLinear[i] = int(30.0/60*i)
        elif i<200:
            aSubLinear[i] = int((220.0-30.0)/(200-60)*(i-60)+30)
        else:
            aSubLinear[i] = int((255.0-220.0)/(255-200)*(i-200)+220)
    return aSubLinear

#线性变换
def LinearTrans(image,array=SubLinear()):
    row = image.shape[0]
    col = image.shape[1]
    image2 = np.zeros(image.shape,image.dtype)
    for i in range(row):
        for j in range(col):
            pi = image[i][j]
            image2[i][j] = array[pi]
    return image2

#图像处理，返回摄像头每一帧处理后的灰度图。
#img:灰度图
#(width,height):输出图像尺寸
#zoomR:图像缩放倍数，默认缩小2倍
#输出处理后的图像
def imageDW(img,(height,width),zoomR=1):
    #height,width=img.shape
    img = cv2.resize(img,(width/zoomR,height/zoomR),interpolation=cv2.INTER_CUBIC)
    #线性变换
    img = LinearTrans(img,SubLinear())
    #直方图均衡化
    #img = cv2.equalizeHist(img)
    #降噪-高斯模糊
    img = cv2.GaussianBlur(img,(3,3),0)
    #降噪-中值滤波
    img = cv2.medianBlur(img,3)
    #形态学梯度
    # element = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
    # img_dilate = cv2.dilate(img, element)
    # img_erode = cv2.erode(img, element)
    # img = cv2.absdiff(img_dilate,img_erode)
    #反色，即对二值图每个像素取反
    img = cv2.bitwise_not(img)
    return img
# 初始化摄像头
def initCap():
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,common_config.CAP_WIDTH);
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,common_config.CAP_HEIGHT);
    return cap
# 裁剪图像,img为灰度图
def cutImage(img):
    h,w = img.shape
    img2 = np.zeros((h/2,w),np.int8)
    img2 = img[h-h/2:h-1,0:w-1]
    return img2

def test_module():
    cap = initCap()
    while(cap.isOpened()):
        ret,frame=cap.read()
        img = cutImage(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))#RGB转换为灰度图
        # cv2.imshow('img',img)
        cv2.imshow('img',imageDW(img,img.shape,2))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
