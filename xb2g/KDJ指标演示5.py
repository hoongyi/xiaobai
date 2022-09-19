# -*- coding: utf-8 -*-
# KDJ指标演示
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


mydf['K'],mydf['D'],mydf['J']=KDJ(9,3,3)

mydf['S80']=80  #增加上轨80轨迹线
mydf['X20']=20  #增加下轨20轨迹线


mydf=mydf.tail(100)  #显示最后100条数据线 
#下面是绘线语句
mydf.S80.plot.line()
mydf.X20.plot.line()
mydf.K.plot.line(legend=True)
mydf.D.plot.line(legend=True)
mydf.J.plot.line(legend=True)


