# coding=UTF-8
# -------------------------------------------------------------------------------
# Name:        sxpJudgeCharacter
# Purpose:     This is the package for judging a character is a text or something else
#
# Author:      sunxp
#
# Created:     04/02/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import filters
def testrolling():
    x = [1, 1, 0, 0, 1, 0, 1, 0, 0, 0]
    print((np.bincount(np.arange(5))))
    print((np.bincount(x)))
    dt = pd.DataFrame(x)
    a = dt
    b = dt.rolling(2).sum()
    c = dt.rolling(3).sum()
    dt['sum_2']=b
    dt['sum_3']=c
    dt.plot()
    plt.show()
    print(dt)
def testcolv():
    plt.plot([1, 2, 3, 4])
    plt.plot([1, 1, 3])
    end = np.convolve([1, 2, 3, 4], [1, 1, 3], 'full')
    plt.plot(end)
    plt.show()
def testcolv1():
    x = [1, 1, 0, 0, 1, 0, 1, 0, 0, 0]
    c = np.convolve(x,[2,1,1,2],'full')
    print(c)
    plt.plot(x)
    plt.plot(c)
    plt.show()
def testblur():
    x = [10, 9, 0, 0, 5, 0, 1, 0, 0, 0]
    sigma = 0.4
    b = filters.gaussian_filter(x, sigma)
    print(b)
    plt.plot(x)
    plt.plot(b)
    plt.show()
class gaus_blur:
    def VerticalFlipping(self, data):  # 垂直翻转
        if data.shape[0] <= 1:
            return data
        newarray = np.zeros(data.shape)
        for i in range(data.shape[0]):
            newarray[i] = data[-i - 1]
        return newarray

    def HorizontalFlipping(self, data):  # 水平翻转
        if data.shape[1] <= 1:
            return data
        newarray = np.zeros(data.shape)
        for i in range(data.shape[1]):
            newarray[:, i] = data[:, -i - 1]
        return newarray

    def fuzzy(self, data):  # 图像边缘模糊算法： 镜像模糊
        data = np.array(data)
        if self.level == 2:
            data = np.row_stack((self.VerticalFlipping(data[:self.radius]), data))
            data = np.row_stack((data, self.VerticalFlipping(data[-1:])))
        data = np.column_stack((self.HorizontalFlipping(data[:, :self.radius]), data))
        data = np.column_stack((data, self.HorizontalFlipping(data[:, -self.radius:])))
        return data
class gaus_filter:
    # 滤波函数
    def filter(self, data, template):
        arr = self.fuzzy(data)
        height = arr.shape[0]
        width = arr.shape[1]
        newData = np.zeros((height, width))
        if self.level == 1:
            for i in range(arr.shape[0]):
                for j in range(self.radius, arr.shape[1] - self.radius):
                    t = arr[i, j - self.radius:j + self.radius + 1]
                    a = np.multiply(t, template)
                    newData[i, j] = a.sum()
            return newData[:, self.radius:-self.radius]
        elif self.level == 2:
            for i in range(self.radius, height - self.radius):
                for j in range(self.radius, width - self.radius):
                    t = arr[i - self.radius:i + self.radius + 1, j - self.radius:j + self.radius + 1]
                    a = np.multiply(t, template)
                    newData[i, j] = a.sum()
                    # newImage = Image.fromarray(newData)
            return newData[self.radius:-self.radius, self.radius:-self.radius]
def calc(sigema,x,y=0,level=1):
        if level==1:
            return 1/((2*np.pi)**0.5*sigema)*np.exp(-(x**2/2/(sigema**2)))
        elif level==2:
             return 1/(2*np.pi*sigema*sigema)*np.exp(-(x**2+y**2)/2/sigema/sigema)
if __name__=="__main__":

  #  testhistx()
    #testcolv()
    #testblur()
    testcolv1()
   # testrolling()