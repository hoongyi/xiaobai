# -*- coding: utf-8 -*-
# K线图演示
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import HP_global as g   #小白量化全局变量
import HP_tdx as htdx   #小白量化通达信行情
from HP_formula import *  #小白量化公式函数库
import HP_plt as hplt   #小白量化K线显示模块
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
#白底色
g.ubg='w'
g.ufg='b'
g.utg='b'
g.uvg='#1E90FF'

#连接行情主站
htdx.TdxInit(ip='40.73.76.10',port=7709)
code='600080'

##获取日线数据,800条数据
#df = htdx.get_k_data(code,ktype='D',index=False,autype='qfq')
#mydf=initmydf(df)  ##初始化mydf表

#nCategory -> K 线种类 
#0 5 分钟K 线 
#1 15 分钟K 线 
#2 30 分钟K 线 
#3 1 小时K 线 
#4 日K 线 
#5 周K 线 
#6 月K 线 
#7 1 分钟 
#8 1 分钟K 线 
#9 日K 线 
#10 季K 线 
#11 年K 线 
df=htdx.get_security_bars(nCategory=3,nMarket = -1,code=code)  #获取1小时K 线 
mydf=initmydf(df)  ##初始化mydf表

##计算KDJ指标
mydf['K'],mydf['D'],mydf['J']=KDJ(9,3,3)

##增加指标坐标线
mydf['S80']=80  #增加上轨80轨迹线
mydf['X20']=20  #增加下轨20轨迹线


mydf=mydf.tail(100)  #显示最后100条数据线 

#下面是绘图
plt.figure(1,figsize=(10,8), dpi=80)
### 定义主图区域ax1
ax1=plt.subplot(211)
hplt.ax_K(ax1,mydf,t='K线图',n=6)  #绘制K线图，n是均线数量

#定义副图绘图区域ax2
ax2=plt.subplot(212)
##下面是绘制KDJ指标
mydf.S80.plot.line()
mydf.X20.plot.line()
mydf.K.plot.line(legend=True)
mydf.D.plot.line(legend=True)
mydf.J.plot.line(legend=True)

#显示图形
plt.show()
