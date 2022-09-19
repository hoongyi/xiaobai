# -*- coding: utf-8 -*-
"""
#功能：通通股票分析软件框架 回测工具
#版本：Ver1.00
#设计人：独狼荷蒲
#电话:18578755056
#QQ：2775205
#百度：荷蒲指标
#开始设计日期: 2018-07-08
#公众号:独狼股票分析
#使用者请同意最后<版权声明>
#最后修改日期:2021年8月16日
"""

import sys,os
import numpy as np
import pandas as pd
import HP_global as g   #建立全局数据域g
from HP_formula import *

#证券类
class security():
    def __init__(self): #类初始化
        self.market =0   #市场
        self.type=0     #种类
        self.index=False     #指数
        self.category=0  #数据周期
        self.stockcode=''  #代码
        self.name=''    #名称
        self.py=''     #拼音简称
        self.start_date=''   #开始日期
        self.end_date=''    #结束日期
        self.count =0  #周期数
        self.df=None   #行情表


#小白面板回测类
class XbQuant(object):
    def __init__(self): #类初始化
        self.order_df=None   #下单流水
        self.trade_df=None   #交易流水
        self.security_df=None   #持仓清单
        self.money2=1000000.00  #总资金
        self.money=1000000.00  #资金
        self.priceBuy=0.00    #最后一次买入价格
        self.priceSell=999999.00  #最后一次卖出价格
        self.amount=0.00   #证券数量
        self.code=""   #证券代码
        self.stamp_duty=0.001   #印花税 0.1%
        self.trading_Commission=0.0005    #交易佣金0.05%
        self.priceStopLoss=0.00   #止损价
        self.position=False   #持仓状态
        self.stop_loss_on=True #允许止损
        self.stop_loss_num=0   #当前止损次数
        self.stop_loss_max=50 #最大允许止损次数.到止损次数,就停止交易
        self.stop_loss_range=0.05   #止损幅度
        self.trade=True   #允许交易
        self.Init()

    def Init(self): #初始化交易数据
        self.order_df = pd.DataFrame(columns = ['date', 'time','mode','code','amount','price']) 
        self.order_df =self.order_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        self.trade_df = pd.DataFrame(columns = ['date', 'time','mode','code','amount','price','money']) 
        self.trade_df =self.trade_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        self.security_df = pd.DataFrame(columns = ['code','amount','price','money']) 
        self.security_df =self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  

    def Init2(self): #初始化交易数据
        self.code=g.hcstock.get() #股票代码
        self.code=self.code.strip()
        self.code=self.code.zfill(6)
        g.hcstock.set(self.code)
        self.date_s=g.hcdate_s.get() #开始日期
        self.date_e=g.hcdate_e.get() #结束日期
        self.hca=g.hca.get()  #允许止损
        #print(type(self.hca))
        if self.hca==1:
            self.stop_loss_on=True
        else:
            self.stop_loss_on=False
        self.hczs=float(g.hczs.get()) #止损阀值(%)
        self.hcb=g.hcb.get()  #允许止盈
        self.hczy=float(g.hczy.get()) #止盈阀值(%)
        self.hcc=g.hcc.get()  #允许追涨
        self.hczz=float(g.hczz.get()) #追涨阀值(%)
        self.hcd=g.hcd.get()  #自动抄底
        self.hce=g.hce.get()  #自动波段
        self.hcf=g.hcf.get()  #允许停损
        self.stop_loss_max=int(g.hcts.get()) #停损阀值(次)
        self.stamp_duty=float(g.hcg.get())  #印花税(%)
        self.trading_Commission=float(g.hch.get())  #佣金(%)
        self.money2=float(g.hczj.get())  #初始资金        
    
    def PrintOrder(self): #输出下单流水
        print(self.order_df)

    def PrintTrade(self): #输出交易流水
        print(self.trade_df)

    def PrintSecurity(self): #输出持仓清单
        print(self.security_df)

    def Order(self,date,time,mode,code,amount,price): #交易函数
        ln=len(self.order_df)
        df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,'price':price},index=[ln])
        self.order_df=self.order_df.append( df_new,ignore_index=True)

        ln=len(self.trade_df)
        if mode==1:   #买入
            se=amount*price*(1+self.trading_Commission)
            self.money=self.money-se
            df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,'price':price,'money':self.money},index=[ln])
            self.trade_df=self.trade_df.append( df_new,ignore_index=True)
            if len(self.security_df[self.security_df.code==code])==0 :
                df_new = pd.DataFrame({'code':code,'amount':amount,'price':se/amount,'money':se},index=[ln])
                self.security_df=self.security_df.append( df_new,ignore_index=True)
            else:
                self.security_df.index=self.security_df['code']
                self.security_df.loc[code,'amount']=self.security_df.loc[code,'amount']+amount
                self.security_df=self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        
        ln=len(self.security_df[self.security_df.code==code])
        if mode==2 and ln>0:  #卖出
            self.security_df.index=self.security_df['code']
            am=self.security_df.loc[code,'amount']
            
            if am<amount :
                amount=am
            se=amount*price*(1-self.trading_Commission-self.stamp_duty)
            self.money=self.money+se
            df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,'price':price,'money':self.money},index=[ln])
            self.trade_df=self.trade_df.append( df_new,ignore_index=True)
            am2=self.security_df.loc[code,'amount']-amount
            self.security_df.loc[code,'amount']=am2
            if am2==0:
                self.security_df=self.security_df.drop(code, axis = 0) # 在行的维度上删除行
            self.security_df=self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  


#####################回测功能#########################
    def Trade_testing(self,df,tp1,tp2,al=''):   #回测函数
        self.Init()
        self.Init2()
        self.trade=True   #允许交易
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
        
        #HPYYX python HPYYX指标
        def HPYYX():
            RSV= (C-LLV(L,9))/(HHV(H,9)-LLV(L,9))*100
            FASTK=SMA(RSV,3,1)
            RSV1= (HHV(H,9)-C)/(HHV(H,9)-LLV(L,9))*100
            LC = REF(C,1)
            RSI1=SMA(MAX(C-LC,0),13,1)/SMA(ABS(C-LC),13,1)*100
            RSI2=SMA(MAX(C-LC,0),6,1)/SMA(ABS(C-LC),6,1)*100
            RSI3=IF(RSI2>50,RSI2*1.05,RSI2)
            RSV3=(C-LLV(L,54))/(HHV(H,54)-LLV(L,54))*100
            HT=IF(RSI3>100,100,RSI3)
            YIN=SMA((SMA(RSV1,3,1)/2)*1.1,3,1)
            YANG=SMA(((SMA(FASTK,3,1))/2+40)*1.1,3,1)
            ZL2=EMA(RSI2,13)
            ZL=IF(ZL2>50,ZL2*1.3,ZL2*0.9)
            return YIN, YANG,HT,ZL
        
        
        #使用HPYYX指标，返回YIN, YANG,HT,ZL序列。
        YIN, YANG,HT,ZL=HPYYX()
        mydf = mydf.join(pd.Series( YIN,name='YIN'))
        mydf= mydf.join(pd.Series( YANG,name='YANG'))
        mydf = mydf.join(pd.Series( ZL,name='ZL'))
        mydf = mydf.join(pd.Series( HT,name='HT'))
        mydf['SG']=85  #增加上轨80轨迹线
        mydf['X20']=20  #增加下轨20轨迹线
        mydf['Z50']=50  #增加中轨50轨迹线
        
        ##下面开始生成HPYYX指标买卖点
        ##买点ZL上穿数值YIN
        b1=CROSS(mydf['ZL'],mydf['YIN'])
        mydf = mydf.join(pd.Series( b1,name='BB1'))  
        
        ##卖点ZL下穿80
        s1=CROSS(mydf['SG'],mydf['ZL'])
        
        #卖点ZL下穿50
        s2=CROSS(mydf['Z50'],mydf['ZL'])
        
        #合并所有卖点信号
        s3=s1 | s2
        
        mydf = mydf.join(pd.Series( s3,name='SS1'))          

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
        
        ##HPCPX交易策略 
        #在ax区
        def HPCPX():
            S0=(CLOSE+OPEN+LOW+HIGH)/4
            S1=EMA(SLOPE(S0,5),60)
            S2=EMA(S1,20)
            S3=IF(S1>=0,S1,DRAWNULL())
            S4=IF(S1>S2 ,S3,DRAWNULL())
            return S1,S2,S4
        #使用HPCPX指标，返回x,y,x序列。
        x,y,z=HPCPX()
        
        mydf['CPX']=x
        mydf['Y']=y
        mydf['Z']=z
        mydf['Y0']=0
        
        ##下面开始生成HPCPX指标买卖点
        ##买点CPX上穿数值0
        b1=CROSS(mydf['CPX'],mydf['Y0'])
        b2=CROSS(mydf['CPX'],mydf['Y'])
        #b1 或者(b2 且 CPX大于0值)
        b3=b1 | (b2 & IF(mydf['CPX']>0,1,0))
        
        ##卖点CPX下穿Y
        s1=CROSS(mydf['Y'],mydf['CPX'])
        

        cc=IF(x>y,1,0)
        mydf = mydf.join(pd.Series( b3,name='BB2'))  
        mydf = mydf.join(pd.Series( s1,name='SS2'))  
        mydf = mydf.join(pd.Series( cc,name='CC'))  
        
        if self.hcd==1:
            mydf[tp1]=IF(mydf['BB1']>0,2,mydf[tp1])
            mydf[tp2]=IF(mydf['SS1']>0,2,mydf[tp2])

        if self.hce==1:
            mydf[tp1]=IF(mydf['BB2']>0,3,mydf[tp1])
            mydf[tp2]=IF(mydf['SS2']>0,3,mydf[tp2])            
        
        mydf['BIAS1']=(CLOSE-MA(CLOSE,10))/MA(CLOSE,10)
        mydf['HHA']=MA(mydf['high'],10)*mydf['BIAS1']

        mydf['CZB']=0
        mydf['CZS']=0
        df=mydf.copy()
        
        myMoney=self.money2
        if (al.strip()==''):
            na='property'
        else:
            na=al 
        self.text='    ----开始回测-----\n'
        i = 0  
        ZB_l = []
        while i < len(df):  
            close=df.close.at[i]
            if (df[tp1].at[i] ==1 and self.position==False and self.trade==True) :  #普通买入
                self.priceBuy=close
                x=int(myMoney/(self.priceBuy*(1+self.trading_Commission))/100)
                self.amount=x*100.00
                self.Order(df.date.at[i],'14:45:01',1,self.code,self.amount,close)
                myMoney=myMoney-self.amount*self.priceBuy*(1.00+self.trading_Commission)
                self.position=True
                self.priceStopLoss=self.priceBuy*(1-self.stop_loss_range)
                self.text=self.text+'日期:'+df.date.at[i]+' 普通买入:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceBuy,2))+'\n'
                df['CZB'].at[i]=df[tp1].at[i]

            if (df[tp1].at[i] ==2 and self.position==False and self.trade==True) :  #抄底买入
                self.priceBuy=close
                x=int(myMoney/(self.priceBuy*(1+self.trading_Commission))/100)
                self.amount=x*100.00
                self.Order(df.date.at[i],'14:45:01',1,self.code,self.amount,close)
                myMoney=myMoney-self.amount*self.priceBuy*(1.00+self.trading_Commission)
                self.position=True
                self.priceStopLoss=self.priceBuy*(1-self.stop_loss_range)
                self.text=self.text+'日期:'+df.date.at[i]+' 抄底买入:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceBuy,2))+'\n'
                df['CZB'].at[i]=df[tp1].at[i]
            
            if (df[tp1].at[i] ==3 and self.position==False and self.trade==True) :  #波段买入
                self.priceBuy=close
                x=int(myMoney/(self.priceBuy*(1+self.trading_Commission))/100)
                self.amount=x*100.00
                self.Order(df.date.at[i],'14:45:01',1,self.code,self.amount,close)
                myMoney=myMoney-self.amount*self.priceBuy*(1.00+self.trading_Commission)
                self.position=True
                self.priceStopLoss=self.priceBuy*(1-self.stop_loss_range)
                self.text=self.text+'日期:'+df.date.at[i]+' 波段买入:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceBuy,2))+'\n'
                df['CZB'].at[i]=df[tp1].at[i]            
            
            if (df[tp2].at[i] ==1 and self.position==True and self.trade==True) : #普通卖出
                self.priceSell=close
                myMoney=myMoney+self.amount*self.priceSell*(1.00-self.trading_Commission-self.stamp_duty)
                self.position=False
                self.Order(df['date'].at[i],'14:45:02',2,self.code,self.amount,self.priceSell)
                self.text=self.text+'日期:'+df.date.at[i]+' 普通卖出:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceSell,2))+'获利:'+str(round((myMoney-self.money2)/self.money2*100,2))+'%\n'
                self.amount=0.00
                df['CZS'].at[i]=df[tp2].at[i]    

            if (df[tp2].at[i] ==2 and self.position==True and self.trade==True) : #逃顶卖出
                self.priceSell=close
                myMoney=myMoney+self.amount*self.priceSell*(1.00-self.trading_Commission-self.stamp_duty)
                self.position=False
                self.Order(df['date'].at[i],'14:45:02',2,self.code,self.amount,self.priceSell)
                self.text=self.text+'日期:'+df.date.at[i]+' 逃顶卖出:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceSell,2))+'获利:'+str(round((myMoney-self.money2)/self.money2*100,2))+'%\n'
                self.amount=0.00
                df['CZS'].at[i]=df[tp2].at[i]   

            if (df[tp2].at[i] ==3 and self.position==True and self.trade==True) : #波段卖出
                self.priceSell=close
                myMoney=myMoney+self.amount*self.priceSell*(1.00-self.trading_Commission-self.stamp_duty)
                self.position=False
                self.Order(df['date'].at[i],'14:45:02',2,self.code,self.amount,self.priceSell)
                self.text=self.text+'日期:'+df.date.at[i]+' 波段卖出:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceSell,2))+'获利:'+str(round((myMoney-self.money2)/self.money2*100,2))+'%\n'
                self.amount=0.00
                df['CZS'].at[i]=df[tp2].at[i]   
                
            if (close<=self.priceStopLoss and self.position==True and self.trade  and self.stop_loss_on):  #止损卖出
                self.priceSell=self.priceStopLoss-0.01
                myMoney=myMoney+self.amount*self.priceSell*(1.00-self.trading_Commission-self.stamp_duty)
                self.position=False
                self.stop_loss_num=self.stop_loss_num+1
                self.Order(df['date'].at[i],'14:45:02',2,self.code,self.amount,self.priceSell)
                self.text=self.text+'日期:'+df.date.at[i]+' 止损卖出:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceSell,2))+'获利:'+str(round((myMoney-self.money2)/self.money2*100,2))+'%\n'
                self.amount=0.00
                if (self.stop_loss_num>=self.stop_loss_max):
                    self.trade=False
                df['CZS'].at[i]=4

            if (close>=self.priceSell*(1+self.hczz) and self.position==False and self.trade  and self.hcc==1) : #追涨买入
                self.priceBuy=close
                x=int(myMoney/(self.priceBuy*(1+self.trading_Commission))/100)
                self.amount=x*100.00
                self.Order(df.date.at[i],'14:45:01',1,self.code,self.amount,close)
                myMoney=myMoney-self.amount*self.priceBuy*(1.00+self.trading_Commission)
                self.position=True
                self.priceStopLoss=self.priceBuy*(1-self.stop_loss_range)
                self.text=self.text+'日期:'+df.date.at[i]+' 追涨买入:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceBuy,2))+'\n'
                df['CZB'].at[i]=4        

            if (close<df['HHA'].at[i]*(1-self.hczy) and self.position==True and self.trade  and self.hcb==1) : #止赢卖出
                self.priceSell=self.priceStopLoss-0.01
                myMoney=myMoney+self.amount*self.priceSell*(1.00-self.trading_Commission-self.stamp_duty)
                self.position=False
                self.stop_loss_num=self.stop_loss_num+1
                self.Order(df['date'].at[i],'14:45:02',2,self.code,self.amount,self.priceSell)
                self.text=self.text+'日期:'+df.date.at[i]+' 止赢卖出:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceSell,2))+'获利:'+str(round((myMoney-self.money2)/self.money2*100,2))+'%\n'
                self.amount=0.00
                df['CZS'].at[i]=5                

            y= (myMoney+self.amount*close-self.money2)/self.money2 *100 
            ZB_l.append(y)  
            i = i + 1          
            
        ZB_s = pd.Series(ZB_l)  
        ZB = pd.Series(ZB_s, name = na)  
        df = df.join(ZB)  
        self.money=myMoney
        y= (myMoney+self.amount*close-self.money2)/self.money2  *100
        self.text=self.text+'总投入'+str(round(self.money2,2))+',最终获利幅度'+str(round(y,0))+'%\n'
            
        return df


#交易回测类
class hpQuant(object):
    def __init__(self): #类初始化
        self.order_df=None   #下单流水
        self.trade_df=None   #交易流水
        self.security_df=None   #持仓清单
        self.money2=1000000.00  #总资金
        self.money=1000000.00  #资金
        self.priceBuy=0.00    #最后一次买入价格
        self.priceSell=999999.00  #最后一次卖出价格
        self.amount=0.00   #证券数量
        self.code=""   #证券代码
        self.stamp_duty=0.001   #印花税 0.1%
        self.trading_Commission=0.0005    #交易佣金0.05%
        self.priceStopLoss=0.00   #止损价
        self.position=False   #持仓状态
        self.stop_loss_on=True #允许止损
        self.stop_loss_num=0   #当前止损次数
        self.stop_loss_max=50 #最大允许止损次数.到止损次数,就停止交易
        self.stop_loss_range=0.05   #止损幅度
        self.trade=True   #允许交易
        self.Init()

    def Init(self): #初始化交易数据
        self.order_df = pd.DataFrame(columns = ['date', 'time','mode','code','amount','price']) 
        self.order_df =self.order_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        self.trade_df = pd.DataFrame(columns = ['date', 'time','mode','code','amount','price','money']) 
        self.trade_df =self.trade_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        self.security_df = pd.DataFrame(columns = ['code','amount','price','money']) 
        self.security_df =self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  

    def PrintOrder(self): #输出下单流水
        print(self.order_df)

    def PrintTrade(self): #输出交易流水
        print(self.trade_df)

    def PrintSecurity(self): #输出持仓清单
        print(self.security_df)

    def Order(self,date,time,mode,code,amount,price): #交易函数
        ln=len(self.order_df)
        df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,'price':price},index=[ln])
        self.order_df=self.order_df.append( df_new,ignore_index=True)

        ln=len(self.trade_df)
        if mode==1:   #买入
            se=amount*price*(1+self.trading_Commission)
            self.money=self.money-se
            df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,'price':price,'money':self.money},index=[ln])
            self.trade_df=self.trade_df.append( df_new,ignore_index=True)
            if len(self.security_df[self.security_df.code==code])==0 :
                df_new = pd.DataFrame({'code':code,'amount':amount,'price':se/amount,'money':se},index=[ln])
                self.security_df=self.security_df.append( df_new,ignore_index=True)
            else:
                self.security_df.index=self.security_df['code']
                self.security_df.loc[code,'amount']=self.security_df.loc[code,'amount']+amount
                self.security_df=self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        
        ln=len(self.security_df[self.security_df.code==code])
        if mode==2 and ln>0:  #卖出
            self.security_df.index=self.security_df['code']
            am=self.security_df.loc[code,'amount']
            
            if am<amount :
                amount=am
            se=amount*price*(1-self.trading_Commission-self.stamp_duty)
            self.money=self.money+se
            df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,'price':price,'money':self.money},index=[ln])
            self.trade_df=self.trade_df.append( df_new,ignore_index=True)
            am2=self.security_df.loc[code,'amount']-amount
            self.security_df.loc[code,'amount']=am2
            if am2==0:
                self.security_df=self.security_df.drop(code, axis = 0) # 在行的维度上删除行
            self.security_df=self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  


#####################回测功能#########################
    def Trade_testing(self,df,tp1,tp2,al=''):   #回测函数
        self.Init()
        self.trade=True   #允许交易
        myMoney=self.money2
        if (al.strip()==''):
            na='property'
        else:
            na=al 
        self.text='    ----开始回测-----\n'
        i = 0  
        ZB_l = []
        while i < len(df):  
            close=df.close.at[i]
            if (df[tp1].at[i] >0 and self.position==False and self.trade==True) :  #买点
                self.priceBuy=close
                x=int(myMoney/(self.priceBuy*(1+self.trading_Commission))/100)
                self.amount=x*100.00
                self.Order(df.date.at[i],'14:45:01',1,self.code,self.amount,close)
                myMoney=myMoney-self.amount*self.priceBuy*(1.00+self.trading_Commission)
                self.position=True
                self.priceStopLoss=self.priceBuy*(1-self.stop_loss_range)
                self.text=self.text+'日期:'+df.date.at[i]+' 买入:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceBuy,2))+'\n'
            
            if (df[tp2].at[i] >0 and self.position==True and self.trade==True) : #卖点
                self.priceSell=close
                myMoney=myMoney+self.amount*self.priceSell*(1.00-self.trading_Commission-self.stamp_duty)
                self.position=False
                self.Order(df['date'].at[i],'14:45:02',2,self.code,self.amount,self.priceSell)
                self.text=self.text+'日期:'+df.date.at[i]+' 卖出:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceSell,2))+'获利:'+str(round((myMoney-self.money2)/self.money2*100,2))+'%\n'
                self.amount=0.00
            
            if (close<=self.priceStopLoss and self.position==True and self.trade  and self.stop_loss_on):  #止损
                self.priceSell=self.priceStopLoss-0.01
                myMoney=myMoney+self.amount*self.priceSell*(1.00-self.trading_Commission-self.stamp_duty)
                self.position=False
                self.stop_loss_num=self.stop_loss_num+1
                self.Order(df['date'].at[i],'14:45:02',2,self.code,self.amount,self.priceSell)
                self.text=self.text+'日期:'+df.date.at[i]+' 止损:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceSell,2))+'获利:'+str(round((myMoney-self.money2)/self.money2*100,2))+'%\n'
                self.amount=0.00
                if (self.stop_loss_num>=self.stop_loss_max):
                    self.trade=False

            y= (myMoney+self.amount*close-self.money2)/self.money2 *100 
            ZB_l.append(y)  
            i = i + 1          
            
        ZB_s = pd.Series(ZB_l)  
        ZB = pd.Series(ZB_s, name = na)  
        df = df.join(ZB)  
        self.money=myMoney
        y= (myMoney+self.amount*close-self.money2)/self.money2  *100
        self.text=self.text+'总投入'+str(round(self.money2,2))+',最终获利幅度'+str(round(y,0))+'%\n'
            
        return df


#交易回测类
class Trade_T60(object):
    def __init__(self): #类初始化
        self.order_df=None   #下单流水
        self.trade_df=None   #交易流水
        self.security_df=None   #持仓清单
        self.money2=10000000.00  #总资金
        self.money=10000000.00  #资金
        self.priceBuy=0.00    #最后一次买入价格
        self.priceSell=999999.00  #最后一次卖出价格
        self.amount=0.00   #证券数量
        self.code=""   #证券代码
        self.stamp_duty=0.001   #印花税 0.1%
        self.trading_Commission=0.0005    #交易佣金0.05%
        self.priceStopLoss=0.00   #止损价
        self.position=False   #持仓状态
        self.stop_loss_on=True #允许止损
        self.stop_loss_num=0   #当前止损次数
        self.stop_loss_max=50 #最大允许止损次数.到止损次数,就停止交易
        self.stop_loss_range=0.05   #止损幅度
        self.trade=True   #允许交易
        self.st=0
        self.money3=self.money2
        self.Init()

    def Init(self): #初始化交易数据
        self.order_df = pd.DataFrame(columns = ['date', 'time','mode','code','amount','price']) 
        self.order_df =self.order_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        self.trade_df = pd.DataFrame(columns = ['date', 'time','mode','code','amount','price','money','amount2','money2']) 
        self.trade_df =self.trade_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        self.security_df = pd.DataFrame(columns = ['code','amount','price','money']) 
        self.security_df =self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        self.rate_df= pd.DataFrame(columns = ['date', 'close','refclose','money','shouyi','total']) 
        self.rate_df =self.rate_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  

    def PrintOrder(self): #输出下单流水
        print(self.order_df)

    def PrintTrade(self): #输出交易流水
        print(self.trade_df)

    def PrintSecurity(self): #输出持仓清单
        print(self.security_df)

    def Order(self,date,time,mode,code,amount,price): #交易函数
        ln=len(self.order_df)
        df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,'price':price},index=[ln])
        self.order_df=self.order_df.append( df_new,ignore_index=True)

        ln=len(self.trade_df)
        if mode==1:   #买入
            se=amount*price*(1+self.trading_Commission)
            self.money=self.money-se
            self.money3=self.money+amount*price
            df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,\
                                   'price':price,'money':self.money,'amount2':amount,'money2':self.money3},index=[ln])
            self.trade_df=self.trade_df.append( df_new,ignore_index=True)
            if len(self.security_df[self.security_df.code==code])==0 :
                df_new = pd.DataFrame({'code':code,'amount':amount,'price':se/amount,'money':se},index=[ln])
                self.security_df=self.security_df.append( df_new,ignore_index=True)
            else:
                self.security_df.index=self.security_df['code']
                self.security_df.loc[code,'amount']=self.security_df.loc[code,'amount']+amount
                self.security_df=self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        
        ln=len(self.security_df[self.security_df.code==code])
        if mode==2 and ln>0:  #卖出
            self.security_df.index=self.security_df['code']
            am=self.security_df.loc[code,'amount']
            
            if am<amount :
                amount=am
            se=amount*price*(1-self.trading_Commission-self.stamp_duty)
            self.money=self.money+se
            self.money3=self.money
            df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,\
                                   'price':price,'money':self.money,'amount2':0,'money2':self.money3},index=[ln])
            self.trade_df=self.trade_df.append( df_new,ignore_index=True)
            am2=self.security_df.loc[code,'amount']-amount
            self.security_df.loc[code,'amount']=am2
            if am2==0:
                self.security_df=self.security_df.drop(code, axis = 0) # 在行的维度上删除行
            self.security_df=self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  


#####################回测功能#########################
    def Trade_testing(self,df,tp1,tp2,al=''):   #回测函数
        self.Init()
        self.trade=True   #允许交易
        myMoney=self.money2
        if (al.strip()==''):
            na='property'
        else:
            na=al 
        self.text='    ----开始回测-----\n'
        i = 0  
        ZB_l = []
        while i < len(df):  
            close=df.close.at[i]
            if (df[tp1].at[i] >0 and self.position==False and self.trade==True) :  #买点
                self.st=1
                self.priceBuy=close
                x=int(myMoney/(self.priceBuy*(1+self.trading_Commission))/100)
                self.amount=x*100.00
                self.Order(df.date.at[i],'',1,self.code,self.amount,close)
                myMoney=myMoney-self.amount*self.priceBuy*(1.00+self.trading_Commission)
                self.position=True
                self.priceStopLoss=self.priceBuy*(1-self.stop_loss_range)
                self.text=self.text+'日期:'+df.date.at[i]+' 买入:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceBuy,2))+'\n'
                self.st=0
            
            elif (df[tp2].at[i] >0 and self.position==True and self.trade==True) : #卖点
                self.st=2
                self.priceSell=close
                myMoney=myMoney+self.amount*self.priceSell*(1.00-self.trading_Commission-self.stamp_duty)
                self.position=False
                self.Order(df['date'].at[i],'',2,self.code,self.amount,self.priceSell)
                self.text=self.text+'日期:'+df.date.at[i]+' 卖出:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceSell,2))+'获利:'+str(round((myMoney-self.money2)/self.money2*100,2))+'%\n'
                self.amount=0.00
                self.st=0
            
            elif (close<=self.priceStopLoss and self.position==True and self.trade  and self.stop_loss_on):  #止损
                self.st=3
                self.priceSell=self.priceStopLoss-0.01
                myMoney=myMoney+self.amount*self.priceSell*(1.00-self.trading_Commission-self.stamp_duty)
                self.position=False
                self.stop_loss_num=self.stop_loss_num+1
                self.Order(df['date'].at[i],'',2,self.code,self.amount,self.priceSell)
                self.text=self.text+'日期:'+df.date.at[i]+' 止损:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceSell,2))+'获利:'+str(round((myMoney-self.money2)/self.money2*100,2))+'%\n'
                self.amount=0.00
                if (self.stop_loss_num>=self.stop_loss_max):
                    self.trade=False
                self.st=0
            
            else:
                self.st=0
                #Order(self,date,time,mode,code,amount,price): #交易函数
                ln=len(self.trade_df)
                df_new = pd.DataFrame({'date':df['date'].at[i],'time':'','mode':0,'code':self.code,'amount':self.amount,'price':close,\
                                       'money':myMoney,'amount2':self.amount,'money2':self.money3},index=[ln])
                self.trade_df=self.trade_df.append( df_new,ignore_index=True)


            y= (myMoney+self.amount*close-self.money2)/self.money2 *100 
            ZB_l.append(y)  
            i = i + 1          
            
        ZB_s = pd.Series(ZB_l)  
        ZB = pd.Series(ZB_s, name = na)  
        df = df.join(ZB)  
        self.money=myMoney
        y= (myMoney+self.amount*close-self.money2)/self.money2  *100
        self.text=self.text+'总投入'+str(round(self.money2,2))+',最终获利幅度'+str(round(y,0))+'%\n'
            
        return df



#####################################################


#交易回测类
class Trade_T0(object):
    def __init__(self): #类初始化
        self.order_df=None   #下单流水
        self.trade_df=None   #交易流水
        self.security_df=None   #持仓清单
        self.money2=0.00  #总资金
        self.money=0.00  #资金
        self.priceBuy=0.00    #最后一次买入价格
        self.priceSell=999999.00  #最后一次卖出价格
        self.amount=0.00   #证券数量
        self.code=""   #证券代码
        self.stamp_duty=0.001   #印花税 0.1%
        self.trading_Commission=0.0005    #交易佣金0.05%
        self.priceStopLoss=0.00   #止损价
        self.position=False   #持仓状态
        self.stop_loss_on=True #允许止损
        self.stop_loss_num=0   #当前止损次数
        self.stop_loss_max=50 #最大允许止损次数.到止损次数,就停止交易
        self.stop_loss_range=0.05   #止损幅度
        self.trade=True   #允许交易
        self.bnum=4   #允许每天买次数
        self.snum=4   #允许每天卖次数
        self.total_money=0  #总资金
        #持股2/3仓
        self.hold_stock_amount=0
        #记录初始持股数
        self.original_hold_stock_amount=0
        #每笔交易股数（总股数的1/10）,并取100整数倍
        self.trade_amount=0
        #现金1/3仓 
        self.hold_money=0
        #记录初始现金
        self.original_hold_money=0
        self.amount2=0 #证券数量变化
        self.firstclose=0
        self.money4=0
        self.money5=0
        self.rate_df=None
        
        self.Init()

    def Init(self): #初始化交易数据
        self.order_df = pd.DataFrame(columns = ['date', 'time','mode','code','amount','price']) 
        self.order_df =self.order_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        self.trade_df = pd.DataFrame(columns = ['date', 'time','mode','code','amount','price','money']) 
        self.trade_df =self.trade_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        self.security_df = pd.DataFrame(columns = ['code','amount','price','money']) 
        self.security_df =self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        self.rate_df= pd.DataFrame(columns = ['date', 'close','refclose','money','shouyi','total']) 
        self.rate_df =self.rate_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  

    def PrintOrder(self): #输出下单流水
        print(self.order_df)

    def PrintTrade(self): #输出交易流水
        print(self.trade_df)

    def PrintSecurity(self): #输出持仓清单
        print(self.security_df)

    def Order(self,date,time,mode,code,amount,price): #交易函数
        ln=len(self.order_df)
        df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,'price':price},index=[ln])
        self.order_df=self.order_df.append( df_new,ignore_index=True)

        ln=len(self.trade_df)
        if mode==1:   #买入
            se=amount*price*(1+self.trading_Commission)
            self.money=self.money-se
            df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,'price':price,'money':self.money},index=[ln])
            self.trade_df=self.trade_df.append( df_new,ignore_index=True)
            if len(self.security_df[self.security_df.code==code])==0 :
                df_new = pd.DataFrame({'code':code,'amount':amount,'price':se/amount,'money':se},index=[ln])
                self.security_df=self.security_df.append( df_new,ignore_index=True)
            else:
                self.security_df.index=self.security_df['code']
                self.security_df.loc[code,'amount']=self.security_df.loc[code,'amount']+amount
                self.security_df=self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        
        ln=len(self.security_df[self.security_df.code==code])
        if mode==2 and ln>0:  #卖出
            self.security_df.index=self.security_df['code']
            am=self.security_df.loc[code,'amount']
            
            if am<amount :
                amount=am
            se=amount*price*(1-self.trading_Commission-self.stamp_duty)
            self.money=self.money+se
            df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,'price':price,'money':self.money},index=[ln])
            self.trade_df=self.trade_df.append( df_new,ignore_index=True)
            am2=self.security_df.loc[code,'amount']-amount
            self.security_df.loc[code,'amount']=am2
            if am2==0:
                self.security_df=self.security_df.drop(code, axis = 0) # 在行的维度上删除行
            self.security_df=self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  


#####################回测功能#########################
    def Trade_testing(self,df,tp1,tp2,al='',c=0.00):   #回测函数
        self.Init()
        self.trade=True   #允许交易
        if len(df)==0:
            return df
        if (al.strip()==''):
            na='property'
        else:
            na=al 
        self.text='    ----开始回测-----\n'
        self.bnum=4   #允许每天买次数
        self.snum=4   #允许每天卖次数
        #i = 0  
        i = df.index[0]
        close=df.close[i]-df.price_change[i]
        if c==0.00:
            self.firstclose=close
        else:
            self.firstclose=c

        self.amount=40000
        self.trade_amount=10000

        self.money3=0  #现金差初值
        self.amount2=0
        self.money4=0
        self.money5=0
        self.lastclose=close
        
        self.hl=0
        ZB_l = []
        ZB_p=[]
        m=i+len(df)
        day2=df.date.at[0]
        day2=day2[0:11]
        ra=[]
        rb=[]
        rc=[]
        rd=[]
        re=[]
        rf=[]
        while i < m:  
            #print('i=',i,df)
            date=df.date.at[i]
            close=df.close.at[i]
            nowtime=df.date.at[i]
            nowtime=nowtime[11:]
            day=df.date.at[i]
            day=day[0:11]
            #print(nowtime)
            if nowtime=='9:35:00' or nowtime=='09:35:00' or nowtime=='09:35' or nowtime=='9:35':
                day2=day
                self.money4=0
#            if nowtime=='09:35' :
#                self.firstclose=close
            if nowtime!='15:00' and nowtime!='15:00:00' :
                if (df[tp1].at[i] >0 and self.bnum>0) :  #买点
                    self.priceBuy=close
                    self.Order(df.date.at[i],nowtime,1,self.code,self.trade_amount,self.priceBuy)
                    myMoney=self.trade_amount*self.priceBuy*(1.00+self.trading_Commission)
                    #self.priceStopLoss=self.priceBuy*(1-self.stop_loss_range)
                    self.text=self.text+'日期:'+df.date.at[i]+' 买入:'+str(round(self.trade_amount,0))+'股, 价格:'+str(round(self.priceBuy,2))+'\n'
                    self.amount2=self.amount2+self.trade_amount
                    self.amount=self.amount+self.trade_amount
                    self.bnum=self.bnum-1
                    self.money3=self.money3-myMoney
                    self.money4=self.money4-myMoney
                
                if (df[tp2].at[i] >0 and self.trade==True and self.snum>0) : #卖点
                    self.priceSell=close
                    if self.amount>=self.trade_amount:
                        myMoney=self.trade_amount*self.priceSell*(1.00-self.trading_Commission-self.stamp_duty)
                        self.Order(df['date'].at[i],nowtime,2,self.code,self.trade_amount,self.priceSell)
                        self.text=self.text+'日期:'+df.date.at[i]+' 卖出:'+str(round(self.trade_amount,0))+'股, 价格:'+str(round(self.priceSell,2))+'\n'
                        self.amount=self.amount-self.trade_amount
                        self.amount2=self.amount2-self.trade_amount
                        self.snum=self.snum-1
                        self.money3=self.money3+myMoney
                        self.money4=self.money4+myMoney
            else:
                if (self.amount2>0):  #需要卖出
                    self.priceSell=close
                    amount=self.amount2
                    myMoney=amount*self.priceSell*(1.00-self.trading_Commission-self.stamp_duty)
                    self.Order(df['date'].at[i],nowtime,2,self.code,amount,self.priceSell)
                    self.text=self.text+'日期:'+df.date.at[i]+' 平仓卖出:'+str(round(amount,0))+'股, 价格:'+str(round(self.priceSell,2))+'\n'
                    self.amount=self.amount-amount
                    self.amount2=0
                    self.money3=self.money3+myMoney
                    self.money4=self.money4+myMoney
                    
                elif (self.amount2<0):  #需要买入
                    self.priceBuy=close
                    amount=-self.amount2
                    self.trade_money=amount*self.priceBuy*(1.00+self.trading_Commission)
                    self.Order(df.date.at[i],nowtime,1,self.code,amount,close)
                    myMoney=amount*self.priceBuy*(1.00+self.trading_Commission)
                    #self.priceStopLoss=self.priceBuy*(1-self.stop_loss_range)
                    self.text=self.text+'日期:'+df.date.at[i]+' 平仓买入:'+str(round(amount,0))+'股, 价格:'+str(round(self.priceBuy,2))+'\n'
                    self.amount2=0
                    self.amount=self.amount+amount
                    self.money3=self.money3-myMoney
                    self.money4=self.money4-myMoney
                self.bnum=4   #允许每天买次数
                self.snum=4   #允许每天卖次数
                # ['date', 'close','refclose','money','shouyi']
                ra.append(date)
                rb.append(close)
                rc.append(self.lastclose)
                rd.append(self.money4)
                if self.money4>0:
                    yy=1
                elif self.money4<0:
                    yy=-1
                else:
                    yy=0
                re.append(yy)
                rf.append(self.money3)
                self.lastclose=close
                day2=""
                #y2= (myMoney-self.money3)/self.money3 *100 
                #ZB_l.append(y2)  
            #y= (myMoney+self.amount*close-self.money2)/self.money2 *100 
            if day2!=day and day2!='':
                if self.amount2!=0:
                    print(day2,day)
                    print('分时线不完整!',nowtime,self.amount2)
                    day2=day
                else:
                    day2=day
                    
            y= self.money3/(self.firstclose *40000)
            ZB_l.append(y)
            ZB_p.append(self.money3)
            self.hl=y
            i = i + 1          
#            if nowtime=='15:00' :
#                self.money3=0
            
        ZB_s = pd.Series(ZB_l)  
        ZB = pd.Series(ZB_s, name = na)  
        df = df.join(ZB) 
        
        ZB_s2 = pd.Series(ZB_p)  
        ZB2 = pd.Series(ZB_s2, name ='money')  
        df = df.join(ZB2)
        #self.money=myMoney
        #y= (myMoney+self.amount*close-self.money2)/self.money2  *100
        #self.text=self.text+'总投入'+str(round(self.money2,2))+',最终获利幅度'+str(round(y,0))+'%\n'
        #['date', 'close','refclose','money','shouyi']
        df_new = pd.DataFrame({'date':ra,'close':rb,'refclose':rc,'money':rd,'shouyi':re,'total':rf})
        self.rate_df= df_new
        #print(self.rate_df)  
        return df
    
    
#交易回测类
class hpQuant(object):
    def __init__(self): #类初始化
        self.order_df=None   #下单流水
        self.trade_df=None   #交易流水
        self.security_df=None   #持仓清单
        self.money2=1000000.00  #总资金
        self.money=1000000.00  #资金
        self.priceBuy=0.00    #最后一次买入价格
        self.priceSell=999999.00  #最后一次卖出价格
        self.amount=0.00   #证券数量
        self.code=""   #证券代码
        self.stamp_duty=0.001   #印花税 0.1%
        self.trading_Commission=0.0005    #交易佣金0.05%
        self.priceStopLoss=0.00   #止损价
        self.position=False   #持仓状态
        self.stop_loss_on=True #允许止损
        self.stop_loss_num=0   #当前止损次数
        self.stop_loss_max=50 #最大允许止损次数.到止损次数,就停止交易
        self.stop_loss_range=0.05   #止损幅度
        self.trade=True   #允许交易
        self.Init()

    def Init(self): #初始化交易数据
        self.order_df = pd.DataFrame(columns = ['date', 'time','mode','code','amount','price']) 
        self.order_df =self.order_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        self.trade_df = pd.DataFrame(columns = ['date', 'time','mode','code','amount','price','money']) 
        self.trade_df =self.trade_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        self.security_df = pd.DataFrame(columns = ['code','amount','price','money']) 
        self.security_df =self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  

    def PrintOrder(self): #输出下单流水
        print(self.order_df)

    def PrintTrade(self): #输出交易流水
        print(self.trade_df)

    def PrintSecurity(self): #输出持仓清单
        print(self.security_df)

    def Order(self,date,time,mode,code,amount,price): #交易函数
        ln=len(self.order_df)
        df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,'price':price},index=[ln])
        self.order_df=self.order_df.append( df_new,ignore_index=True)

        ln=len(self.trade_df)
        if mode==1:   #买入
            se=amount*price*(1+self.trading_Commission)
            self.money=self.money-se
            df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,'price':price,'money':self.money},index=[ln])
            self.trade_df=self.trade_df.append( df_new,ignore_index=True)
            if len(self.security_df[self.security_df.code==code])==0 :
                df_new = pd.DataFrame({'code':code,'amount':amount,'price':se/amount,'money':se},index=[ln])
                self.security_df=self.security_df.append( df_new,ignore_index=True)
            else:
                self.security_df.index=self.security_df['code']
                self.security_df.loc[code,'amount']=self.security_df.loc[code,'amount']+amount
                self.security_df=self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        
        ln=len(self.security_df[self.security_df.code==code])
        if mode==2 and ln>0:  #卖出
            self.security_df.index=self.security_df['code']
            am=self.security_df.loc[code,'amount']
            
            if am<amount :
                amount=am
            se=amount*price*(1-self.trading_Commission-self.stamp_duty)
            self.money=self.money+se
            df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,'price':price,'money':self.money},index=[ln])
            self.trade_df=self.trade_df.append( df_new,ignore_index=True)
            am2=self.security_df.loc[code,'amount']-amount
            self.security_df.loc[code,'amount']=am2
            if am2==0:
                self.security_df=self.security_df.drop(code, axis = 0) # 在行的维度上删除行
            self.security_df=self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  


#####################回测功能#########################
    def Trade_testing(self,df,tp1,tp2,al=''):   #回测函数
        self.Init()
        self.trade=True   #允许交易
        myMoney=self.money2
        if (al.strip()==''):
            na='property'
        else:
            na=al 
        self.text='    ----开始回测-----\n'
        i = 0  
        ZB_l = []
        while i < len(df):  
            close=df.close.at[i]
            if (df[tp1].at[i] >0 and self.position==False and self.trade==True) :  #买点
                self.priceBuy=close
                x=int(myMoney/(self.priceBuy*(1+self.trading_Commission))/100)
                self.amount=x*100.00
                self.Order(df.date.at[i],'14:45:01',1,self.code,self.amount,close)
                myMoney=myMoney-self.amount*self.priceBuy*(1.00+self.trading_Commission)
                self.position=True
                self.priceStopLoss=self.priceBuy*(1-self.stop_loss_range)
                self.text=self.text+'日期:'+df.date.at[i]+' 买入:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceBuy,2))+'\n'
            
            if (df[tp2].at[i] >0 and self.position==True and self.trade==True) : #卖点
                self.priceSell=close
                myMoney=myMoney+self.amount*self.priceSell*(1.00-self.trading_Commission-self.stamp_duty)
                self.position=False
                self.Order(df['date'].at[i],'14:45:02',2,self.code,self.amount,self.priceSell)
                self.text=self.text+'日期:'+df.date.at[i]+' 卖出:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceSell,2))+'获利:'+str(round((myMoney-self.money2)/self.money2*100,2))+'%\n'
                self.amount=0.00
            
            if (close<=self.priceStopLoss and self.position==True and self.trade  and self.stop_loss_on):  #止损
                self.priceSell=self.priceStopLoss-0.01
                myMoney=myMoney+self.amount*self.priceSell*(1.00-self.trading_Commission-self.stamp_duty)
                self.position=False
                self.stop_loss_num=self.stop_loss_num+1
                self.Order(df['date'].at[i],'14:45:02',2,self.code,self.amount,self.priceSell)
                self.text=self.text+'日期:'+df.date.at[i]+' 止损:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceSell,2))+'获利:'+str(round((myMoney-self.money2)/self.money2*100,2))+'%\n'
                self.amount=0.00
                if (self.stop_loss_num>=self.stop_loss_max):
                    self.trade=False

            y= (myMoney+self.amount*close-self.money2)/self.money2 *100 
            ZB_l.append(y)  
            i = i + 1          
            
        ZB_s = pd.Series(ZB_l)  
        ZB = pd.Series(ZB_s, name = na)  
        df = df.join(ZB)  
        self.money=myMoney
        y= (myMoney+self.amount*close-self.money2)/self.money2  *100
        self.text=self.text+'总投入'+str(round(self.money2,2))+',最终获利幅度'+str(round(y,0))+'%\n'
            
        return df
################独狼荷蒲软件版权声明###################
'''
独狼荷蒲软件(或通通软件)版权声明
1、独狼荷蒲软件(或通通软件)均为软件作者设计,或开源软件改进而来，仅供学习和研究使用，不得用于任何商业用途。
2、用户必须明白，请用户在使用前必须详细阅读并遵守软件作者的“使用许可协议”。
3、作者不承担用户因使用这些软件对自己和他人造成任何形式的损失或伤害。
4、作者拥有核心算法的版权，未经明确许可，任何人不得非法复制；不得盗版。作者对其自行开发的或和他人共同开发的所有内容，
    包括设计、布局结构、服务等拥有全部知识产权。没有作者的明确许可，任何人不得作全部或部分复制或仿造。

独狼荷蒲软件
QQ: 2775205
Tel: 18578755056
公众号:独狼股票分析
'''