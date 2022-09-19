# -*- coding: utf-8 -*-
# KDJ指标演示
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import HP_tdx as htdx  #小白通达信行情库
from HP_formula import *  ##小白公式库
from HP_tdxgs import *  #小白通达信公式库


#连接行情主站
htdx.TdxInit(ip='40.73.76.10',port=7709)
code='600080'
market=htdx.get_market(code)
#获取日线数据,800条数据
df = htdx.get_security_bars(nCategory=4,nMarket = market,code=code,nStart=0, nCount=240)
mydf=initmydf(df)  ##初始化mydf表
##读取财务数据
get_base(market,code)

##换手率
mydf['hsl']=mydf['vol']*100/CAPITAL()

##每股收益
mydf['sy']=FINANCE(33)
##动态市盈率
mydf['syl']=mydf['close']/mydf['sy']

##每股净资产
mydf['jzc']=FINANCE(34)
##动态市净率
mydf['sjl']=mydf['close']/mydf['jzc']

print(mydf[['date','hsl','sy','syl','jzc','sjl']])
