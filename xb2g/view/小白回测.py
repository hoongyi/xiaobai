# -*- coding: utf-8 -*-
# 小白回测模板
import time
import tkinter as tk
import  tkinter.ttk  as  ttk   #导入Tkinter.ttk
import  tkinter.tix  as  tix   #导入Tkinter.tix
import  HP_tk  as  htk   #导入htk
import HP_global as g 
import HP_data as hp
from HP_view import * #菜单栏对应的各个子页面 
import HP_tdx as htdx

#系统设定了g.tab1--g.tab9,系统只是用了g.tab1--g.tab6
#控件结构 g.root -〉 g.tabControl  -〉g.tab1
#增加tab，用add()
#删除tab,用forget()
#当然用户可以设置更多的tab窗口。必须使用全局变量g.变量名
#重复建立新tab窗会出错，所以我们先检测是否None,不是就先做删除旧tab窗口。


if g.tab5!=None:
    g.tabControl.forget(g.tab5)
    g.tab5=None

#用户自建新画面
g.tab5 = tk.Frame(g.tabControl)
g.tabControl.add(g.tab5, text='小白回测') 
g.tabControl.select(g.tab5)

#回测面板
def hc(frame)    :
    tk.Label(frame, text=' ').grid(row=0, column=0)
    label4 = tk.Label(frame ,width=12, text='股票代码:')
    label4.grid(row=0, column=1)
    #输入框 (Entry)
    g.hcstock = tk.StringVar()  #股票代码
    g.hcstock.set('000001')    
    entryst = tk.Entry(frame,width=10, textvariable=g.hcstock)
    entryst.grid(row=0, column=2)
    
    label1 = tk.Label(frame, width=10, text='开始日期: ',ancho=tk.S)
    label1.grid(row=0, column=3)
    #输入框 (Entry)
    g.hcdate_s = tk.StringVar()
    entrydates = tk.Entry(frame, width=10, textvariable=g.hcdate_s)
    entrydates.grid(row=0, column=4)
    g.hcdate_s.set(g.sday)
    #tk.Label(frame , text=' ').grid(row=0, column=5)
    label2 = tk.Label(frame ,width=10, text='结束日期: ')
    label2.grid(row=0, column=5)
    #输入框 (Entry)
    g.hcdate_e = tk.StringVar()
    entrydatee = tk.Entry(frame, width=10,textvariable=g.hcdate_e)
    g.hcdate_e.set(g.eday)
    entrydatee.grid(row=0, column=6)
    tk.Label(frame , text=' ').grid(row=0, column=7)
    label3 = tk.Label(frame ,width=10, text='初始资金(元):')
    label3.grid(row=0, column=8)
    #输入框 (Entry)
    g.hczj = tk.StringVar()
    g.hczj.set(g.money)    
    entryzj = tk.Entry(frame,width=12, textvariable=g.hczj)
    entryzj.grid(row=0, column=9)
    

    tk.Label(frame , text=' ').grid(row=0, column=11)
    def stt():
        if g.UserCanvas!=None:
            g.UserPlot.cla() 
            g.UserPlot.close()
            g.UserCanvas._tkcanvas.pack_forget() 
            g.UserCanvas=None
#        if g.UserPlot !=None:
#            g.UserPlot.pack_forget()         
    #按钮  (Button)
    getname = tk.Button(frame , text='清除画面' ,command=stt)
    getname.grid(row=0, column=11)

    tk.Label(frame, text=' ').grid(row=1, column=0)
    g.hca=tk.IntVar()
    g.hca.set(0)
    cbtm1= tk.Checkbutton(frame,text='允许止损',variable = g.hca)
    cbtm1.grid(row=1, column=1)
    label5 = tk.Label(frame ,width=12, text='止损阀值(%):')
    label5.grid(row=1, column=2)
    #输入框 (Entry)
    g.hczs = tk.StringVar()
    g.hczs.set('0.05')
    entryzs = tk.Entry(frame,width=6, textvariable=g.hczs)
    
    entryzs.grid(row=1, column=3)
    tk.Label(frame , text=' ').grid(row=1, column=4)
    g.hcb=tk.IntVar()
    g.hcb.set(0)    
    cbtm2= tk.Checkbutton(frame,text='允许止盈',variable = g.hcb)
    cbtm2.grid(row=1, column=5)
    label6 = tk.Label(frame ,width=12, text='止盈阀值(%):')
    label6.grid(row=1, column=6)    
    g.hczy = tk.StringVar()
    g.hczy.set('0.01')
    entryzy = tk.Entry(frame,width=6, textvariable=g.hczy)
    entryzy.grid(row=1, column=7)
 
    tk.Label(frame , text=' ').grid(row=1, column=8)   
    g.hcc=tk.IntVar()
    g.hcc.set(0)      
    cbtm3= tk.Checkbutton(frame,text='允许追涨',variable = g.hcc)
    cbtm3.grid(row=1, column=9)
    label7 = tk.Label(frame ,width=12, text='追涨阀值(%):')
    label7.grid(row=1, column=10)    
    g.hczz = tk.StringVar()
    g.hczz.set('0.05')    
    entryzz = tk.Entry(frame,width=6, textvariable=g.hczz)
    entryzz.grid(row=1, column=11)

    g.hcd=tk.IntVar()
    g.hcd.set(0)   
    tk.Label(frame, text='   ').grid(row=2, column=0)
    cbtm4= tk.Checkbutton(frame,text='自动抄底',variable = g.hcd)
    cbtm4.grid(row=2, column=1)
    g.hce=tk.IntVar()
    g.hce.set(0)     
    tk.Label(frame, text=' ').grid(row=2, column=2)
    cbtm5= tk.Checkbutton(frame,text='自动波段',variable = g.hce)
    cbtm5.grid(row=2, column=3)    
    g.hcf=tk.IntVar()
    g.hcf.set(0)
    tk.Label(frame, text=' ').grid(row=2, column=4)
    cbtm6= tk.Checkbutton(frame,text='允许停损',variable = g.hcf)
    cbtm6.grid(row=2, column=5)    

    label8 = tk.Label(frame ,width=12, text='停损阀值(次):')
    label8.grid(row=2, column=6)    
    g.hcts = tk.StringVar()
    g.hcts.set('9999')    
    entryts = tk.Entry(frame,width=6, textvariable=g.hcts)
    entryts.grid(row=2, column=7)

    label9 = tk.Label(frame ,width=12, text='印花税(%):')
    label9.grid(row=2, column=8)    
    g.hcg = tk.StringVar()
    g.hcg.set('0.001')    
    entryts = tk.Entry(frame,width=6, textvariable=g.hcg)
    entryts.grid(row=2, column=9)

    label10 = tk.Label(frame ,width=12, text='佣金(%):')
    label10.grid(row=2, column=10)    
    g.hch = tk.StringVar()
    g.hch.set('0.0005')    
    entryts = tk.Entry(frame,width=6, textvariable=g.hch)
    entryts.grid(row=2, column=11) 
    
frmt=tk.Frame(g.tab5)
myhc=hc(frmt)
frmt.pack(side=tk.TOP,fill=tk.Y)

#创建frame容器
frmA = ttk.LabelFrame(g.tab5, text='回测输出画板')
frmA.rowconfigure(0,weight=1)
frmA.columnconfigure(0,weight=1)
frmA.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
frmL = tk.Frame(frmA,width =  g.winW-600, \
                height = 800,relief=tk.SUNKEN)
frmR = tk.Frame(frmA,width = 600, \
        height = 800,relief=tk.SUNKEN)
g.UserFrame=frmL

#窗口布局
frmL.grid(row = 0, column = 0,sticky=tk.NSEW)
frmR.grid(row = 0, column = 1,sticky=tk.NSEW)
myedit3=htk.useredit(frmR)
myedit3.textf='''
from HP_draw import * #菜单栏对应的各个子页面 
import pandas as pd  
import matplotlib.pyplot as plt
from matplotlib import ticker as mticker
from mpl_finance import candlestick_ohlc
import matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import HP_tdx as htdx
from HP_formula import *
from HP_sys import *
import tkinter as tk
import HP_global as g 
import HP_data as hp

g.hctitle=''
global CLOSE,LOW,HIGH,OPEN,VOL
global C,L,H,O,V
ds=g.hcdate_s.get()
de=g.hcdate_e.get()
stockn=g.hcstock.get()
df2=htdx.get_k_data(stockn,ktype='D',start=ds,end=de,index=False,autype='qfq')
df3=df2


df3.dropna(inplace=True)

mydf=initmydf(df3)  ##初始化mydf表
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
mydf['B']=0
mydf['S']=0
B=mydf['B']
S=mydf['S']
'''

myedit3.texte='''

mydf['B']=B
mydf['S']=S
g.tabControl.select(g.tab5)

tt=XbQuant()
tt.Init2()
df3=tt.Trade_testing(mydf,'B','S','HL')
print('打印内部交易记录信息')
print(tt.text) 

if g.UserCanvas!=None:
    g.UserPlot.cla() 
    g.UserPlot.close()
    g.UserCanvas._tkcanvas.pack_forget() 
    g.UserCanvas=None


plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False 
fig=plt.figure(2, figsize=(12,8), dpi=80,facecolor=g.ubg)

g.UserFig=fig
g.UserPlot=plt
ax1 = plt.subplot(211,fc=g.ubg)
ax2 = plt.subplot(212,fc=g.ubg)

plt.sca(ax1)
ax_K(ax1,df3,stockn)  
plt.sca(ax1)
plt.suptitle(stockn+' '+g.stock_names[stockn]+'  '+g.hctitle+'回测结果',color=g.ufg)
ax1.tick_params(axis='x', colors='white')
ax1.tick_params(axis='y', colors='white')

plt.sca(ax2)
df3.HL.plot(color='orange', grid=True,label="获利")
df3.B.plot(color='red',label="$B$")
df3.S.plot(color='blue',label="$S$")
plt.ylabel('获利率', color='white')
plt.legend() 
plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
ax2.xaxis.set_major_locator(mticker.MaxNLocator(8))
ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=3, prune='upper'))
ax2.grid(True, color='r')
ax2.tick_params(axis='y', colors='white')
plt.subplots_adjust(left=.075, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)
plt.close()
canvas =FigureCanvasTkAgg(fig, master=g.UserFrame)
#toolbar =NavigationToolbar2TkAgg(canvas, g.UserFrame)
#toolbar.update()

canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
g.UserCanvas=canvas
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
g.hctitle=''
del tt
'''

myedit3.update()
