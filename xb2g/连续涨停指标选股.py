#小白量化选股 :连续涨停指标选股

#购买<零基础搭建量化投资系统>正版书,送小白量化软件源代码。
# https://item.jd.com/61567375505.html
#独狼荷蒲qq:2775205
#通通python量化群:524949939
#电话微信:18578755056
#微信公众号：独狼股票分析
#日期:2021-01-09
import time
import HP_tdx as htdx
from HP_formula import *

global CLOSE,LOW,HIGH,OPEN,VOL
global C,L,H,O,V

hq=htdx.TdxInit(ip='183.60.224.178',port=7709)  ##初始化通达信
#codes=htdx.getblock2('沪深300') #返回板块中的股票
bkn='近期强势'
codes=htdx.getblock2(bkn) #返回板块中的股票

#code='600655'
#bk=htdx.getblock3(code)
#print(code,' 所属板块 :',bk)

print('小白量化选股: 连续涨停指标选股')
print('输出股票池或板块中股票')
print(bkn,' 板块中股票 :',codes)

#均线选股函数
def function(cd):
    global CLOSE,LOW,HIGH,OPEN,VOL
    global C,L,H,O,V

    df3=htdx.get_security_bars(nCategory=4,nMarket = 0,code=cd,\
                    nStart=0, nCount=500) #获取指定范围的证券K线
    
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

    C1=REF(CLOSE,1);
    A1=IF(CLOSE>=HIGH,1,0)*IF((CLOSE-C1)/C1>=0.099,1,0);
    A2=SUM(A1,2);
    A3=IF(REF(A2,1)>=2,1,0);

    B2=list(A3)
    if B2[len(B2)-1]==1:
        return 1
    else:
        return 0
    

#下面开始进行板块或股票池选股
myblock=[]  #选股池
start = time.time()
for code in codes:
     buy=function(code)  #计算股票选股函数
     if buy==1:
         myblock.append(code)

print('输出选出的股票池')
print(myblock)
end=time.time()
print('时间:',round(start,2),round(end,2),round(end-start,2),'秒')