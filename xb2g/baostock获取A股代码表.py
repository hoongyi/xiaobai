# -*- coding: utf-8 -*-
# xbdata股票代码表下载
# 2022年04月04日
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts
import baostock as bs

def IF(COND, V1, V2):
    var = np.where(COND, V1, V2)
    return pd.Series(var)


filename='./data/all_stock.csv'
#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)
 
#### 获取证券信息 ####
rs = bs.query_all_stock(day="2023-02-10")
print('query_all_stock respond error_code:'+rs.error_code)
print('query_all_stock respond  error_msg:'+rs.error_msg)
 
#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
dmb = pd.DataFrame(data_list, columns=rs.fields)

dmb['code2']=dmb['code']
dmb['code']=[x[3:] for x in dmb.code2.astype(str)]
dmb['market2']=[x[0:2] for x in dmb.code2.astype(str)]
dmb['market']=IF(dmb['market2']=='sz',0,1)


dmb['type']=''
dmb['kind']=''
dmb['type2']=10
for i in range(len(dmb)):
    mk=int(dmb['market'][i])
    x=int(dmb['code'][i])
    if mk==0:
        if x<2000:
            dmb.loc[i,'type']='证券'
            dmb.loc[i,'kind']='A股股票'
            dmb.loc[i,'type2']=1
        elif x>=2000 and x<31000:
            dmb.loc[i,'type']='证券'
            dmb.loc[i,'kind']='中小板'
            dmb.loc[i,'type2']=2
        elif x>=31000 and x<80000:
            dmb.loc[i,'type']='证券'
            dmb.loc[i,'kind']='权证'
            dmb.loc[i,'type2']=8
        elif x>=80000 and x<100000:
            dmb.loc[i,'type']='证券'
            dmb.loc[i,'kind']='配股'
            dmb.loc[i,'type2']=1
        elif x>=100000 and x<150000:
            dmb.loc[i,'type']='证券'    
            dmb.loc[i,'kind']='债券'
            dmb.loc[i,'type2']=6
        elif x>=150000 and x<200000:
            dmb.loc[i,'type']='证券'
            dmb.loc[i,'kind']='基金'   
            dmb.loc[i,'type2']=7
        elif x>=200000 and x<300000:
            dmb.loc[i,'type']='证券'
            dmb.loc[i,'kind']='B股股票'
            dmb.loc[i,'type2']=5
        elif x>=300000 and x<380000:
            dmb.loc[i,'type']='证券'
            dmb.loc[i,'kind']='创业板'
            dmb.loc[i,'type2']=3
        elif x>=390000 and x<400000:
            dmb.loc[i,'type']='指数板块'
            dmb.loc[i,'kind']='指数'         
            dmb.loc[i,'type2']=0
        elif x>=400000 and x<500000:
            dmb.loc[i,'type']='证券'
            dmb.loc[i,'kind']='三板'  
            dmb.loc[i,'type2']=1            
        elif x>=500000 and x<600000:
            dmb.loc[i,'type']='证券'
            dmb.loc[i,'kind']='基金'    
            dmb.loc[i,'type2']=7
        elif x>=600000 and x<800000:
            dmb.loc[i,'type']='证券'
            dmb.loc[i,'kind']='A股股票'  
            dmb.loc[i,'type2']=1
        elif x>=800000 and x<900000:
            dmb.loc[i,'type']='指数板块'
            dmb.loc[i,'kind']='板块'       
            dmb.loc[i,'type2']=0
        elif x>=900000 and x<999000:
            dmb.loc[i,'type']='证券'
            dmb.loc[i,'kind']='B股股票'  
            dmb.loc[i,'type2']=5
        elif x>=999000 :
            dmb.loc[i,'type']='指数板块'  
            dmb.loc[i,'kind']='指数'  
            dmb.loc[i,'type2']=0
    elif mk==1:
        if x<1000:
            dmb.loc[i,'type']='指数板块'
            dmb.loc[i,'kind']='指数'
            dmb.loc[i,'type2']=0
        elif x>=1000 and x<30000:
            dmb.loc[i,'type']='证券'
            dmb.loc[i,'kind']='债券'
            dmb.loc[i,'type2']=6
        elif x>=30000 and x<200000:
            dmb.loc[i,'type']='证券'  
            dmb.loc[i,'kind']='债券'  
            dmb.loc[i,'type2']=6
        elif x>=200000 and x<500000:
            dmb.loc[i,'type']='证券'              
            dmb.loc[i,'kind']='债券'  
            dmb.loc[i,'type2']=6
        elif x>=500000 and x<600000:
            dmb.loc[i,'type']='证券'       
            dmb.loc[i,'kind']='基金'
            dmb.loc[i,'type2']=7
        elif x>=600000 and x<688000:
            dmb.loc[i,'type']='证券'  
            dmb.loc[i,'kind']='A股股票'  
            dmb.loc[i,'type2']=1
        elif x>=688000 and x<700000:
            dmb.loc[i,'type']='证券'
            dmb.loc[i,'kind']='科创版'  
            dmb.loc[i,'type2']=1              
        elif x>=700000 and x<750000:
            dmb.loc[i,'type']='证券'  
            dmb.loc[i,'kind']='新股申购'  
            dmb.loc[i,'type2']=1
        elif x>=750000 and x<800000:
            dmb.loc[i,'type']='其他'  
            dmb.loc[i,'kind']='其他'  
            dmb.loc[i,'type2']=9
        elif x>=800000 and x<900000:
            dmb.loc[i,'type']='指数板块'              
            dmb.loc[i,'kind']='板块'
            dmb.loc[i,'type2']=0
        elif x>=900000 and x<999000:
            dmb.loc[i,'type']='证券'  
            dmb.loc[i,'kind']='B股股票'  
            dmb.loc[i,'type2']=5
        elif x>=999000 :
            dmb.loc[i,'type']='指数板块'  
            dmb.loc[i,'kind']='指数'  
            dmb.loc[i,'type2']=0


#### 结果集输出到csv文件 ####   
dmb.to_csv(filename, encoding="gbk", index=False)
print(dmb)
 
#### 登出系统 ####
bs.logout()


