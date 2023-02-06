# -*- coding: utf-8 -*-
"""
##  小白量化事件回测程序--A股回测

#购买<零基础搭建量化投资系统>正版书,送小白量化软件源代码。
# https://item.jd.com/61567375505.html
#独狼荷蒲qq:2775205
#通通python量化群:524949939
#电话微信:18578755056
#微信公众号：独狼股票分析
#最后修改日期:2021年01月25日
"""
from HP_view import * #菜单栏对应的各个子页面 
import pandas as pd  
import numpy  as np
import datetime as dt
import time
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
#from matplotlib.finance import candlestick_ohlc
from mpl_finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import matplotlib
from numpy import arange, sin, pi
#from matplotlib.backends.backend_tkagg import FigureCanvasTk,NavigationToolbar2Tk  #matplotlib 2.0.2 
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)    ##matplotlib 3.0.2 
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import math
import HP_tdx as htdx
import HP_lib as mylib
from HP_sys import *
import tkinter as tk
import HP_global as g 
import HP_data as hp
from HP_formula import *#小白量化仿通达信库模块
import HP_tdx as htdx #小白量化通达信莫开
import HP_plt as hplt   #小白量化指标绘图模块
import HP_quant as hqu   #小白量化事件回测


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

htdx.TdxInit(ip='183.60.224.178',port=7709)

#获取股票行情数据
code='301190'
df2 = htdx.get_security_bars(nCategory=4,code=code)
df3=df2

##数据规格化 
df3.dropna(inplace=True)
#对数据做小白量化格式转换
mydf=df3.copy()
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


#调用自定义指标
MID,UPPER,LOWER,M1,M2,MM=XBHDMMX(34,4,32)

#把指标值添加到mydf数据表中
mydf['MID']=MID
mydf['UPPER']=UPPER
mydf['LOWER']=LOWER
mydf['M1']=M1
mydf['M2']=M2
mydf['MM']=MM

#成交量过滤条件,成交量持续大于113均量线
MAV113=MA(V,113);
T1=IF(REF(V,1)>REF(MAV113,1),1,0);
T2=IF(REF(V,2)>REF(MAV113,2),1,0);
T3=IF(V>MAV113,1,0);
T=IF((T1+T2+T3)>=2,1,0);
mydf['T']=T

mydf['b1']=CROSS(mydf['MM'],mydf['LOWER'])
mydf['b2']=CROSS(mydf['MM'],mydf['M2'])
mydf['b3']=CROSS(mydf['MM'],mydf['MID'])
mydf['b4']=mydf['b1']+mydf['b2']+mydf['b3']
mydf['B']=IF(mydf['b4']>0,1,0)   #买入信号

mydf['s1']=CROSS(mydf['UPPER'],mydf['MM'],)
mydf['s2']=CROSS(mydf['M1'],mydf['MM'],)
mydf['s3']=CROSS(mydf['MID'],mydf['MM'],)
mydf['s4']=mydf['s1']+mydf['s2']+mydf['s3']
mydf['S']=IF(mydf['s4']>0,1,0)  #卖出信号



G=hqu.GlobalVars()   #用户全局变量
context = hqu.Context()  #创建回测句柄
data = hqu.Data()  #创建交易数据

data.code=code   #回测品种
data.price=0.0  #成本价

def initialize(context,df):
    print('回测初始化')
    context.f1=0.001   #买入佣金
    context.f2=0.001   #卖出佣金
    context.f3=0.001   #买入印花税
    context.f4=0.00   #卖出印花税
    context.f5=0.00005   #交易费（香港）
    context.f6=0.000027   #交易征费（香港）
    context.f7=0.00002   #交收费（香港）
    context.lot=100   #每手股数
    
    # 定义一个全局变量, 保存要操作的证券                                                                                           
    context.stocks = []   #股票池
    context.cash=1000000.00    #初始现金
    context.cash2=context.cash    #初始现金
    context.i=0        #i是起始位置
    context.start=0        #i是起始位置
    context.end=1500        #i是结束位置

    df['mode']=0  #买卖状态
    df['yl']=0   #盈利
    df['jz']=context.cash  #净值


    context.mydf=df    #df数据

    context.yingli=5.0   #基准盈利
    context.kuisun=-10.0  #基准亏损
    context.volume=0.00   #持仓量
    context.mode=0   #买单状态0:空仓,1:多单,2:空单
    context.end=len(context.mydf)  #结束位置
    context.start=0        #i是起始位置
    context.dc=0.5   #点差
    context.price=0.0   #成本价
    context.s1=0   #买多次数
    context.s2=0   #买空次数
    context.s3=0   #平仓次数
    context.s4=0   #止损次数



#买
def buy(context, data,volume=0.1):
    cash=context.cash
    lot=int(cash/(data.close*(1+context.f1+context.f3))/context.lot)
    context.volume=lot
    context.cash=cash-lot*context.lot*data.close*(1+context.f1+context.f3+context.f5+context.f6+context.f7)
    data.price=data.close*(1+context.f1+context.f3)
    context.mode=1
    context.price=data.price
    context.s1=context.s1+1
    print('买入',lot,data.price)

#卖    
def sell(context, data,volume=0.1):
    cash=data.close*(1-context.f2-context.f4)*context.lot*context.volume
    context.cash=context.cash+cash
    data.price=data.close*(1-context.f2-context.f4)
    lot=context.volume
    context.price=data.price
    context.mode=0
    context.volume=0.0
    context.s2=context.s2+1
    print('卖出',lot,data.price)

mydf['HL']=0.00  #获利比例

#策略初始化
initialize(context,mydf)
context.end=len(mydf)
print(mydf)

#用户策略
def handle_data(context,data):
    i=context.i

    #获取每个数据的值
    df3=context.mydf
    data.high=df3.at[i,'high']
    data.low=df3.at[i,'low']
    data.open=df3.at[i,'open']
    data.close=df3.at[i,'close']
    B=df3.at[i,'B']
    S=df3.at[i,'S']
    
    #计算买卖
    if context.mode==0 and B==1:  #买多
        buy(context, data)
    elif context.mode==1 and S==1:  #买空
        sell(context, data)
    
    #计算获利率
    context.mydf.at[i,'HL']=(context.cash+context.volume*context.lot*data.close-context.cash2)/context.cash2*100


    context.i=i+1   #继续下一个周期


#开始回测
m=context.end-context.start
#循环回测
for i in range(context.start,context.end):
    context.i=i
    handle_data(context,data)
    print('当前进度:',(i*100/m),'资金: ',context.cash)



print('买多:',context.s1,'买空:',context.s2,'止损:',context.s4,'资金:',context.cash)    
print('持仓:', context.volume*context.lot,'现价:',data.close)
print('初始资产:',context.cash2)
print('当前资产:',round(context.cash+context.volume*context.lot*data.close,2))

######下面是绘图
mydf=context.mydf

#数据裁减
m=1
mydf=mydf.tail(150*m).head(150).copy()

#绘制图形
plt.figure(1,figsize=(16,12), dpi=80)

#绘制主图指标
ax1=plt.subplot(311)
plt.title(code+'  日线图')
hplt.ax_K(ax1,mydf,t=data.code,n=0)
mydf['MID'].plot.line(legend=True)
mydf['UPPER'].plot.line(legend=True,linewidth=3)
mydf['LOWER'].plot.line(legend=True,linewidth=3)
mydf['M1'].plot.line(legend=True)
mydf['M2'].plot.line(legend=True)
mydf['MM'].plot.line(legend=True,linewidth=4)

#绘制副图指标
ax2=plt.subplot(312)
mydf['MID'].plot.line(legend=True)
mydf['UPPER'].plot.line(legend=True,linewidth=3)
mydf['LOWER'].plot.line(legend=True,linewidth=3)
mydf['M1'].plot.line(legend=True)
mydf['M2'].plot.line(legend=True)
mydf['MM'].plot.line(legend=True,linewidth=4)


ax3=plt.subplot(313)
plt.sca(ax3)
mydf.HL.plot(color='orange', grid='on',legend=True)
mydf.B.plot(color='blue',legend=True)
mydf.S.plot(color='green',legend=True)
#添加标题
plt.title(code+'  获利')
plt.show()