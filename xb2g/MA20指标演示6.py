# -*- coding: utf-8 -*-
# 仿通达信指标演示
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
#小白数据规格化
mydf=initmydf(df)  ##初始化mydf表
CLOSE=mydf['close']
LOW=mydf['low']
HIGH=mydf['high']
OPEN=mydf['open']

#用户仿通达信指标计算
mydf['ma20']=MA(CLOSE,20)

mydf['buy']=CROSS(CLOSE,mydf['ma20'])*CLOSE


mydf=mydf.tail(100)  #显示最后100条数据线 
#下面是绘线语句
mydf.close.plot.line(legend=True)
mydf.ma20.plot.line(legend=True)
mydf.buy.plot.line(legend=True)



