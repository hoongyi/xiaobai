#购买<零基础搭建量化投资系统>正版书,送小白量化软件源代码。
# https://item.jd.com/61567375505.html
#独狼荷蒲qq:2775205
#通通python量化群:524949939
#电话微信:18578755056
#微信公众号：独狼股票分析
from HP_formula import *  #小白量化仿通达信公式函数库
import HP_tdx as htdx  #小白量化通达信行情库

#KDJ指标
def KDJ(N=9, M1=3, M2=3):
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = SMA(RSV,M1,1)
    D = SMA(K,M2,1)
    J = 3*K-2*D
    return K, D, J

#RSI指标
def RSI(N1=5):
    LC = REF(CLOSE, 1)
    RSI1 = SMA(MAX(CLOSE - LC, 0), N1, 1) / SMA(ABS(CLOSE - LC), N1, 1) * 100.00
    return RSI1

def VR(M1=26):
    """
    VR容量比率
    """
    LC = REF(CLOSE, 1)
    VR = SUM(IF(CLOSE > LC, VOL, 0), M1) / SUM(IF(CLOSE <= LC, VOL, 0), M1) * 100
    return VR

def ARBR(M1=26):
    """
    ARBR人气意愿指标
    """
    AR = SUM(HIGH - OPEN, M1) / SUM(OPEN - LOW, M1) * 100
    BR = SUM(MAX(0, HIGH - REF(CLOSE, 1)), M1) / SUM(MAX(0, REF(CLOSE, 1) - LOW), M1) * 100
    return AR, BR

def DMI(M1=14, M2=6):
    """
    DMI 趋向指标
    """
    TR = SUM(MAX(MAX(HIGH - LOW, ABS(HIGH - REF(CLOSE, 1))), ABS(LOW - REF(CLOSE, 1))), M1)
    HD = HIGH - REF(HIGH, 1)
    LD = REF(LOW, 1) - LOW

    DMP = SUM(IF((HD > 0) & (HD > LD), HD, 0), M1)
    DMM = SUM(IF((LD > 0) & (LD > HD), LD, 0), M1)
    DI1 = DMP * 100 / TR
    DI2 = DMM * 100 / TR
    ADX = MA(ABS(DI2 - DI1) / (DI1 + DI2) * 100, M2)
    ADXR = (ADX + REF(ADX, M2)) / 2

    return DI1, DI2, ADX, ADXR

#连接行情主站
htdx.TdxInit(ip='183.60.224.178',port=7709)
code='600080'
#获取日线数据,800条数据
df = htdx. get_security_bars(nCategory=4,nMarket = 0,code=code,nCount=800)

#对数据做小白量化格式转换
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

#自编防通达信技术指标计算
mydf['ema5']=EMA(C,5)  #5日均线
mydf['k'],mydf['d'],mydf['j']=KDJ()  #kdj指标
mydf['rsi']=RSI()   #rsi指标
mydf['vr']=VR()   #VR指标
mydf['ar'],mydf['br']=ARBR()  #ARBR指标
mydf['di1'],mydf['di2'],mydf['adx'],mydf['adxr']=DMI()  #DMI指标


#设置涨跌标签
mydf['label']=IF(C>REF(C,1),1.0,0.0)   #判断当日上涨或不上张
mydf['label2']=REF(mydf['label'],-1)  #把下一周期的上涨移动到前一周期,用于学习标签

print(mydf)
mydf=mydf.tail(100)


x_all = []     #定义两个列表变量
y_all = []

#装配深度网络学习数据
for i in range(0,len(mydf)-1):
    features = []
    features.append(mydf['open'].iloc[i]) 
    features.append(mydf['high'].iloc[i]) 
    features.append(mydf['low'].iloc[i]) 
    features.append(mydf['close'].iloc[i]) 
    features.append(mydf['ema5'].iloc[i]) 
    features.append(mydf['rsi'].iloc[i])
    features.append(mydf['k'].iloc[i])
    features.append(mydf['d'].iloc[i])
    features.append(mydf['j'].iloc[i])
    features.append(mydf['vr'].iloc[i])
    features.append(mydf['ar'].iloc[i])
    features.append(mydf['br'].iloc[i])
    features.append(mydf['di1'].iloc[i])
    features.append(mydf['di2'].iloc[i])
    features.append(mydf['adx'].iloc[i])
    features.append(mydf['adxr'].iloc[i])
    
    x_all.append(features)
    #前一天数据，标记下一天涨跌      
    y_all.append(mydf['label2'].iloc[i])
    

# 准备神经网络算法需要用到的数据,截取前790条做神经网络学习，后10条进行验证效果。
x_train = x_all[: -10]
y_train = y_all[: -10]

print('神经网络数据已准备好了！')


#保存训练后模型
import joblib

#导入支持向量机(SVM)
from sklearn import svm
#开始利用支持向量机(SVM)机器学习算法计算
clf = svm.SVC()
#训练的代码
print('神经网络开始数据学习!')
clf.fit(x_train, y_train)

#保存训练后的模型
joblib.dump(clf, "svm.m")
print('神经网络学习结束!')
#对训练结果进行检验

#加载训练后的模型
clf2 = joblib.load("svm.m")

#后20条数据做神经网络测试集
print('向量机(SVM)预测结果如下(前10条已学习过,后10条数据未学习.):')
M=20
for i in range(M):
    x_test = x_all[i-M]
    y_test = y_all[i-M]
    prediction = clf2.predict([x_test])
    mess='预测错误！'
    if prediction == y_test :
        mess="预测正确！"
    print(i+1,' : ',y_test,prediction,mess)