# -*- coding: utf-8 -*-
#指标演示
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import HP_tdx as htdx
from HP_formula import *



#连接行情主站
htdx.TdxInit(ip='40.73.76.10',port=7709)
code='600080'
#获取日线数据,800条数据
df = htdx.get_k_data(code,ktype='D',index=False,autype='qfq')
mydf=initmydf(df)  ##初始化mydf表

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

sh=SLOPE(H,18);
rh=(sh-MA(sh,600))/STD(sh,600);
sl=SLOPE(L,18);
rl=(sl-MA(sl,600))/STD(sl,600);



#绘制图形
plt.figure(1,figsize=(10,6), dpi=100)
#绘制主图指标
ax1=plt.subplot(311)
mydf.close.tail(200).plot.line(legend=True)
#绘制副图指标
ax2=plt.subplot(312)
#绘制副图指标
#下面是绘线语句
sh.tail(200).plot.line(legend=True,label='sh')
rh.tail(200).plot.line(legend=True,label='rh')
ax3=plt.subplot(313)
sl.tail(200).plot.line(legend=True,label='sl')
rl.tail(200).plot.line(legend=True,label='rl')
plt.show()

