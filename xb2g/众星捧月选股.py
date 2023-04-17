#众星捧月选股
# MA5:=EMA(C,5);
# MA10:=EMA(C,10);
# MV5:=EMA(V,5);
# MV10:=EMA(V,10);
# K:="KDJ.K"(9,3,3);
# D:="KDJ.D"(9,3,3);
# DIF:=EMA(CLOSE,12)-EMA(CLOSE,26);
# DEA:=EMA(DIF,9);
# MACD1:=DIF>REF(DIF,1) AND DEA>=REF(DEA,1) AND DIF>DEA;
# V1:=MA5>REF(MA5,1) AND MA10>REF(MA10,1) AND C>REF(C,1) AND
# C/O>1.01;
# VV1:=MV5>REF(MV5,1) AND MV10>=REF(MV10,1) AND V>REF(V,1)*1.2 ;
# KD1:=K>REF(K,1) AND D>=REF(D,1);
# VA:=COUNT(CROSS(K,D),4)>=1 AND COUNT(CROSS(MA5,MA10),4)>=1 AND
# COUNT(CROSS(MV5,MV10),4)>=1 AND COUNT(CROSS(DIF,DEA),4)>=1;
# XG2:IF(V1 AND VV1 AND KD1 AND MACD1 AND VA,1,0);

#日期:2023-02-06
import time
import HP_tdx as htdx
from HP_formula import *

hq=htdx.TdxInit(ip='183.60.224.178',port=7709)  ##初始化通达信
#codes=htdx.getblock2('沪深300') #返回板块中的股票
shCodes = htdx.get_A_stocks()
codes=set(shCodes['code'])
print('众星捧月选股')
print('输出股票池中股票')
print(shCodes[['code','name']])

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

    MA5 = EMA(C, 5)
    MA10 = EMA(C, 10)
    MV5 = EMA(V, 5)
    MV10 = EMA(V, 10)
    K,D = ZST_KD(CLOSE,LOW,HIGH,9, 3, 3)
    DIF = EMA(CLOSE, 12) - EMA(CLOSE, 26)
    DEA = EMA(DIF, 9)
    MACD1 = AND(AND(DIF > REF(DIF, 1), (DEA >= REF(DEA, 1))),(DIF > DEA))
    V1 = AND(AND(AND((MA5 > REF(MA5, 1)), (MA10 > REF(MA10, 1))), (C > REF(C, 1))), (C / O > 1.01))
    VV1 = AND(AND(MV5 > REF(MV5, 1), MV10 >= REF(MV10, 1)), V > REF(V, 1) * 1.2)
    KD1 = AND(K > REF(K, 1), D >= REF(D, 1))
    VA = AND(AND(AND(COUNT(CROSS(K, D), 4) >= 1, COUNT(CROSS(MA5, MA10), 4) >= 1), COUNT(CROSS(MV5, MV10), 4) >= 1), COUNT(CROSS(DIF, DEA), 4) >= 1)
    #XG2 = IF(AND(AND(AND(AND(V1, VV1), KD1), MACD1), VA), 1, 0)
    XG2 = V1+VV1+KD1+MACD1+VA
    B2 = list(XG2)
    lastN = len(B2) - 1
    if lastN > 0 and B2[lastN] >= 5:
        return 1
    else:
        return 0
import easytrader
ths = easytrader.use('ths')
ths.connect("C:\\同花顺软件\\同花顺\\xiadan.exe")
ths.enable_type_keys_for_editor()
print(ths.balance)
print('选出的股票')
#下面开始进行板块或股票池选股
myblock=[]  #选股池
start = time.time()
for code in codes:
    try:
        buy=function(code)  #计算股票选股函数
        if buy==1:
            print(code,shCodes[shCodes['code']==code])
            ths.buy(code, price=C.iloc[-1], amount=500)
            myblock.append(code)
    except:
        print('e')

# for stock in myblock:
#     try:
#         ths.buy(code, price=C.iloc[-1], amount=500)
#     except:
#         print('e')

print('输出选出的股票池')
print(myblock)
end=time.time()
print('时间:',round(start,2),round(end,2),round(end-start,2),'秒')