import pandas as pd
import random
import time
import json
import numpy as np
import matplotlib.pyplot as plt
class K_means(object):
    def __init__(self):
        self.df = pd.read_csv('xclara.csv')
        print(self.df)
        self.num = int(input('请输入聚类中心的个数'))
        self.core = []
        self.x1_list = []
        self.x2_list = []
        self.x3_list = []
        self.y1_list = []
        self.y2_list = []
        self.y3_list = []
        self.distance1 = []
        self.List = [[],[],[]]

        for i in range(0,self.num):

            self.core.append(self.df.loc[random.randint(0,3000),:])
        self.plot()

    def First(self):
        for j2 in range(0,3000):

            for i1 in range(0,len(self.core)):
                self.X = ((self.core[i1]['V1']) - (self.df.loc[j2,'V1']))**2

                self.Y = ((self.core[i1]['V2']) - (self.df.loc[j2,'V2']))**2
                self.distance = (self.X+self.Y)**(1/2)
                self.distance1.append(self.distance)

            self.min_distance = min(self.distance1)

            self.List[self.distance1.index(self.min_distance)].append(self.df.loc[j2,:])
            self.distance1 = []
    def circulate(self):
        self.First()
        for i in range(0,3):
            self.sum = 0
            self.sum1 = 0
            for j in range(0,len(self.List[i])):
                self.sum = self.sum + self.List[i][j]['V1']
                self.sum1 = self.sum1 + self.List[i][j]['V2']
            self.x_mean = self.sum/len(self.List[i])
            self.y_mean = self.sum1/len(self.List[i])
            self.core[i] = pd.Series(data={'V1':self.x_mean,'V2':self.y_mean})
            print(self.core[i])
            print(type(self.core[i]))
            self.List2 = self.List
        self.List = [[],[],[]]
    def A(self):
        for i4 in range(15):
            self.circulate()
    def plot(self):
        self.A()
        plt.rcParams['font.sans-serif']=['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.xlim(xmax=-100,xmin=100)
        plt.ylim(ymax=-100,ymin=100)
        for i in range (0,len(self.List2)):
            for j in range(0,len(self.List2[i])):
                self.x1 = self.List2[i][j]['V1']
                self.y1 = self.List2[i][j]['V2']
                if i ==0:
                    self.x1_list.append(self.x1)
                    self.y1_list .append(self.y1)
                if i ==1:
                    self.x2_list.append(self.x1)
                    self.y2_list .append(self.y1)
                if i ==2:
                    self.x3_list.append(self.x1)
                    self.y3_list .append(self.y1)
                self.colors1 = '#00CED1' #点的颜色
                self.colors2 = '#DC143C'
                self.colors3 = '#7FFFD4'
                self.area = np.pi * 2  # 点面积
        self.np_x1 = np.array(self.x1_list)
        self.np_x2 = np.array(self.x2_list)
        self.np_x3 = np.array(self.x3_list)
        self.np_y1 = np.array(self.y1_list)
        self.np_y2 = np.array(self.y2_list)
        self.np_y3 = np.array(self.y3_list)
        plt.scatter(self.np_x1, self.np_y1, s=self.area, c=self.colors1, alpha=0.4, label='类别A',marker='1')
        plt.scatter(self.np_x2, self.np_y2, s=self.area, c=self.colors2, alpha=0.4, label='类别B',marker='p')
        plt.scatter(self.np_x3, self.np_y3, s=self.area, c=self.colors3, alpha=0.4, label='类别C',marker='*')
        plt.legend()
        plt.savefig('julei2.png', dpi=300)
        plt.show()
# 画散点图
K_means = K_means()




