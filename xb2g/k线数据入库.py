

#日期:2023-02-13
import time
import HP_tdx as htdx
from HP_formula import *
from sqlalchemy import create_engine
import pymysql
from sqlalchemy.types import VARCHAR

hq=htdx.TdxInit(ip='183.60.224.178',port=7709)  ##初始化通达信
shCodes = htdx.get_A_stocks()
codes=set(shCodes['code'])
print('股票个数:',len(codes))

engine = create_engine('mysql+pymysql://root:zhang137@macbook:3306/hq?charset=utf8')

#选股函数
def function(cd):
    global CLOSE, LOW, HIGH, OPEN, VOL
    global C, L, H, O, V
    df3=htdx.get_security_bars(nCategory=4,nMarket = -1,code=cd,\
                    nStart=0, nCount=100) #获取指定范围的证券K线
    if df3.empty:
       # print(cd)
        return 0
    ##数据规格化 
    df3.dropna(inplace=True)
    df3.to_sql(f'kline', engine, if_exists='append', index=False, dtype={'code':VARCHAR(length=6)})
    return 1

myblock=[]  #选股池
start = time.time()
for code in codes:
    try:
        buy=function(code)  #计算股票选股函数
        if buy==1:
            print(code,shCodes[shCodes['code']==code])
            myblock.append(code)
    except:
        print('e'+code)



print('输出更新的股票池:',len(myblock))
print(myblock)
end=time.time()
print('时间:',round(start,2),round(end,2),round(end-start,2),'秒')