# -*- coding: utf-8 -*-
# KDJ指标演示
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from HP_formula import *
import tushare as ts
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

global CLOSE,LOW,HIGH,OPEN,VOL
def KDJ(N=9, M1=3, M2=3):
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = SMA(RSV,M1,1)
    D = SMA(K,M2,1)
    J = 3*K-2*D
    return K, D, J

def SMMA(c,N,M):
    SUM1 = SUM(c, N)
    SMMA1 = SUM1/N
    SMMA2 =  (SUM1-SMMA1+c)/M
    return SMMA2

def LWMA(c,N):
    l1=SUM(c,N)
    
    SUM(Close(i)*i, N)/SUM(i, N)


#首先要对数据预处理
df = ts.get_k_data('600080',ktype='D')
mydf=df.copy()
CLOSE=mydf['close']
LOW=mydf['low']
HIGH=mydf['high']
OPEN=mydf['open']
VOL=mydf['volume']
C=mydf['close']
L=mydf['low']
H=mydf['high']
O=mydf['open']
V=mydf['volume']

mydf['K'],mydf['D'],mydf['J']=KDJ(9,3,3)
mydf['S80']=80  #增加上轨80轨迹线
mydf['X20']=20  #增加下轨20轨迹线

mydf['J2']=REF(mydf['J'],3)

MEDIAN_PRICE = (HIGH + LOW) / 2

mydf['鳄鱼的下巴'] = SMMA (MEDIAN_PRICE, 13, 8)
mydf['鳄鱼的牙齿'] = SMMA (MEDIAN_PRICE, 8, 5)
mydf['鳄鱼的嘴唇'] = SMMA (MEDIAN_PRICE, 5, 3)
mydf=mydf.tail(100)  #显示最后100条数据线 
##下面是绘线语句
#mydf.S80.plot.line()
#mydf.X20.plot.line()
#mydf.K.plot.line(legend=True)
#mydf.D.plot.line(legend=True)
#mydf.J.plot.line(legend=True)
#mydf.J2.plot.line(legend=True)
mydf['鳄鱼的下巴'].plot.line(legend=True)
mydf['鳄鱼的牙齿'].plot.line(legend=True)
mydf['鳄鱼的嘴唇'].plot.line(legend=True)
