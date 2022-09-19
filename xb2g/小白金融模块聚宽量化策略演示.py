#购买<零基础搭建量化投资系统>正版书,送小白量化软件源代码。
# https://item.jd.com/61567375505.html
#独狼荷蒲qq:2775205
#小白python量化群: 524949939
#小白python量化群2: 983815766
#电话微信:18578755056
#微信公众号：独狼股票分析

# 导入函数库
from jqdata import *
import pandas as pd  
import numpy  as np

##小白量化股票数据格式同ts旧版数据格式
## jqtots来源HP_data
def jqtots(df1):  #聚宽格式转ts格式
    a=[x.strftime("%Y-%m-%d") for x in df1.index]
    df1.insert(0,'date',a)
    df1=df1.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    return df1

global CLOSE,LOW,HIGH,OPEN,VOL
##从小白量化公式函数库中复制.
## 函数来源 HP_formula
def MA(Series, N):
    return pd.Series.rolling(Series, N).mean()

def HHV(Series, N=0):
    if N==0:
        return Series.cummax()
    else:
        return pd.Series(Series).rolling(N).max()

def LLV(Series, N=0):
    if N==0:
        return Series.cummin()
    else:
        return pd.Series(Series).rolling(N).min()

def EMA(Series, N):
    var=pd.Series.ewm(Series, span=N, min_periods=N - 1, adjust=True).mean()
    if N>0:
        var[0]=0
        #y=0
        a=2.00000000/(N+1)
        for i in range(1,N):
            y=pd.Series.ewm(Series, span=i, min_periods=i - 1, adjust=True).mean()
            y1=a*Series[i]+(1-a)*y[i-1]
            var[i]=y1
    return var

def CROSS(A, B):
    A2=np.array(A)
    var = np.where(A2<B, 1, 0)
    return (pd.Series(var, index=A.index).diff()<0).apply(int)
       
##下面开始写用户自编股票公式
def KDJ(N=9, M1=3, M2=3):
    global CLOSE,LOW,HIGH,OPEN,VOL
    """
    KDJ 随机指标
    """
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = EMA(RSV, (M1 * 2 - 1))
    D = EMA(K, (M2 * 2 - 1))
    J = K * 3 - D * 2
    return K, D, J


# 初始化函数，设定基准等等
def initialize(context):
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    # 输出内容到日志 log.info()
    log.info('初始函数开始运行且全局只运行一次')
    # 过滤掉order系列API产生的比error级别低的log
    # log.set_level('order', 'error')

    ### 股票相关设定 ###
    # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')

    ## 运行函数（reference_security为运行时间的参考标的；传入的标的只做种类区分，因此传入'000300.XSHG'或'510300.XSHG'是一样的）
      # 开盘前运行
    run_daily(before_market_open, time='before_open', reference_security='000300.XSHG')
      # 开盘时运行
    run_daily(market_open, time='open', reference_security='000300.XSHG')
      # 收盘后运行
    run_daily(after_market_close, time='after_close', reference_security='000300.XSHG')

## 开盘前运行函数
def before_market_open(context):
    # 输出运行时间
    log.info('函数运行时间(before_market_open)：'+str(context.current_dt.time()))

    # 给微信发送消息（添加模拟交易，并绑定微信生效）
    # send_message('美好的一天~')

    # 要操作的股票：（g.为全局变量）
    g.security = '600519.XSHG'

## 开盘时运行函数
def market_open(context):
    global CLOSE,LOW,HIGH,OPEN,VOL
    current_date = context.current_dt.date()
    # 取得当前的现金
    cash = context.portfolio.available_cash
    log.info('函数运行时间(market_open):'+str(context.current_dt.time()))
    security = g.security
    # 获取股票的收盘价
    df = get_price(security, start_date='2020-11-01', end_date=current_date, fields=['open', 'close', 'low', 'high', 'volume'])
    mydf=jqtots(df)
    CLOSE=mydf['close']
    LOW=mydf['low']
    HIGH=mydf['high']
    OPEN=mydf['open']
    VOL=mydf['volume']
    mydf['s80']=80
    
    k,d,j=KDJ()
    mydf['k']=k
    mydf['d']=d
    mydf['j']=k
    
    mydf['buy']=CROSS(k,d)   #k上穿d
    mydf['sell']=CROSS(mydf['s80'],k)  #k下穿80
    log.info(mydf)
    buy=list(mydf['buy'])
    sell=list(mydf['sell'])
    if buy[-1]>0:
        log.info('买')
    if sell[-1]>0:
        log.info('卖')

    # 如果上一时间点价格高出五天平均价1%, 则全仓买入
    if (buy[-1]>0) and (cash > 0):
        # 记录这次买入
        log.info("价格高于均价 1%%, 买入 %s" % (security))
        # 用所有 cash 买入股票
        order_value(security, cash)
    # 如果上一时间点价格低于五天平均价, 则空仓卖出
    elif (sell[-1]>0) and context.portfolio.positions[security].closeable_amount > 0:
        # 记录这次卖出
        log.info("价格低于均价, 卖出 %s" % (security))
        # 卖出所有股票,使这只股票的最终持有量为0
        order_target(security, 0)


## 收盘后运行函数
def after_market_close(context):
    log.info(str('函数运行时间(after_market_close):'+str(context.current_dt.time())))
    #得到当天所有成交记录
    trades = get_trades()
    for _trade in trades.values():
        log.info('成交记录：'+str(_trade))
    log.info('一天结束')
    log.info('##############################################################')
