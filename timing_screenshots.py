# -*- coding: utf-8 -*-
"""
一个定时截屏小程序
每30秒截屏一次，如果图片和上一张相同，则移动到备份中
"""

import pyautogui  # pip3 install pyautogui
import time
from datetime import datetime
import cv2  # pip3 install  opencv-python
import os
import shutil
# Hash值对比
def cmpHash(hash1, hash2, shape=(10, 10)):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 相等则n计数+1，n最终为相似度
        if hash1[i] == hash2[i]:
            n = n + 1
    return n / (shape[0] * shape[1])


# 均值哈希算法
def aHash(img, shape=(10, 10)):
    img = cv2.imread(img)
    # 缩放为10*10
    img = cv2.resize(img, shape)
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(shape[0]):
        for j in range(shape[1]):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / 100
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(shape[0]):
        for j in range(shape[1]):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


img_list = []
if not os.path.exists('D:\screenshot'):
    os.mkdir('D:\screenshot')
if not os.path.exists(r'D:\screenshot\bak'):  # 重复的文件放到备份里
    os.mkdir(r'D:\screenshot\bak')
while True:
    time.sleep(30)  # 每30秒截图，放到D:\screenshot中
    img_path = r'D:\screenshot\%s.png' % datetime.now().strftime('%H_%M_%S')
    print('开始截图%s......\n' % img_path)
    # 截图
    im = pyautogui.screenshot(img_path)
    img_list.append(img_path)
    # 如果多于两张图则开始比较最后两张
    if len(img_list) >= 2:
        hash_last = aHash(img_list[-1])
        hash_penultimate = aHash(img_list[-2])
        n = cmpHash(hash_last, hash_penultimate)
        print("%s与%s相似度为%s\n" % (img_list[-1], img_list[-2], n))
        if n >= 0.95:
            # 如果两张图相似，移动最后一张,且将它从列表里移除
            print("图片和上一张相同,移动图片%s到备份文件夹...\n" % img_list[-1])
            shutil.move(img_list[-1], r'D:\screenshot\bak')
            img_list.pop()
    print("当前存放的图片共%s张,为%s\n" % (len(img_list), img_list))
