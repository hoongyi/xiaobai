# -*- coding: utf-8 -*-
# KDJ指标演示
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import HP_global as g  #小白量化全局变量库
from HP_formula import *
import HP_tdx as htdx
import HP_plt as hplt   #小白量化指标绘图模块
import talib

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
#白底色
g.ubg='w'
g.ufg='b'
g.utg='b'
g.uvg='#1E90FF'


global CLOSE,LOW,HIGH,OPEN,VOL
def KDJ(N=9, M1=3, M2=3):
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = SMA(RSV,M1,1)
    D = SMA(K,M2,1)
    J = 3*K-2*D
    return K, D, J


htdx.TdxInit(ip='40.73.76.10',port=7709)

code='603488'
#首先要对数据预处理
df = htdx.get_security_bars(code=code)
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


mydf['sar']=talib.SAR(H,L)

mydf=mydf.tail(100)  #显示最后100条数据线 
print(mydf)

#绘制图形
plt.figure(1,figsize=(12,10), dpi=80)

#绘制主图指标
ax1=plt.subplot(211)
hplt.ax_K(ax1,mydf,t=code,n=0)
plt.scatter(mydf.index,mydf.sar,c="b",label="SAR")
#绘制副图指标
ax2=plt.subplot(212)
mydf.close.plot.line(legend=True)
mydf.sar.plot.line(legend=True)
