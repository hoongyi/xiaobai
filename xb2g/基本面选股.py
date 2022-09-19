#小白量化选股 :基本面指标选股

#购买<零基础搭建量化投资系统>正版书,送小白量化软件源代码。
# https://item.jd.com/61567375505.html
#独狼荷蒲qq:2775205
#通通python量化群:524949939
#电话微信:18578755056
#微信公众号：独狼股票分析
#日期:2021-01-09
import time
import HP_tdx as htdx
import HP_tdxgs as hgs
from HP_formula import *

global CLOSE,LOW,HIGH,OPEN,VOL
global C,L,H,O,V


'''
财务函数
FINANCE(1)　　　总股本（万股）
FINANCE(2)　　　市场类型
FINANCE(3)　　　沪深品种类型
FINANCE(4)　　　沪深品种通达信二级行业代码
FINANCE(5)　　　B股（万股）
FINANCE(6)　　　H股（万股）
FINANCE(7)　　　流通股本（万股）
CAPITAL　　　　流通股本（手）
FINANCE(8)   股东人数(户)(上市公司的最新数据)
FINANCE(9)   资产负债率
FINANCE(10) 总资产
FINANCE(11) 流动资产
FINANCE(12) 固定资产
FINANCE(13) 无形资产
FINANCE(14) 长期投资
FINANCE(15) 流动负债
FINANCE(16) 　　长期负债
FINANCE(17) 　　资本公积金金
FINANCE(18) 每股公积金金
FINANCE(19) 　　股东权益
FINANCE(20) 　　主营收入
FINANCE(21) 　　主营利利益
FINANCE(22) 　　其它利利益
FINANCE(23) 　　营业利利益
FINANCE(24) 　　投资收益
FINANCE(25) 　　补贴收入
FINANCE(26) 　　营业外收支
FINANCE(27) 　　上年年损益调整
FINANCE(28)　　利利益总额
FINANCE(29) 　　税后利利益
FINANCE(30) 　　净利利益
FINANCE(31) 　　未分配利利益
FINANCE(32) 每股未分配利利润
FINANCE(33) 每股收益
FINANCE(34) 　每股净资产
FINANCE(35)　　调整每股净资产
FINANCE(36) 　股东权益比
FINANCE(40) 流通市值
FINANCE(41) 总市值
FINANCE(42) 上市日期
'''

def FINANCE(x):
    return hgs.FINANCE(x)

#CAPITAL　　　　流通股本（手）
def CAPITAL():
    return hgs.Capital


hq=htdx.TdxInit(ip='183.57.72.22',port=7709)  ##初始化通达信

bkn='沪深300'
codes=htdx.getblock2(bkn) #返回板块中的股票


print('小白量化选股: 基本面指标选股')
print('输出股票池或板块中股票')
print(bkn,len(codes),' 板块中股票 :',codes)

#均线选股函数
def function(cd):
    global CLOSE,LOW,HIGH,OPEN,VOL
    global C,L,H,O,V
    
    #获取通达信财物数据
    #nMarket = get_market(cd)
    hgs.readbase(htdx.get_market(cd),cd)
    df3=htdx.get_security_bars(nCategory=4,nMarket = htdx.get_market(cd),code=cd,\
                    nStart=0, nCount=10) #获取指定范围的证券K线
    
    ##数据规格化 
    df3.dropna(inplace=True)
    #小白数据规格化
    mydf=df3.copy()
    CLOSE=mydf['close']
    LOW=mydf['low']
    HIGH=mydf['high']
    OPEN=mydf['open']
    VOL=mydf['volume']/100  #通达信软件是手
    C=mydf['close']
    L=mydf['low']
    H=mydf['high']
    O=mydf['open']
    V=mydf['volume']/100  #通达信软件是手
    

    #仿通达信，大智慧公式计算和选股
    A1=SUM(VOL,5);
    A2=IF(A1/CAPITAL()*100>15,1,0);
    A3=IF(CLOSE/FINANCE(33)>1,1,0)*IF(CLOSE/FINANCE(33)<50,1,0);
    AX=IF(A2+A3>=2,1,0);

    #转化为买点信号
    B2=list(AX)
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

print('输出选出的股票池',len(myblock))
print(myblock)
end=time.time()
print('时间:',round(start,2),round(end,2),round(end-start,2),'秒')