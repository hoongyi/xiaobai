# -*- coding: utf-8 -*-
#演示指标库的使用，调用系统KDJ指标，使用自编指标XBHDMMX
'''
这个程序演示了调用系统指标和使用自编指标的方法。
以及获取系统数据mydf表的方法，同理可以获取系统的CLOSE
CLOSE=hgs.CLOSE
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import HP_tdx as htdx
import HP_formula as hgs
from HP_formula import *

global CLOSE,LOW,HIGH,OPEN,VOL
global C,L,H,O,V

#小白换档买卖线
def XBHDMMX(N=24,M=2,X=25):
    MID =MA(CLOSE,N)
    UPPER=MID + 2*STD(CLOSE,N)
    LOWER= MID - 2*STD(CLOSE,N)
    M1=(UPPER-MID)/2+MID
    M2=(MID-LOWER)/2+LOWER
    MM1=EMA((OPEN+CLOSE*2+LOW+HIGH)/5,M);
    MM2=EMA(IF(MM1>=MID,MM1*(1+X/1000),MM1*(1-X/1000)),3)
    MM=MM2
    return MID,UPPER,LOWER,M1,M2,MM


#连接行情主站
htdx.TdxInit(ip='40.73.76.10',port=7709)
code='600080'
#获取日线数据,800条数据
df = htdx.get_k_data(code,ktype='D',index=False,autype='qfq')
mydf=initmydf(df)

#调用系统KDJ指标
mydf['K'],mydf['D'],mydf['J']=KDJ(9,3,3)
mydf['S80']=80  #增加上轨80轨迹线
mydf['X20']=20  #增加下轨20轨迹线

##下面开始调用自编指标
CLOSE=mydf['close']
LOW=mydf['low']
HIGH=mydf['high']
OPEN=mydf['open']
VOL=mydf['volume']

#从系统公式库mydf表中获取数据
C=hgs.mydf['close']
L=hgs.LOW
H=hgs.mydf['high']
O=hgs.mydf['open']
V=hgs.mydf['volume']
#调用自定义指标
MID,UPPER,LOWER,M1,M2,MM=XBHDMMX()

#把指标值添加到mydf数据表中
mydf['MID']=MID
mydf['UPPER']=UPPER
mydf['LOWER']=LOWER
mydf['M1']=M1
mydf['M2']=M2
mydf['MM']=MM


mydf['S80']=80  #增加上轨80轨迹线
mydf['X20']=20  #增加下轨20轨迹线



mydf=mydf.tail(100)  #显示最后100条数据线 
#下面是绘线语句
#绘制主图指标
plt.figure(figsize=(8, 4))
ax1=plt.subplot(211)
mydf.S80.plot.line()
mydf.X20.plot.line()
mydf.K.plot.line(legend=True)
mydf.D.plot.line(legend=True)
mydf.J.plot.line(legend=True)
#绘制副图指标
ax2=plt.subplot(212)
mydf['MID'].plot.line(legend=True)
mydf['UPPER'].plot.line(legend=True,linewidth=3)
mydf['LOWER'].plot.line(legend=True,linewidth=3)
mydf['M1'].plot.line(legend=True)
mydf['M2'].plot.line(legend=True)
mydf['MM'].plot.line(legend=True,linewidth=4)

plt.show()
