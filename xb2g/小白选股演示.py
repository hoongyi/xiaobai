#小白量化选股 

import HP_tdx as htdx
from HP_formula import *

global CLOSE,LOW,HIGH,OPEN,VOL
global C,L,H,O,V

hq=htdx.TdxInit(ip='183.60.224.178',port=7709)  ##初始化通达信
codes=htdx.getblock2('上证50') #返回板块中的股票
print('小白量化选股: 5日均线上传20日均线')
print('输出股票池或板块中股票')
print(codes)

#均线选股函数
def function(cd):
    global CLOSE,LOW,HIGH,OPEN,VOL
    global C,L,H,O,V

    df3=htdx.get_security_bars(nCategory=4,nMarket = 0,code=cd,\
                    nStart=0, nCount=40) #获取指定范围的证券K线
    
    ##数据规格化 
    df3.dropna(inplace=True)
    #小白数据规格化
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
    #仿通达信，大智慧公式计算和选股
    MA5=MA(CLOSE,5)
    MA20=MA(CLOSE,20)
    B=CROSS(MA5,MA20)   #5日均线上传20日均线
    B2=list(B)
    return B2[len(B2)-1]
    

#下面开始进行板块或股票池选股
myblock=[]  #选股池
for code in codes:
     buy=function(code)  #计算股票选股函数
     if buy==1:
         myblock.append(code)

print('输出选出的股票池')
print(myblock)

