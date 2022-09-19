# -*- coding: utf-8 -*-
"""
#仿通达新大智慧公式基础库  Ver1.00
#版本：Ver1.04
#设计人：独狼荷蒲
#电话:18578755056
#QQ：2775205
#百度：荷蒲指标
#开始设计日期: 2018-07-08
#公众号:独狼股票分析
#使用者请同意最后<版权声明>
#最后修改日期:2021年12月17日
#主程序：HP_main.py
*********************************************
通达信公式转为python公式的过程
1.‘:=’为赋值语句，用程序替换‘:=’为python的赋值命令‘=。
2.‘:’为公式的赋值带输出画线命令，再替换‘:’为‘=’，‘:’前为输出变量，顺序写到return 返回参数中。
3.全部命令转为英文大写。
4.删除绘图格式命令。
5.删除掉每行未分号; 。
6.参数可写到函数参数表中.例如: def KDJ(N=9, M1=3, M2=3):

例如通达信 KDJ指标公式描述如下。
参数表 N:=9, M1:=3, M2:=3
RSV:=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100;
K:SMA(RSV,M1,1);
D:SMA(K,M2,1);
J:3*K-2*D;

def KDJ(N=9, M1=3, M2=3):
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = EMA(RSV, (M1 * 2 - 1))
    D = EMA(K, (M2 * 2 - 1))
    J = 3*K-2*D
    return K, D, J
###################基本函数库##############################
"""
import os
import math
import datetime as dt
import time
import pandas as pd  
import numpy  as np

global CODE,DATE,TIME,INDEX
global CLOSE,LOW,HIGH,OPEN,VOL,AMO
global C,L,H,O,V,mydf,LEN

def LTON(a):
    b=a
    if str(b.dtype)=='bool':
        var = np.where(b, 1, 0)
    else:
        var =b
    return pd.Series(var)

def WEEKDAY():
    now = dt.datetime.now()
    return now.weekday()

#取得当前客户端机器为星期几(1,2,3,4,5,6,0)
def MACHINEWEEK():
    return dt.datetime.now().weekday()    

#取得当前客户端机器从1900以来的的年月日,
def MACHINEDATE():
    today=dt.date.today()   #获取今天日期
    date=today.year*10000+today.month*100+today.day-19000000
    return date

#取得当前客户端机器的时间,比如11:01:15时为110115
def MACHINETIME():
    today=dt.datetime.now()
    time2=today.hour*10000+today.minute*100+today.second
    return time2

def initmydf(df):
    global CODE,DATE,TIME,INDEX
    global CLOSE,LOW,HIGH,OPEN,VOL,AMO
    global C,L,H,O,V,mydf,LEN
    mydf=df.copy()
    LEN=len(mydf)
    for s in mydf.columns:
        mydf[s.lower()]=mydf[s]
    CLOSE=mydf['close']
    LOW=mydf['low']
    HIGH=mydf['high']
    OPEN=mydf['open']
    C=CLOSE
    L=LOW
    H=HIGH
    O=OPEN
    if 'datetime' in  mydf.columns:
        mydf['date']=mydf.datetime
    if 'vol' in  mydf.columns:
        mydf['volume']=mydf.vol
        VOL=mydf['volume']
        V=mydf['volume']
    if 'volume' in  mydf.columns:
        mydf['vol']=mydf['volume']
    if 'amount' in  mydf.columns:
        mydf['amo']=mydf.amount
        AMO=mydf['amo']
    if 'time' in  mydf.columns:
        TIME=mydf.time
    if 'date' in  mydf.columns:
        DATE=mydf.date
    if 'code' in  mydf.columns:
        CODE=mydf.code
    print(mydf)
    mydf['rtn']=100*(mydf['close']-REF(mydf['close'],1))/mydf['close']   #收益率，又称回报率
    mydf['vwap']=SUM(mydf['close']*mydf['vol'], 10)/SUM(mydf['vol'], 10)  #成交量加权平均价        
    INDEX=mydf.index
    return mydf

##转换为pd.Series
def nSeries(s):
    global LEN
    if isinstance(s, np.ndarray):
        return pd.Series(s)
    elif isinstance(s, list):
        return pd.Series(s)
    elif isinstance(s, float) or isinstance(s,int):
        return pd.Series([s+x*0 for x in range(LEN)])

def REFDATE(x,d):
    global CODE,DATE,TIME,INDEX
    global CLOSE,LOW,HIGH,OPEN,VOL,AMO
    global C,L,H,O,V,mydf,LEN        
    try:
        f=x[mydf.date==d].iat[0]
        return f
    except:
        return np.nan
       
def REFDATE2(x,d):
    global CODE,DATE,TIME,INDEX
    global CLOSE,LOW,HIGH,OPEN,VOL,AMO
    global C,L,H,O,V,mydf,LEN    
    try:    
        d1=1900+int(d/10000)
        d2=int((d-int(d/10000)*10000)/100)
        d3=int((d-int(d/10000)*10000-d2*100))
        ds='%4d-%02d-%02d'%(d1,d2,d3)
        f=x[mydf.date==ds].iat[0]
        return f
    except:
        return np.nan    
    
class HSeries(pd.Series):
    def __init__(self,**kw):
       super.__init__(**kw)


#列表扩展
def Listexpand(List,n):
    Lista=[]
    for x in List:
        for i in range(n):
            Lista.append(x)
    return Lista

#列表扩展
def Seriesexpand(Series,n):
    Lista=[]
    for x in list(Series):
        for i in range(n):
            Lista.append(x)
    return pd.Series(Lista)
     


def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]


# DATE=Date(date)
def Date(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        d=(100+int(s[2:4]))*10000+int(s[5:7])*100+int(s[8:10])
        ret.append(d)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

# YEAR=Year(date)
def Year(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        d=int(s[0:4])
        ret.append(d)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

# MONTH =Month(date)
def Month(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        d=int(s[5:7])
        ret.append(d)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

def Week(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        t1=dt.datetime.strptime(s[0:10],"%Y-%m-%d")
        w2=dt.date.weekday(t1)
        ret.append(w2)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)    

    
# DAY=Day(date)
def Day(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        d=int(s[8:10])
        ret.append(d)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

# TIME=Time(date)    
def Time(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        t=int(s[-5:-3])*100+int(s[-2:])
        ret.append(t)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

# HOUR =  Hour(date):
def Hour(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        t=int(s[-5:-3])*100+int(s[-2:])
        ret.append(t)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

# MINUTE=Minute(date)
def MINUTE(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        t=int(s[-5:-3])*100+int(s[-2:])
        ret.append(t)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

def FROMOPEN():
    d1=time.strftime("%Y-%m-%d",time.localtime(time.time()))+' 09:30:01.001'
    d3=dt.datetime.strptime(todayopen,"%Y-%m-%d %H:%M:%S.%f")
    d2 = dt.datetime.now()
    return int((d2-d3).seconds/60)

##########################
#杂函数
#判断是否是英文句子
def isenglish(ss):
    result=True
    for c in ss.lower():
        if c in "abcdefghijklmnopqrstuvwxyz,.' !?":
            continue 
        result=False
        break
    return result

def CODE(code):
    code=code.strip()
    if isenglish(code)==True or len(code)==0:
        ret_=0
    else:
        ret_=int(code)
    return ret_


def get_names():
    names={}
    codes=[]
    names2=[]
    if (os.path.isfile('./names.csv'))==True:
        base=pd.read_csv('./names.csv' , encoding= 'gbk')
        codes2=list(base.code)
        names2=list(base.name)
        i=0
        for code in codes2:
            codes.append(code[1:])
            names.update({code[1:]:names2[i]})
            i+=1
    return names,codes

def STKNAME(code):
    names,codes=get_names()
    if code in codes:
        ret_=names[code]
    else:
        ret_=''
    return ret_
    
# 算农历日期
g_lunar_month_day = [
	0x00752, 0x00ea5, 0x0ab2a, 0x0064b, 0x00a9b, 0x09aa6, 0x0056a, 0x00b59, 0x04baa, 0x00752, # 1901 ~ 1910 
	0x0cda5, 0x00b25, 0x00a4b, 0x0ba4b, 0x002ad, 0x0056b, 0x045b5, 0x00da9, 0x0fe92, 0x00e92, # 1911 ~ 1920 
	0x00d25, 0x0ad2d, 0x00a56, 0x002b6, 0x09ad5, 0x006d4, 0x00ea9, 0x04f4a, 0x00e92, 0x0c6a6, # 1921 ~ 1930 
	0x0052b, 0x00a57, 0x0b956, 0x00b5a, 0x006d4, 0x07761, 0x00749, 0x0fb13, 0x00a93, 0x0052b, # 1931 ~ 1940 
	0x0d51b, 0x00aad, 0x0056a, 0x09da5, 0x00ba4, 0x00b49, 0x04d4b, 0x00a95, 0x0eaad, 0x00536, # 1941 ~ 1950 
	0x00aad, 0x0baca, 0x005b2, 0x00da5, 0x07ea2, 0x00d4a, 0x10595, 0x00a97, 0x00556, 0x0c575, # 1951 ~ 1960 
	0x00ad5, 0x006d2, 0x08755, 0x00ea5, 0x0064a, 0x0664f, 0x00a9b, 0x0eada, 0x0056a, 0x00b69, # 1961 ~ 1970 
	0x0abb2, 0x00b52, 0x00b25, 0x08b2b, 0x00a4b, 0x10aab, 0x002ad, 0x0056d, 0x0d5a9, 0x00da9, # 1971 ~ 1980 
	0x00d92, 0x08e95, 0x00d25, 0x14e4d, 0x00a56, 0x002b6, 0x0c2f5, 0x006d5, 0x00ea9, 0x0af52, # 1981 ~ 1990 
	0x00e92, 0x00d26, 0x0652e, 0x00a57, 0x10ad6, 0x0035a, 0x006d5, 0x0ab69, 0x00749, 0x00693, # 1991 ~ 2000 
	0x08a9b, 0x0052b, 0x00a5b, 0x04aae, 0x0056a, 0x0edd5, 0x00ba4, 0x00b49, 0x0ad53, 0x00a95, # 2001 ~ 2010 
	0x0052d, 0x0855d, 0x00ab5, 0x12baa, 0x005d2, 0x00da5, 0x0de8a, 0x00d4a, 0x00c95, 0x08a9e, # 2011 ~ 2020 
	0x00556, 0x00ab5, 0x04ada, 0x006d2, 0x0c765, 0x00725, 0x0064b, 0x0a657, 0x00cab, 0x0055a, # 2021 ~ 2030 
	0x0656e, 0x00b69, 0x16f52, 0x00b52, 0x00b25, 0x0dd0b, 0x00a4b, 0x004ab, 0x0a2bb, 0x005ad, # 2031 ~ 2040 
	0x00b6a, 0x04daa, 0x00d92, 0x0eea5, 0x00d25, 0x00a55, 0x0ba4d, 0x004b6, 0x005b5, 0x076d2, # 2041 ~ 2050 
	0x00ec9, 0x10f92, 0x00e92, 0x00d26, 0x0d516, 0x00a57, 0x00556, 0x09365, 0x00755, 0x00749, # 2051 ~ 2060 
	0x0674b, 0x00693, 0x0eaab, 0x0052b, 0x00a5b, 0x0aaba, 0x0056a, 0x00b65, 0x08baa, 0x00b4a, # 2061 ~ 2070 
	0x10d95, 0x00a95, 0x0052d, 0x0c56d, 0x00ab5, 0x005aa, 0x085d5, 0x00da5, 0x00d4a, 0x06e4d, # 2071 ~ 2080 
	0x00c96, 0x0ecce, 0x00556, 0x00ab5, 0x0bad2, 0x006d2, 0x00ea5, 0x0872a, 0x0068b, 0x10697, # 2081 ~ 2090 
	0x004ab, 0x0055b, 0x0d556, 0x00b6a, 0x00752, 0x08b95, 0x00b45, 0x00a8b, 0x04a4f, ]
 
 
#农历数据 每个元素的存储格式如下： 
#    12~7         6~5    4~0  
#  离元旦多少天  春节月  春节日  
#####################################################################################
g_lunar_year_day = [
	0x18d3, 0x1348, 0x0e3d, 0x1750, 0x1144, 0x0c39, 0x15cd, 0x1042, 0x0ab6, 0x144a, # 1901 ~ 1910 
	0x0ebe, 0x1852, 0x1246, 0x0cba, 0x164e, 0x10c3, 0x0b37, 0x14cb, 0x0fc1, 0x1954, # 1911 ~ 1920 
	0x1348, 0x0dbc, 0x1750, 0x11c5, 0x0bb8, 0x15cd, 0x1042, 0x0b37, 0x144a, 0x0ebe, # 1921 ~ 1930 
	0x17d1, 0x1246, 0x0cba, 0x164e, 0x1144, 0x0bb8, 0x14cb, 0x0f3f, 0x18d3, 0x1348, # 1931 ~ 1940 
	0x0d3b, 0x16cf, 0x11c5, 0x0c39, 0x15cd, 0x1042, 0x0ab6, 0x144a, 0x0e3d, 0x17d1, # 1941 ~ 1950 
	0x1246, 0x0d3b, 0x164e, 0x10c3, 0x0bb8, 0x154c, 0x0f3f, 0x1852, 0x1348, 0x0dbc, # 1951 ~ 1960 
	0x16cf, 0x11c5, 0x0c39, 0x15cd, 0x1042, 0x0a35, 0x13c9, 0x0ebe, 0x17d1, 0x1246, # 1961 ~ 1970 
	0x0d3b, 0x16cf, 0x10c3, 0x0b37, 0x14cb, 0x0f3f, 0x1852, 0x12c7, 0x0dbc, 0x1750, # 1971 ~ 1980 
	0x11c5, 0x0c39, 0x15cd, 0x1042, 0x1954, 0x13c9, 0x0e3d, 0x17d1, 0x1246, 0x0d3b, # 1981 ~ 1990 
	0x16cf, 0x1144, 0x0b37, 0x144a, 0x0f3f, 0x18d3, 0x12c7, 0x0dbc, 0x1750, 0x11c5, # 1991 ~ 2000 
	0x0bb8, 0x154c, 0x0fc1, 0x0ab6, 0x13c9, 0x0e3d, 0x1852, 0x12c7, 0x0cba, 0x164e, # 2001 ~ 2010 
	0x10c3, 0x0b37, 0x144a, 0x0f3f, 0x18d3, 0x1348, 0x0dbc, 0x1750, 0x11c5, 0x0c39, # 2011 ~ 2020 
	0x154c, 0x0fc1, 0x0ab6, 0x144a, 0x0e3d, 0x17d1, 0x1246, 0x0cba, 0x15cd, 0x10c3, # 2021 ~ 2030 
	0x0b37, 0x14cb, 0x0f3f, 0x18d3, 0x1348, 0x0dbc, 0x16cf, 0x1144, 0x0bb8, 0x154c, # 2031 ~ 2040 
	0x0fc1, 0x0ab6, 0x144a, 0x0ebe, 0x17d1, 0x1246, 0x0cba, 0x164e, 0x1042, 0x0b37, # 2041 ~ 2050 
	0x14cb, 0x0fc1, 0x18d3, 0x1348, 0x0dbc, 0x16cf, 0x1144, 0x0a38, 0x154c, 0x1042, # 2051 ~ 2060 
	0x0a35, 0x13c9, 0x0e3d, 0x17d1, 0x11c5, 0x0cba, 0x164e, 0x10c3, 0x0b37, 0x14cb, # 2061 ~ 2070 
	0x0f3f, 0x18d3, 0x12c7, 0x0d3b, 0x16cf, 0x11c5, 0x0bb8, 0x154c, 0x1042, 0x0ab6, # 2071 ~ 2080 
	0x13c9, 0x0e3d, 0x17d1, 0x1246, 0x0cba, 0x164e, 0x10c3, 0x0bb8, 0x144a, 0x0ebe, # 2081 ~ 2090 
	0x1852, 0x12c7, 0x0d3b, 0x16cf, 0x11c5, 0x0c39, 0x154c, 0x0fc1, 0x0a35, 0x13c9, # 2091 ~ 2100 
	]
 
START_YEAR = 1901
month_DAY_BIT = 12
month_NUM_BIT = 13 
#　todo：正月初一 == 春节   腊月二十九/三十 == 除夕
yuefeng = ["正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "冬月", "腊月"]
riqi = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "廿十",
    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
 
xingqi = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
xingqi2 = ["星期日","星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
tiangan   = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
dizhi     = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
shengxiao = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
 
# 节气名称组
jieqi = [
    "小寒", "大寒",  # 1月        
    "立春", "雨水",  # 2月
    "惊蛰", "春分",  # 3月
    "清明", "谷雨",  # 4月
    "立夏", "小满",  # 5月
    "芒种", "夏至",  # 6月
    "小暑", "大暑",  # 7月
    "立秋", "处暑",  # 8月
    "白露", "秋分",  # 9月
    "寒露", "霜降",  # 10月
    "立冬", "小雪",  # 11月
    "大雪", "冬至"]  # 12月

# 节气日期
jieqi2 = [
    5, 20,  # 1月        
    3,18,  # 2月
    5, 20,  # 3月
    4, 20,  # 4月
    5, 21,  # 5月
    5, 21,  # 6月
    7, 22,  # 7月
    7, 23,  # 8月
    7, 23,  # 9月
    8, 23,  # 10月
    7, 22,  # 11月
    7, 22]  # 12月


 ## 特殊年份特殊节气进行纠正
def rectify_year(year,m,day):
    day2=day
    cday=''
    m=m-1
    jq1=2*m
    jq2=2*m+1
    
    day=jieqi[jq1]
 
    if day2==jieqi2[jq1]:
        cday=jieqi[jq1]
    if day2==jieqi2[jq2]:
        cday=jieqi[jq2]
    return cday
 
def change_year(num):
    dx = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
    tmp_str = ""
    for i in str(num):
        tmp_str += dx[int(i)]
    return tmp_str
 
def week_str(tm):
    return xingqi[tm.weekday()]
 
def lunar_day(day):
    return riqi[(day - 1) % 30]
 
def lunar_day1(month, day):
    if day == 1:
        return lunar_month(month)
    else:
        return riqi[day - 1]
 
def lunar_month(month):
    leap = (month>>4)&0xf
    m = month&0xf
    month = yuefeng[(m - 1) % 12]
    if leap == m:
        month = "闰" + month
    return month
 
def lunar_year(year):
    return tiangan[(year - 4) % 10] + dizhi[(year - 4) % 12] + '[' + shengxiao[(year - 4) % 12] + ']'
 
# 返回：
# a b c
# 闰几月，该闰月多少天 传入月份多少天
def lunar_month_days(lunar_year, lunar_month):
    if (lunar_year < START_YEAR):
        return 30
 
    leap_month, leap_day, month_day = 0, 0, 0 # 闰几月，该月多少天 传入月份多少天
 
    tmp = g_lunar_month_day[lunar_year - START_YEAR]
 
    if tmp & (1<<(lunar_month-1)):
        month_day = 30
    else:
        month_day = 29
 
    # 闰月
    leap_month = (tmp >> month_NUM_BIT) & 0xf
    if leap_month:
        if (tmp & (1<<month_DAY_BIT)):
            leap_day = 30
        else:
            leap_day = 29
 
    return (leap_month, leap_day, month_day)
# 返回的月份中，高4bit为闰月月份，低4bit为其它正常月份
def get_ludar_date(tm):
    year, month, day = tm.year, 1, 1
    code_data = g_lunar_year_day[year - START_YEAR]
    days_tmp = (code_data >> 7) & 0x3f
    chunjie_d = (code_data >> 0) & 0x1f
    chunjie_m = (code_data >> 5) & 0x3
    span_days = (tm - dt.datetime(year, chunjie_m, chunjie_d)).days
    #print("span_day: ", days_tmp, span_days, chunjie_m, chunjie_d)
 
    # 日期在该年农历之后
    if (span_days >= 0):
        (leap_month, foo, tmp) = lunar_month_days(year, month)
        while span_days >= tmp:
            span_days -= tmp
            if (month == leap_month):
                (leap_month, tmp, foo) = lunar_month_days(year, month) # 注：tmp变为闰月日数
                if (span_days < tmp): # 指定日期在闰月中
                    month = (leap_month<<4) | month
                    break
                span_days -= tmp
            month += 1 # 此处累加得到当前是第几个月
            (leap_month, foo, tmp) = lunar_month_days(year, month)
        day += span_days
        return year, month, day
    # 倒算日历
    else:
        month = 12
        year -= 1
        (leap_month, foo, tmp) = lunar_month_days(year, month)
        while abs(span_days) >= tmp:
            span_days += tmp
            month -= 1
            if (month == leap_month):
                (leap_month, tmp, foo) = lunar_month_days(year, month)
                if (abs(span_days) < tmp): # 指定日期在闰月中
                    month = (leap_month<<4) | month
                    break
                span_days += tmp
            (leap_month, foo, tmp) = lunar_month_days(year, month)
        day += (tmp + span_days) # 从月份总数中倒扣 得到天数
        return year, month, day

def CWEEK(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        t1=dt.datetime.strptime(s[0:10],"%Y-%m-%d")
        w2=dt.date.weekday(t1)
        ret.append(xingqi2(w2))
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)    


def LYEAR(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        y=int(s[0:4])
        m=int(s[5:7])
        d=int(s[8:10])
        tmp = dt.datetime(y, m, d)
        y2,m2,d2=get_ludar_date(tmp)
        ret.append(y2)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

def LMONTH(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        y=int(s[0:4])
        m=int(s[5:7])
        d=int(s[8:10])
        tmp = dt.datetime(y, m, d)
        y2,m2,d2=get_ludar_date(tmp)
        ret.append(m2)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

def LDAY(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        y=int(s[0:4])
        m=int(s[5:7])
        d=int(s[8:10])
        tmp = dt.datetime(y, m, d)
        y2,m2,d2=get_ludar_date(tmp)
        ret.append(d2)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

def CYEAR(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        y=int(s[0:4])
        m=int(s[5:7])
        d=int(s[8:10])
        tmp = dt.datetime(y, m, d)
        y2,m2,d2=get_ludar_date(tmp)
        y3=lunar_year(y2)
        ret.append(y3)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

def CYEARX(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        y=int(s[0:4])
        m=int(s[5:7])
        d=int(s[8:10])
        tmp = dt.datetime(y, m, d)
        y2,m2,d2=get_ludar_date(tmp)
        y3=lunar_year(y2)
        ret.append(y3)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)


def CMONTH(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        y=int(s[0:4])
        m=int(s[5:7])
        d=int(s[8:10])
        tmp = dt.datetime(y, m, d)
        y2,m2,d2=get_ludar_date(tmp)
        m3=lunar_month(m2)
        ret.append(m3)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

def CDAY(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        y=int(s[0:4])
        m=int(s[5:7])
        d=int(s[8:10])
        tmp = dt.datetime(y, m, d)
        y2,m2,d2=get_ludar_date(tmp)
        d3= lunar_day(d2)
        ret.append(d3)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)



"""
Series 类

这个是下面以DataFrame为输入的基础函数
return pd.Series format
"""

#求相反数。
def REVERSE(Series):
    return -Series
    
#异同移动平均
def EXPMEMA(Series, N):
    ret=pd.Series.ewm(Series, span=N, min_periods=N - 1, adjust=True).mean()
    return pd.Series(ret, index=Series.tail(len(ret)).index)

#异同移动平均
def EMA(S,N):
    ret= pd.Series(S).ewm(span=N, adjust=False).mean().values   
    return pd.Series(ret, index=S.tail(len(ret)).index)


#简单移动平均
def MA(Series, N):
    return pd.Series.rolling(Series, N).mean()

#简单移动平均
def MA2(Series, N):
    var=pd.Series.rolling(Series, N).mean()
    if N>0:
        y=0
        for i in range(N):
            y=y+Series[i]
            var[i]=y/(i+1)
    return var


#累积平均
# SMA(X,N,M):X的N日移动平均,M为权重,如Y=(X*M+Y'*(N-M))/N
def SMA(S, N, M=1):      
    ret=pd.Series(S).ewm(alpha=M/N,adjust=False).mean().values 
    return pd.Series(ret, index=S.tail(len(ret)).index)
    

#累积平均
# SMA(X,N,M):X的N日移动平均,M为权重,如Y=(X*M+Y'*(N-M))/N
def SMA2(Series, N, M=1):
    ret = []
    i = 1
    length = len(Series)
    # 跳过X中前面几个 nan 值
    while i < length:
        if np.isnan(Series.iloc[i]):
            i += 1
        else:
            break
    
    preY = Series.iloc[i]  # Y'
    ret.append(preY)
    while i < length:
        Y = (M * Series.iloc[i] + (N - M) * preY) / float(N)
        ret.append(Y)
        preY = Y
        i += 1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

# WMA(X,N):X的N日加权移动平均.算法:Yn=(1*X1+2*X2+...+n*Xn)/(1+2+...+n)
def WMA(S, N):            #通达信S序列的N日加权移动平均 Yn = (1*X1+2*X2+3*X3+...+n*Xn)/(1+2+3+...+Xn)
    ret=pd.Series(S).rolling(N).apply(lambda x:x[::-1].cumsum().sum()*2/N/(N+1),raw=True).values
    return pd.Series(ret, index=S.tail(len(ret)).index)
    

# WMA(X,N):X的N日加权移动平均.算法:Yn=(1*X1+2*X2+...+n*Xn)/(1+2+...+n)
def WMA2(Series, N):
    ret = []
    i = 0
    length = len(Series)
    # 跳过X中前面几个 nan 值
#    while i < length:
#        if np.isnan(Series.iloc[i]):
#            i += 1
#        else:
#            break
#    j=1
#    while j<N and i<length:
#        #preY = Series.iloc[i]  # Y'
#        ret.append( np.NAN)
#        i+=1
#        j=j+1
    while i < length:
        j=0
        y=0.0
        y2=0
        while j<N:
            y = y+Series.iloc[i-N+j]*(j+1)
            j=j+1
            y2= y2+j
            
        i=i+1
        y3= y/ float(y2)
        ret.append(y3)
    return pd.Series(ret, index=Series.tail(len(ret)).index)


def SMMA(Series,N,M):
    SUM1 = SUM(Series, N)
    SMMA1 = SUM1/N
    SMMA2 =  (SUM1-SMMA1+Series)/M
    return SMMA2

#SUM(Close(i)*i, N)/SUM(i, N)
def LWMA(Series,N):
    ret = []
    _ls=list[Series]
    i = 0
    length = len(Series)
    # 跳过X中前面几个 nan 值
    while i < length:
        _ls[i]=_ls[i]*i
        ret.append(i)    
    lwma=SUM(_ls,N)/SUM(ret,N)
    return pd.Series(lwma, index=Series.tail(len(ret)).index)
    


def DIFF(Series, N=1):
    return pd.Series(Series).diff(N)

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

def LLV2(Series, N):
    if isinstance(N, int):  # N为整型
        return pd.Series(Series).rolling(N).min()
    elif isinstance(N, (list, pd.Series)):  # N为序列或列表
        df = pd.DataFrame({'Series': Series, 'N': N})
        res = []
        for idx, row in df.iterrows():
            if not np.isnan(row[1]):
                N = int(row[1])
                r = df['Series'].rolling(N).min()
                rs = r.iloc[idx]
            else:
                rs = np.nan
            res.append(rs)
        return res


def HHV2(Series, N):
    if isinstance(N, int):  # N为整型
        return pd.Series(Series).rolling(N).max()
    elif isinstance(N, (list, pd.Series)):  # N为序列或列表
        df = pd.DataFrame({'Series': Series, 'N': N})
        res = []
        for idx, row in df.iterrows():
            if not np.isnan(row[1]):
                N = int(row[1])
                r = df['Series'].rolling(N).max()
                rs = r.iloc[idx]
            else:
                rs = np.nan
            res.append(rs)
        return res



#新的变参HHV()
def HHV3(Series, Series2):
    if 'int' in str(type(Series2)):
        return pd.Series(Series).rolling(Series2,min_periods=1).max()
    s1,lenth1=list(Series),len(Series)
    if 'list' in str(type(Series2)):
        s2,lenth2=Series2,len(Series2)
    else:
        s2,lenth2=list(Series2),len(Series2)
    bars_=[]
    if lenth1!=lenth2:
        return np.nan
    for i in range(lenth1):
        if not np.isnan(s2[i]):
            if i - int(s2[i]) >= 0:
                bars_.append(max(s1[i - int(s2[i]):i+1]))
            else:
                bars_.append(max(s1[0:i+1]))
        else:
            bars_.append(s1[i])
    return pd.Series(bars_)

#新的变参LLV()
def LLV3(Series, Series2):
    if 'int' in str(type(Series2)):
        return pd.Series(Series).rolling(Series2,min_periods=1).min()
    s1,lenth1=list(Series),len(Series)
    if 'list' in str(type(Series2)):
        s2,lenth2=Series2,len(Series2)
    else:
        s2,lenth2=list(Series2),len(Series2)
    bars_=[]
    if lenth1!=lenth2:
        return np.nan
    for i in range(lenth1):
        if not np.isnan(s2[i]):
            if i - int(s2[i]) >= 0:
                bars_.append(min(s1[i - int(s2[i]):i+1]))
            else:
                bars_.append(min(s1[0:i+1]))
        else:
            bars_.append(s1[i])
    return pd.Series(bars_)


def SUMX(Series, N=0):
    if N<=0:
        N=len(Series)
    sum_=pd.Series.rolling(Series, N).sum()
    return pd.Series(sum_,name='sums')

def SUM(ser_,p):
    ser_,sum_=list(ser_),[ser_[0],]
    for i in range(1,len(ser_)):
        if i<p:sum_.append(sum(ser_[:i+1]))
        else:sum_.append(sum(ser_[i+1-p:i+1]))
    return pd.Series(sum_,name='sums')

def SUMX_2(ser_1, ser_2):
    ser_2,sum_2=list(ser_2),list(ser_2) #将ser_2和sum_2设置为长度与ser_2相同的数组
    for i in range(1,len(ser_1)+1):
        N=0
        for p in ser_2:
            N=N+1
            if p > 0:
                pp=int(p)
            else:
                pp=0
            if N==i:
                sum_1=pd.Series.rolling(ser_1, pp).sum()
        sum_2[i-1]=sum_1[i-1]
    return pd.Series(sum_2,name='sums')

def RD(N,D=3):   return np.round(N,D)        #四舍五入取3位小数 
def RET(S,N=1):  return np.array(S)[-N]      #返回序列倒数第N个值,默认返回最后一个

def ABS(Series):  #绝对值 
    return abs(Series)

def MAX(A, B):
    var = IF(A > B, A, B)
    return pd.Series( var,name='maxs')

def MIN(A, B):
    var = IF(A < B, A, B)
    return var

def SQRT(A):   #平方根 
    A2=np.array(A)
    var = np.sqrt(A2)
    return (pd.Series(var, index=A.index))


def SQUARE(A):   #平方根 
    A2=np.array(A)
    var = np.square(A2)
    return (pd.Series(var, index=A.index))

def CEILING(A):   #返回沿A数值增大方向最接近的整数。
    A2=np.array(A)
    var = np.ceil(A2)
    return (pd.Series(var, index=A.index))

def FLOOR(A):   #返回沿A数值减少方向最接近的整数。
    A2=np.array(A)
    var = np.floor(A2)
    return (pd.Series(var, index=A.index))

def INTPART(A):   #返回沿A数值减少方向最接近的整数。
    A2=np.array(A)
    var = np.floor(A2)
    return (pd.Series(var, index=A.index))

def INT(A):   #返回沿A数值四舍五入
    A2=np.array(A)
    var = np.rint(A2)
    return (pd.Series(var, index=A.index))

def LN(A):   #自然对数
    A2=np.array(A)
    var = np.log(A2)
    return (pd.Series(var, index=A.index))


def LOG(A):    #10为底的对数
    A2=np.array(A)
    var = np.log10(A2)
    return (pd.Series(var, index=A.index))

def LOG2(A):   #2为底的对数
    A2=np.array(A)
    var = np.log2(A2)
    return (pd.Series(var, index=A.index))

def EXP(A):   #指数值 
    A2=np.array(A)
    var = np.exp(A2)
    return (pd.Series(var, index=A.index))

def POW(A,x):   #A的x次幂
    A2=np.array(A)
    var = A2**x
    return (pd.Series(var, index=A.index))

def POW2(x):
    if isinstance(x, int or float):  # N为整型
        return 10**x
    elif isinstance(x, (list, pd.Series)):  # N为序列或列表
        x_array = np.array(list(x))
        res = 10 ** x_array
        return pd.Series(res)

def SIGN(A):   #符号值 1（+），0，-1（-）  
    A2=np.array(A)
    var = np.sign(A2)
    return (pd.Series(var, index=A.index))


def MOD(A, B):  #元素级的模运算
    var = np.mod(np.array(A) ,np.array(B))
    return  (pd.Series(var, index=A.index))

def COS(A):   
    A2=np.array(A)
    var = np.cos(A2)
    return (pd.Series(var, index=A.index))


def SIN(A):   
    A2=np.array(A)
    var = np.sin(A2)
    return (pd.Series(var, index=A.index))



def TAN(A):   
    A2=np.array(A)
    var = np.tan(A2)
    return (pd.Series(var, index=A.index))


def ACOS(A):   
    A2=np.array(A)
    var = np.arccos(A2)
    return (pd.Series(var, index=A.index))

def ASIN(A):   
    A2=np.array(A)
    var = np.arcsin(A2)
    return (pd.Series(var, index=A.index))

def ATAN(A):   
    A2=np.array(A)
    var = np.arctan(A2)
    return (pd.Series(var, index=A.index))

def HTPOT(A, B):  #直角三角形求斜边
    var = np.hypot(np.array(A) ,np.array(B))
    return  (pd.Series(var, index=A.index))


def SINGLE_CROSS(A, B):
    if A.iloc[-2] < B.iloc[-2] and A.iloc[-1] > B.iloc[-1]:
        return True
    else:
        return False

# A上穿B。B可为数字
def CROSS(A, B):
    if ('Series' in str(type(A))) :
        A2=np.array(A)
        B2=B
    else:
        A2=A
        B2=np.array(B)
    var = np.where(A2<B2, 1, 0)
    return (pd.Series(var).diff()<0).apply(int)

def CROSSX(A, B):
    if ('Series' in str(type(A))) :
        A2=np.array(A)
        B2=B
    else:
        A2=A
        B2=np.array(B)
    var = np.where(A2<B2, 1, 0)
    return (pd.Series(var).diff()<0).apply(int)

#表示A大于B同时小于C时返回1，否则返回0。
def RANGE(A, B, C):
    A2=np.array(A)
    var = np.where(A2>=B, 1, 0)
    var2 = np.where(A2<=C, 1, 0)
    v1=pd.Series(var, index=A.index)
    v2=pd.Series(var2, index=A.index)
    v3=v1*v2
    return v3

#表示A大于B同时小于C时返回1，否则返回0。
#贡献代码Andrew(596542695)  
def BETWEEN(SA, SB, SC):
    SB2 = MIN(SB, SC)
    SC2 = MAX(SB, SC)
    return RANGE(SA, SB2, SC2)

def LONGCROSS(S1,S2,N):                # 两条线维持一定周期后交叉,S1在N周期内都小于S2,本周期从S1下方向上穿过S2时返回1,否则返回0         
    return  np.array(np.logical_and(LAST(S1<S2,N,1),(S1>S2)),dtype=bool)            # N=1时等同于CROSS(S1, S2)
    
def VALUEWHEN(S, X):                   # 当S条件成立时,取X的当前值,否则取VALUEWHEN的上个成立时的X值
    return pd.Series(np.where(S,X,np.nan)).ffill().values  

#统计N周期中满足X条件的周期数，若N=0则从第一个有效值开始。
def COUNT(COND,N=0):
    if N==0:
        return pd.Series(np.where(COND,1,0),index=COND.index).cumsum()
    else:
        return pd.Series(np.where(COND,1,0),index=COND.index).rolling(N).sum()

#统计N周期中满足X条件的周期数，若N=0则从第一个有效值开始。
def COUNT2(COND, N):
    var=pd.Series(np.where(COND,1,0),index=COND.index).rolling(N).sum()
    if N>0:
        y=0
        for i in range(N):
            print(COND.iloc[i])
            if  COND.iloc[i]:
                y=y+1
            var[i]=y
    return var

#　IF(X，A，B)　若X不不为0则返回A，否则返回B。
def IF(COND, V1, V2):
    var = np.where(COND, V1, V2)
    return pd.Series(var)

def AND(V1, V2):
    var = np.where(V1>=1, 1, 0)
    var2 = np.where(V2>=1, 1, 0)
    return pd.Series(var*var2)

def OR(V1, V2):
    var = np.where(V1>=1, 1, 0)
    var2 = np.where(V2>=1, 1, 0)
    var3=var+var2
    var4 = np.where(var3>=1, 1, 0)
    return pd.Series(var4)
    

#　IFF(X，A，B)　若X不不为0则返回A，否则返回B。
def IFF(COND, V1, V2):
    var = np.where(COND, V1, V2)
    return pd.Series(var)
# IFN(X，A，B)　若X不不为0则返回B，否则返回A。
def IFN(COND, V1, V2):
    var = np.where(COND, V2, V1)
    return pd.Series(var)


#向前引用引用若干周期前的数据。
def REF(Series, N,sign=0):
    #sign=1表示保留数据,并延长序列
    if sign==1:
        for i in range(N):
            Series=Series.append(pd.Series([0],index=[len(Series)+1]))
    return Series.shift(N)

def REFX(Series, N):
    return Series.shift(-N)

#变参REFA()
def REFA(Series, Series2):
    if 'int' in str(type(Series2)):
        return REF(Series, Series2)
    s1,lenth1=list(Series),len(Series)
    if 'list' in str(type(Series2)):
        s2,lenth2=Series2,len(Series2)
    else:
        s2,lenth2=list(Series2),len(Series2)
    bars_=[]
    if lenth1!=lenth2:
        return Series
    for i in range(lenth1):
        if s1[i-int(s2[i])]==np.nan:
            bars_.append(np.nan)
        elif (i-int(s2[i])>=0 and (i-int(s2[i]))<lenth1):
            bars_.append(s1[i-int(s2[i])])
        else:
            bars_.append(np.nan)
    return pd.Series(bars_ )    


def LAST(COND, N1, N2):
    N2 = 1 if N2 == 0 else N2
    assert N2 > 0
    assert N1 > N2
    return COND.iloc[-N1:-N2].all()

def STD(Series, N):
    return pd.Series.rolling(Series, N).std()

def AVEDEV(Series, N):
    return Series.rolling(N).apply(lambda x: (np.abs(x - x.mean())).mean(), raw=True)

#求S的动态移动平均，A作平滑因子,必须 0<A<1  (此为核心函数，非指标）
def DMA(S, A):            
    if isinstance(A,(int,float)):  return pd.Series(S).ewm(alpha=A,adjust=False).mean().values    
    A=np.array(A);   A[np.isnan(A)]=1.0;   Y= np.zeros(len(S));   Y[0]=S[0]     
    for i in range(1,len(S)): Y[i]=A[i]*S[i]+(1-A[i])*Y[i-1]              
    return pd.Series(Y, index=S.tail(len(Y)).index)

#求X的动态移动平均。若Y=DMA(X，A)则Y=A*X+(1-A)*Y'，
#其中Y'表示上一周期Y值，A必须小于1。
def DMA2(S,para_):#DMA函数(para<1)
    if (np.isnan(para_).any()):
        newdf=pd.DataFrame(para_)
        newdf=newdf.fillna(axis=0,value=0.000000000001)
        para_=newdf[0]
    ser_=list(S),
    dma_=[ser_[0]]
    for i in range(1,len(ser_)):
        dma_.append(para_[i]*ser_[i]+(1-para_)*dma_[-1])
    return dma_

#求N周期内X最高值到当前周期数，
#N=0表示从第一个有效值开始统计。
def LLVBARS(price,window):
    return price.rolling(window).apply(lambda x:window-np.argmin(x)-1,raw=True)

#求N周期内X最低值到当前周期数，
#N=0表示从第一个有效值开始统计。
def HHVBARS(price,window):
    return price.rolling(window).apply(lambda x:window-np.argmax(x)-1,raw=True)

#BARSLAST 上一次条件成立位置
def BARSLAST2(ser_cond):
    ser_cond,sig_,bars_,lenth=list(ser_cond),[0,],[],len(ser_cond)
    for i in range(1,lenth):
        sig_.append(1) if ser_cond[i]==True and ser_cond[i-1]==False else sig_.append(0)
    first_=sig_.index(1)
    for i in range(first_):
        bars_.append(np.nan)
    for i in range(first_,lenth):
        if sig_[i]==1:
            count_=0
            bars_.append(0)
        else:
            count_+=1
            bars_.append(count_)
    return pd.Series(bars_ )

def BARSLAST(COND):
    result_=[i*0 for i in COND]
    for n in range(1,len(COND)+1):
        sumxs_n=COUNT(COND,n)
        j=0
        for sumx_n in sumxs_n:
            j+=1
            if  result_[j-1] ==0 and sumx_n == 1 :
                result_[j-1]=n
    return pd.Series(result_ ,name='sumbars')-1

# 统计连续满足S条件的周期数    
def BARSLASTCOUNT(S):                  # 统计连续满足S条件的周期数    
    rt = np.zeros(len(S)+1)            # BARSLASTCOUNT(CLOSE>OPEN)表示统计连续收阳的周期数
    for i in range(len(S)): rt[i+1]=rt[i]+1  if S[i] else rt[i+1]
    return rt[1:]  

def BARSSINCEN(S, N):                  # N周期内第一次S条件成立到现在的周期数,N为常量
    return pd.Series(S).rolling(N).apply(lambda x:N-1-np.argmax(x) if np.argmax(x) or x[0] else 0,raw=True).fillna(0).values.astype(int)

def ISLASTBAR(ser_cond):
    ser_cond,bars_,lenth=list(ser_cond),[],len(ser_cond)
    for i in range(0,lenth):
        bars_.append(0)
    bars_[-1]=1
    return pd.Series(bars_ )

#返回无效数。
def DRAWNULL():
    return np.nan

#第一个有效数据到当前的天数。
def BARSCOUNT(ser_cond):
    ser_cond=list(ser_cond)
    lenth=len(ser_cond)
    bars_=[]
    y=0
    sign=False
    for i in range(0,lenth):
        if math.isnan(float(ser_cond[i])) and sign==False:
            bars_.append(0)
        else:
            y=y+1
            bars_.append(y)
    return pd.Series(bars_ )

#BARSSINCE(X)　第一次X不不为0到现在的天数。
def BARSSINCE(ser_cond):
    ser_cond=list(ser_cond)
    lenth=len(ser_cond)
    bars_=[]
    y=0
    sign=False
    for i in range(0,lenth):
        if math.isnan(float(ser_cond[i])) and sign==False:
            bars_.append(0)
        else:
            if ser_cond[i]>0  and sign==False:
                sign=True
            if sign==True:
                y=y+1
            bars_.append(y)
    return pd.Series(bars_ )

def NOT(A):
    A2=np.array(A)
    var = np.where(A2>0, 0, 1)
    return (pd.Series(var, index=A.index).diff()<0).apply(int)

#过滤连续出现的信号。
#X满足条件后，删除其后N周期内的数据置为0。
def FILTER(A, N):
    A2=np.array(A)
    var = np.where(A2>0, 1, 0)
    k=N
    sign=False
    for i in range(len(var)):
        if sign==True and k>0:
            var[i]=0
            k=k-1
        if k<=0:
            sign=False
        if var[i]>0:
            sign=True
            k=N
    return (pd.Series(var, index=A.index).diff()<0).apply(int)

#BACKSET(X，N)　若X非0，则将当前位置到N周期前的数值设为1。
def BACKSET(A, N):
    A2=np.array(A)
    var = np.where(A2>0, 1, 0)
    for i in range(len(var)):
        if var[i]>0:
            for j in range(min(i,N)):
                var[i-j]=0
                
    return (pd.Series(var, index=A.index).diff()<0).apply(int)

def TFILTER(A,B, N):
    A2=np.array(A)
    var = np.where(A2>0, 1, 0)
    B2=np.array(B)
    var2 = np.where(B2>0, 1, 0)    
    sign=False
    for i in range(len(var)):
        if N==1 or N==0:
            if sign==False and var[i]>0:
                var[i]=1
                sign=True
        else:
            if  var[i]>0:
                var[i]=1
                sign=True
                
        if N==2 or N==0:
            if sign==True and var2[i]>0:
                var[i]=2
                sign=False
        else:
            if  var2[i]>0:
                var[i]=2
                sign=False
    return (pd.Series(var, index=A.index).diff()<0).apply(int)


def TFILTER2(A, B, N):
    A2 = np.array(A)
    var = np.where(A2 > 0, 1, 0)
    B2 = np.array(B)
    var2 = np.where(B2 > 0, 1, 0)
    sign = False
    for i in range(len(var)):
        if N == 1 or N == 0:
            if sign == False and var[i] > 0:
                var[i] = 1
                sign = True
            else:
                if var[i] > 0:
                    var[i] = 1
                    sign = True

        if N == 2 or N == 0:
            if sign == True and var2[i] > 0:
                var[i] = 2
                sign = False
            else:
                if var2[i] > 0:
                    var[i] = 2
                    sign = False
    return (pd.Series(var, index=A.index).diff() < 0).apply(int)

#线性回归斜率
def SLOPE2(Series, N):
    #SLOPE(X,N)为X的N周期线性回归线的斜率
    xx=list(Series)
    res=np.ones(len(xx))*np.nan
    for i in range(N,len(xx)):
        slp=np.polyfit(range(N),xx[i+1-N:i+1],1)
        res[i]=slp[0]
    #return pd.Series(res)
    return pd.Series(res, index=Series.tail(len(res)).index)


def SLOPE(S, N):          #返S序列N周期回线性回归斜率            
    ret=pd.Series(S).rolling(N).apply(lambda x: np.polyfit(range(N),x,deg=1)[0],raw=True).values
    return pd.Series(ret, index=S.tail(len(ret)).index)

def FORCAST(S, N):        #返回S序列N周期回线性回归后的预测值，  
    ret= pd.Series(S).rolling(N).apply(lambda x:np.polyval(np.polyfit(range(N),x,deg=1),N-1),raw=True).values  
    return pd.Series(res, index=Series.tail(len(res)).index)


ZIG_STATE_START = 0
ZIG_STATE_RISE = 1
ZIG_STATE_FALL = 2
def zig(k,x=0.055):
    '''
    #之字转向
    CLOSE=mydf['close']
    zz=zig(CLOSE,x=0.055) 
    mydf = mydf.join(pd.Series(zz,name='zz'))  #增加 J到 mydf中1
    mydf.zz.plot.line()
    CLOSE.plot.line()
    '''
    #d = k.index
    peer_i = 0
    candidate_i = None
    scan_i = 0
    peers = [0]
    z = np.zeros(len(k))
    state = ZIG_STATE_START
    while True:
        scan_i += 1
        if scan_i == len(k) - 1:
            # 扫描到尾部
            if candidate_i is None:
                peer_i = scan_i
                peers.append(peer_i)
            else:
                if state == ZIG_STATE_RISE:
                    if k[scan_i] >= k[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
                elif state == ZIG_STATE_FALL:
                    if k[scan_i] <= k[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
            break
 
        if state == ZIG_STATE_START:
            if k[scan_i] >= k[peer_i] * (1 + x):
                candidate_i = scan_i
                state = ZIG_STATE_RISE
            elif k[scan_i] <= k[peer_i] * (1 - x):
                candidate_i = scan_i
                state = ZIG_STATE_FALL
        elif state == ZIG_STATE_RISE:
            if k[scan_i] >= k[candidate_i]:
                candidate_i = scan_i
            elif k[scan_i] <= k[candidate_i]*(1-x):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_FALL
                candidate_i = scan_i
        elif state == ZIG_STATE_FALL:
            if k[scan_i] <= k[candidate_i]:
                candidate_i = scan_i
            elif k[scan_i] >= k[candidate_i]*(1+x):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_RISE
                candidate_i = scan_i
    
    #线性插值， 计算出zig的值            
    for i in range(len(peers) - 1):
        peer_start_i = peers[i]
        peer_end_i = peers[i+1]
        start_value = k[peer_start_i]
        end_value = k[peer_end_i]
        a = (end_value - start_value)/(peer_end_i - peer_start_i)# 斜率
        for j in range(peer_end_i - peer_start_i +1):
            z[j + peer_start_i] = start_value + a*j
    
    return z
"""
之字转向。
用法:
ZIG(K,N,ABS),当价格变化量超过N%时转向,K表示0:开盘价,1:最高价,2:最低价,3:收盘价,4:低点采用最低价、高点采用最高价。若ABS为0或省略，则表示相对ZIG转向，否则为绝对ZIG转向。
例如：ZIG(3,5)表示收盘价的5%的ZIG转向;
ZIG(3,0.5,1)表示收盘价的0.5元绝对ZIG转向
"""
def ZIG(k,x=5.5):
    '''
    #之字转向
    CLOSE=mydf['close']
    zz=zig(CLOSE,x=0.055) 
    mydf = mydf.join(pd.Series(zz,name='zz'))  #增加 J到 mydf中1
    mydf.zz.plot.line()
    CLOSE.plot.line()
    '''
    #d = k.index
    k=list(k)
    x=x/100
    peer_i = 0
    candidate_i = None
    scan_i = 0
    peers = [0]
    z = np.zeros(len(k))
    state = ZIG_STATE_START
    while True:
        scan_i += 1
        if scan_i == len(k) - 1:
            # 扫描到尾部
            if candidate_i is None:
                peer_i = scan_i
                peers.append(peer_i)
            else:
                if state == ZIG_STATE_RISE:
                    if k[scan_i] >= k[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
                elif state == ZIG_STATE_FALL:
                    if k[scan_i] <= k[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
            break
 
        if state == ZIG_STATE_START:
            if k[scan_i] >= k[peer_i] * (1 + x):
                candidate_i = scan_i
                state = ZIG_STATE_RISE
            elif k[scan_i] <= k[peer_i] * (1 - x):
                candidate_i = scan_i
                state = ZIG_STATE_FALL
        elif state == ZIG_STATE_RISE:
            if k[scan_i] >= k[candidate_i]:
                candidate_i = scan_i
            elif k[scan_i] <= k[candidate_i]*(1-x):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_FALL
                candidate_i = scan_i
        elif state == ZIG_STATE_FALL:
            if k[scan_i] <= k[candidate_i]:
                candidate_i = scan_i
            elif k[scan_i] >= k[candidate_i]*(1+x):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_RISE
                candidate_i = scan_i
    
    #线性插值， 计算出zig的值            
    for i in range(len(peers) - 1):
        peer_start_i = peers[i]
        peer_end_i = peers[i+1]
        start_value = k[peer_start_i]
        end_value = k[peer_end_i]
        a = (end_value - start_value)/(peer_end_i - peer_start_i)# 斜率
        for j in range(peer_end_i - peer_start_i +1):
            z[j + peer_start_i] = start_value + a*j
    
    return pd.Series(z)

def getBorder(start, offset):
    greater = start * (1 + offset)
    lesser = start * (1 - offset)
    return greater, lesser


def findFirstZig(dataList, offset):
    found = 0
    greater, lesser = getBorder(dataList[0], offset)
    for i in range(1, len(dataList)):
        if dataList[i] >= greater:
            found = 1
            break
        if dataList[i] < lesser:
            found = 2
            break
    return found, i


def findNextZig(dataList, offset, foundType, pos):
    counterPos = 0
    newPos = pos
    if foundType == 1:
        for i in range(pos + 1, len(dataList)):
            if dataList[i] > dataList[newPos]:
                newPos = i
            else:
                if dataList[i] < dataList[newPos] * (1 - offset):
                    counterPos = i
                    break
    elif foundType == 2:
        for i in range(pos + 1, len(dataList)):
            if dataList[i] < dataList[newPos]:
                newPos = i
            else:
                if dataList[i] > dataList[newPos] * (1 + offset):
                    counterPos = i
                    break
    else:
        assert 0

    return newPos, counterPos


def getZigData(dataList, zigPoints):
    res = [dataList[0], ]
    for i in range(len(zigPoints) - 1):
        ov = (dataList[zigPoints[i + 1]] - dataList[zigPoints[i]]) / (zigPoints[i + 1] - zigPoints[i])
        for j in range(1, zigPoints[i + 1] - zigPoints[i] + 1):
            res.append(dataList[zigPoints[i]] + j * ov)
    return res


def MyZig(Series, offset):
    zigPoints = [0, ]
    offset = offset / 100.0

    dataList = list(Series)
    found, pos = findFirstZig(dataList, offset)
    if found == 0:
        zigPoints.append(len(dataList) - 1)
    else:
        while True:
            newPos, counterPos = findNextZig(dataList, offset, found, pos)
            if newPos > len(Series) - 1:
                break
            zigPoints.append(newPos)
            if counterPos == 0:
                break
            pos = counterPos
            found = (found % 2) + 1
        if zigPoints[-1] != len(Series) - 1:
            zigPoints.append(len(Series) - 1)

    res = getZigData(dataList, zigPoints)
    return pd.Series(res)


def ZIG2(k,x=5.5):
    '''
    #之字转向
    CLOSE=mydf['close']
    zz=zig(CLOSE,x=0.055) 
    mydf = mydf.join(pd.Series(zz,name='zz'))  #增加 J到 mydf中1
    mydf.zz.plot.line()
    CLOSE.plot.line()
    '''
    k=list(k)
    x=x/100
    peer_i = 0
    candidate_i = None
    scan_i = 0
    peers = [0]
    z = np.zeros(len(k))
    state = ZIG_STATE_START
    while True:
        scan_i += 1
        if scan_i == len(k) - 1:
            # 扫描到尾部
            if candidate_i is None:
                peer_i = scan_i
                peers.append(peer_i)
            else:
                if state == ZIG_STATE_RISE:
                    if k[scan_i] >= k[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
                else :
                    if state == ZIG_STATE_FALL:
                        if k[scan_i] <= k[candidate_i]:
                            peer_i = scan_i
                            peers.append(peer_i)
                        else:
                            peer_i = candidate_i
                            peers.append(peer_i)
                            peer_i = scan_i
                            peers.append(peer_i)
            break
 
        if state == ZIG_STATE_START:
            if k[scan_i] >= k[peer_i] * (1 + x):
                candidate_i = scan_i
                state = ZIG_STATE_RISE
            else:
                if k[scan_i] <= k[peer_i] * (1 - x):
                    candidate_i = scan_i
                    state = ZIG_STATE_FALL
        else:
            if state == ZIG_STATE_RISE:
                if k[scan_i] >= k[candidate_i]:
                    candidate_i = scan_i
                else:
                    if k[scan_i] <= k[candidate_i]*(1-x):
                        peer_i = candidate_i
                        peers.append(peer_i)
                        state = ZIG_STATE_FALL
                        candidate_i = scan_i
            else:
                if state == ZIG_STATE_FALL:
                    if k[scan_i] <= k[candidate_i]:
                        candidate_i = scan_i
                    else:
                        if k[scan_i] >= k[candidate_i]*(1+x):
                            peer_i = candidate_i
                            peers.append(peer_i)
                            state = ZIG_STATE_RISE
                            candidate_i = scan_i
    
    #线性插值， 计算出zig的值            
    for i in range(len(peers) - 1):
        peer_start_i = peers[i]
        peer_end_i = peers[i+1]
        start_value = k[peer_start_i]
        end_value = k[peer_end_i]
        a = (end_value - start_value)/(peer_end_i - peer_start_i)# 斜率
        for j in range(peer_end_i - peer_start_i +1):
            z[j + peer_start_i] = start_value + a*j
    
    return pd.Series(z),peers


# def ZIG(close_arr, ratio):
#     up_rate = 1 + ratio
#     down_rate = 1 - ratio
#     极值列表 = []
#     高点 = [0, close_arr[0]]
#     低点 = [0, close_arr[0]]
#     side = 0
#     for i, 收 in enumerate(close_arr):
#         if 收 > 高点[1]:
#             高点[0] = i
#             高点[1] = 收
#         elif 收 < 低点[1]:
#             低点[0] = i
#             低点[1] = 收

#         if side >= 0 and 收 < 高点[1] * down_rate:  # 下跌确认
#             极值列表.append((side, i, 高点[0], 高点[1]))
#             side = -1
#             低点[0] = i
#             低点[1] = 收
#         elif side <= 0 and 收 > 低点[1] * up_rate:
#             极值列表.append((side, i, 低点[0], 低点[1]))
#             side = 1
#             高点[0] = i
#             高点[1] = 收
#         if i > 3875:
#             breakpoint()
#     极值_dtype = np.dtype([('side', 'i'),
#                          ('index', 'i'),
#                          ('extreme_i', 'i'),
#                          ('extreme_v', 'f')])
#     return np.array(极值列表, dtype=极值_dtype)
def ZIG3(K线数据_df, ratio):
    close_arr = K线数据_df['MAP'].values
    日期_arr = K线数据_df['日期'].values
    收盘价_arr = K线数据_df['收盘价'].values
    up_rate = 1 + ratio
    down_rate = 1 - ratio
    极值列表 = []
    高点 = [0, close_arr[0]]
    低点 = [0, close_arr[0]]
    side = 0
    for i, 收 in enumerate(close_arr):
        if 收 > 高点[1]:
            高点[0] = i
            高点[1] = 收
        elif 收 < 低点[1]:
            低点[0] = i
            低点[1] = 收

        if side >= 0 and 收 < 高点[1] * down_rate:  # 下跌确认
            极值列表.append((side, i, 高点[0], 高点[1]))
            side = -1
            低点[0] = i
            低点[1] = 收
        elif side <= 0 and 收 > 低点[1] * up_rate:
            极值列表.append((side, i, 低点[0], 低点[1]))
            side = 1
            高点[0] = i
            高点[1] = 收
        if i > 3800:
            print(日期_arr[i], close_arr[i], 收盘价_arr[i], 低点[0], 高点[1])
            breakpoint()
    极值_dtype = np.dtype([('side', 'i'),
                         ('index', 'i'),
                         ('extreme_i', 'i'),
                         ('extreme_v', 'f')])
    return np.array(极值列表, dtype=极值_dtype)

##代码贡献：周(2047887246) 2021/6/30 23:02:22
#TROUGHBARS(K,N,M)表示之字转向ZIG(K,N)的前M个波谷到当前的周期数,M必须大于等于1
def TROUGHBARS(K,N,M):
    a1=ZIG(K,N)
    波谷=(REF(a1,1)<REF(a1,2))&(REF(a1,0)>REF(a1,1))
    波谷=波谷+0
    波谷个数=0
    周期数=0
    for i in  range(len(波谷)):
        波谷个数=波谷[len(波谷)-i-1]+波谷个数
        周期数=i
        if(M==波谷个数):
            break
    return 周期数

#PEAKBARS(K,N,M)表示之字转向ZIG(K,N)的前M个波峰到当前的周期数,M必须大于等于1
def PEAKBARS(K,N,M):
    a1=ZIG(K,N)
    波峰=(REF(a1,1)>REF(a1,2))&(REF(a1,0)<REF(a1,1))
    波峰=波峰+0
    波峰个数=0
    周期数=0
    for i in  range(len(波峰)):
        波峰个数=波峰[len(波峰)-i-1]+波峰个数
        周期数=i
        if(M==波峰个数):
            break
    return 周期数


#SUMBARS(X,A):将X向前累加直到大于等于A,返回这个区间的周期数
def SUMBARS(X,A):
    X2 = np.array(X)
    var = np.where(X2 > A, 0, -1)
    A2=0.0
    i=len(X2)-1
    j=0
    while i>0:
        if var[i] ==0:
            i=i-1
            A2=0.0
            j=0
        elif X2[i] !=0:
            A2=A2+X2[i-j]
            if A2>A:
                var[i]=j
                j=j-1
                A2=A2-X2[i]
                i=i-1
            if j<i:
                j=j+1
            else:
                for k in range(j):
                    var[k]=-1
                i=0
    return pd.Series(var)
    
    

#######################################################

def SAR(h, l, afstep, aflimit):
    high, low=np.array(h),np.array(l)
    oParClose = None
    oParOpen = None
    oPosition = None
    oTransition = None

    opc_s = []
    opo_s = []
    opos_s = []
    otran_s = []

    hlen = len(high)
    llen = len(low)

    if hlen <= 0 or llen <= 0:
        return pd.Series(opc_s), pd.Series(opo_s), pd.Series(opos_s), pd.Series(otran_s)

    arr = high if hlen < llen else low

    Af = 0
    ParOpen = 0
    Position = 0
    HHValue = 0
    LLValue = 0
    pHHValue = 0
    pLLValue = 0

    for i, a in enumerate(arr):
        if i == 0:
            Position = 1
            oTransition = 1
            Af = afstep
            HHValue = high[i]
            LLValue = low[i]
            oParClose = LLValue
            ParOpen = oParClose + Af * (HHValue - oParClose)
            if ParOpen > LLValue:
                ParOpen = LLValue
        else:
            oTransition = 0

            pHHValue = HHValue
            pLLValue = LLValue
            HHValue = HHValue if HHValue > high[i] else high[i]
            LLValue = LLValue if LLValue < low[i] else low[i]

            if Position == 1:
                if low[i] <= ParOpen:
                    Position = -1
                    oTransition = -1
                    oParClose = HHValue
                    pHHValue = HHValue
                    pLLValue = LLValue
                    HHValue = high[i]
                    LLValue = low[i]

                    Af = afstep
                    ParOpen = oParClose + Af * (LLValue - oParClose)

                    if ParOpen < high[i]:
                        ParOpen = high[i]

                    if ParOpen < high[i - 1]:
                        ParOpen = high[i - 1]

                else:
                    oParClose = ParOpen
                    if HHValue > pHHValue and Af < aflimit:
                        if Af + afstep > aflimit:
                            Af = aflimit
                        else:
                            Af = Af + afstep

                    ParOpen = oParClose + Af * (HHValue - oParClose)

                    if ParOpen > low[i]:
                        ParOpen = low[i]

                    if ParOpen > low[i - 1]:
                        ParOpen = low[i - 1]

            else:
                if high[i] >= ParOpen:
                    Position = 1
                    oTransition = 1

                    oParClose = LLValue
                    pHHValue = HHValue
                    pLLValue = LLValue
                    HHValue = high[i]
                    LLValue = low[i]

                    Af = afstep
                    ParOpen = oParClose + Af * (HHValue - oParClose)

                    if ParOpen > low[i]:
                        ParOpen = low[i]

                    if ParOpen > low[i - 1]:
                        ParOpen = low[i - 1]

                else:
                    oParClose = ParOpen

                    if LLValue < pLLValue and Af < aflimit:
                        if Af + afstep > aflimit:
                            Af = aflimit
                        else:
                            Af = Af + afstep

                    ParOpen = oParClose + Af * (LLValue - oParClose)

                    if ParOpen < high[i]:
                        ParOpen = high[i]

                    if ParOpen < high[i - 1]:
                        ParOpen = high[i - 1]

        oParOpen = ParOpen
        oPosition = Position

        opc_s.append(oParClose)
        opo_s.append(oParOpen)
        opos_s.append(oPosition)
        otran_s.append(oTransition)

    return pd.Series(opc_s), pd.Series(opo_s), pd.Series(opos_s), pd.Series(otran_s)

class SARIndicator(object):
    def __init__(self,
                 high: pd.Series,
                 low: pd.Series,
                 close: pd.Series,
                 period: int = 4,
                 step: float = 0.02,
                 max_step: float = 0.20,
                 fillna: bool = False,
                 ):
        self._high = high.copy()
        self._low = low.copy()
        self._close = close.copy()
        self._length = self._close.__len__()
        self._period = period - 1
        self._step = step
        self._max_step = max_step  # 步长最大值
        self._fillna = fillna  # 是否填充空值
        self._run()

    def _run(self):
        up_trend = True  # 默认初始是上升趋势
        acceleration_factor = self._step  # 初始加速因子是0.02
        up_trend_high = self._high.iloc[0]  # 初始上升趋势最高值，为第一天的最高
        down_trend_low = self._low.iloc[0]  # 初始下降趋势最低值，为第一天的最低

        self._psar = pd.Series([np.nan] * self._length, index=self._close.index)
        self._psar_up = pd.Series([np.nan] * self._length, index=self._close.index)
        self._psar_down = pd.Series([np.nan] * self._length, index=self._close.index)
        self._psar_indicator = pd.Series([np.nan] * self._length, index=self._close.index)
        self._psar_af = pd.Series([np.nan] * self._length, index=self._close.index)

        for i in range(1, self._length):
            if i < self._period:
                up_trend_high = max(self._high.iloc[i], up_trend_high)
                down_trend_low = min(self._low.iloc[i], down_trend_low)
                continue
            # print(up_trend_high, down_trend_low)

            if up_trend:
                down_trend_low = min(self._low.iloc[i], down_trend_low)

                if np.isnan(self._psar.iloc[i - 1]):  # 如果一开始是空值，上升趋势默认，min最低点
                    self._psar.iloc[i] = down_trend_low
                else:
                    self._psar.iloc[i] = self._psar.iloc[i - 1] + (  # 如果有前值，计算
                        acceleration_factor * (up_trend_high - self._psar.iloc[i - 1])
                    )
                self._psar.iloc[i] = round(self._psar.iloc[i], 2)

                if self._psar.iloc[i] > self._low.iloc[i]:  # 上升趋势中SAR大于当前最低点，则翻转
                    up_trend = False  # 表示翻转了
                    self._psar.iloc[i] = up_trend_high  # 上一周期的max最高
                    down_trend_low = self._low.iloc[i]  # 最低值是当前的最低点
                    acceleration_factor = self._step  # 加速因子重置

                else:  # 没有翻转
                    if self._high.iloc[i] > up_trend_high:  # 如果有新高
                        up_trend_high = self._high.iloc[i]  # 更新当前周期内的最高价
                        acceleration_factor = min(  # 更新加速因子
                            acceleration_factor + self._step, self._max_step
                        )
            else:  # 进入下降趋势
                up_trend_high = max(self._high.iloc[i], up_trend_high)

                self._psar.iloc[i] = self._psar.iloc[i - 1] - (  # 如果有前值，计算
                    acceleration_factor * (self._psar.iloc[i - 1] - down_trend_low)
                )
                self._psar.iloc[i] = round(self._psar.iloc[i], 2)

                if self._psar.iloc[i] < self._high.iloc[i]:  # 下降趋势中，SAR小于当前最高点，则翻转
                    up_trend = True  # 表示翻转了
                    self._psar.iloc[i] = down_trend_low  # 上一周期的min最低
                    up_trend_high = self._high.iloc[i]  # 最高值是当前的最高点
                    acceleration_factor = self._step  # 加速因子重置

                else:
                    if self._low.iloc[i] < down_trend_low:  # 如果有新低
                        down_trend_low = self._low.iloc[i]  # 更新当前周期内的最低价
                        acceleration_factor = min(  # 更新加速因子
                            acceleration_factor + self._step, self._max_step
                        )

            if up_trend:
                self._psar_up.iloc[i] = 1
                self._psar_indicator.iloc[i] = 1
            else:
                self._psar_down.iloc[i] = 1
                self._psar_indicator.iloc[i] = -1
            self._psar_af.iloc[i] = acceleration_factor

    def psar(self):
        """
        返回SAR数值
        :return:
        """
        return pd.Series(self._psar, name='psar')

    def psar_up(self):
        """
        返回上升趋势
        :return:
        """
        return pd.Series(self._psar_up, name='psar_up')

    def psar_down(self):
        """
        返回下降趋势
        :return:
        """
        return pd.Series(self._psar_down, name='psar_down')

    def psar_indicator(self):
        """
        返回多头和空头
        :return:
        """
        return pd.Series(self._psar_indicator, name='indicator')

    def psar_acceleration_factor(self):
        """
        返回加速因子
        :return:
        """
        return pd.Series(self._psar_af, name='acceleration_factor')


#------------------------指标函数---------------------------------------------
def SUMBARSFAST(X, A): 
    # type: (np.ndarray, Optional[np.ndarray, float, int]) -> np.ndarray
    """
    通达信SumBars函数的Python实现  by jqz1226
    SumBars函数将X向前累加，直到大于等于A, 返回这个区间的周期数。例如SUMBARS(VOL, CAPITAL),求完全换手的周期数。
    :param X: 数组。被累计的源数据。 源数组中不能有小于0的元素。
    :param A: 数组（一组）或者浮点数（一个）或者整数（一个），累加截止的界限数
    :return:  数组。各K线分别对应的周期数
    """
    if any(X<=0):   raise ValueError('数组X的每个元素都必须大于0！')
    
    X = np.flipud(X)  # 倒转
    length = len(X)

    if isinstance(A * 1.0, float):  A = np.repeat(A, length)  # 是单值则转化为数组
    A = np.flipud(A)  # 倒转
    sumbars = np.zeros(length)  # 初始化sumbars为0
    Sigma = np.insert(np.cumsum(X), 0, 0.0)  # 在累加值前面插入一个0.0（元素变多1个，便于引用）

    for i in range(length):
        k = np.searchsorted(Sigma[i + 1:], A[i] + Sigma[i])
        if k < length - i:  # 找到
            sumbars[length - i - 1] = k + 1
    return sumbars.astype(int)  
  
def SAR(HIGH, LOW, N=10, S=2, M=20):             
    """
    求抛物转向。 例如SAR(10,2,20)表示计算10日抛物转向，步长为2%，步长极限为20%
    Created by: jqz1226, 2021-11-24首次发表于聚宽(www.joinquant.com)
    
    :param HIGH: high序列
    :param LOW: low序列
    :param N: 计算周期
    :param S: 步长
    :param M: 步长极限
    :return: 抛物转向
    """
    f_step = S / 100;    f_max = M / 100;    af = 0.0
    is_long = HIGH[N - 1] > HIGH[N - 2]
    b_first = True
    length = len(HIGH)

    s_hhv = REF(HHV(HIGH, N), 1)  # type: np.ndarray
    s_llv = REF(LLV(LOW, N), 1)  # type: np.ndarray
    sar_x = np.repeat(np.nan, length)  # type: np.ndarray
    for i in range(N, length):
        if b_first:  # 第一步
            af = f_step
            sar_x[i] = s_llv[i] if is_long else s_hhv[i]
            b_first = False
        else:  # 继续多 或者 空
            ep = s_hhv[i] if is_long else s_llv[i]  # 极值
            if (is_long and HIGH[i] > ep) or ((not is_long) and LOW[i] < ep):  # 顺势：多创新高 或者 空创新低
                af = min(af + f_step, f_max)
            #
            sar_x[i] = sar_x[i - 1] + af * (ep - sar_x[i - 1])

        if (is_long and LOW[i] < sar_x[i]) or ((not is_long) and HIGH[i] > sar_x[i]):  # 反空 或者 反多
            is_long = not is_long
            b_first = True
    return sar_x


def get_SAR(df,N=10,step=2,maxp=20):
    sr_value=[]
    sr_up=[]
    ep_up=[]
    af_up=[]
    sr_down=[]
    ep_down=[]
    af_down=[]
    for i in range(len(df)):
            
        if i >=N:
            if len(sr_up)==0 and len(sr_down)==0:
                if df.ix[i,'close']>df.ix[0,'close']:
                     #标记为上涨趋势
                    sr0=df['low'][0:i].min()
                    af0=0.02
                    ep0=df.ix[i,'high']
                    sr_up.append(sr0)
                    ep_up.append(ep0)
                    af_up.append(af0)
                    sr_value.append(sr0)
                if df.ix[i,'close']<=df.ix[0,'close']:
                    #标记为上涨趋势
                    sr0=df['high'][0:i].max()
                    af0=0.02
                    ep0=df.ix[i,'high']
                    sr_down.append(sr0)
                    ep_down.append(ep0)
                    af_down.append(af0)
                    sr_value.append(sr0)
            if len(sr_up)>0:
                if df.ix[i-1,'low']>sr_up[-1]:
                   sr0=sr_up[-1]
                   ep0=df['high'][-len(sr_up):].max()
                   if df.ix[i,'high']>df['high'][-(len(sr_up)-1):].max() :
                      af0=af_up[-1]+0.02
                   if df.ix[i,'high']<=df['high'][-(len(sr_up)-1):].max() :
                      af0=af_up[-1]
                   
                   sr=sr0+af0*(ep0-sr0)
                   sr_up.append(sr)
                   ep_up.append(ep0)
                   af_up.append(af0)
                   sr_value.append(sr)
                   #print('上涨sr0={},ep0={},af0={},sr={}'.format(sr0,ep0,af0,sr))
                if df.ix[i-1,'low']<=sr_up[-1]:
                   ep0=df['high'][-len(sr_up):].max()
                   sr0=ep0
                   af0=0.02
                   sr_down.append(sr0)
                   ep_down.append(ep0)
                   af_down.append(af0)
                   sr_value.append(sr0)
                   sr_up=[]
                   ep_up=[]
                   af_up=[]
            if len(sr_down)>0:
                if df.ix[i-1,'high']<sr_down[-1]:
                    sr0=sr_down[-1]
                    ep0=df['low'][-len(sr_down):].max()
                    if df.ix[i,'low']<df['low'][-(len(sr_down)-1):].max() :
                      af0=af_down[-1]+0.02
                    if df.ix[i,'low']>=df['low'][-(len(sr_down)-1):].max() :
                      af0=af_down[-1]
                   
                    sr=sr0+af0*(ep0-sr0)
                    sr_down.append(sr)
                    ep_down.append(ep0)
                    af_down.append(af0)
                    sr_value.append(sr)
                    #print('下跌sr0={},ep0={},af0={},sr={}'.format(sr0,ep0,af0,sr))
                if df.ix[i-1,'high']>=sr_down[-1]:
                   ep0=df['low'][-len(sr_up):].max()
                   sr0=ep0
                   af0=0.02
                   sr_up.append(sr0)
                   ep_up.append(ep0)
                   af_up.append(af0)
                   sr_value.append(sr0)
                   sr_down=[]
                   ep_down=[]
                   af_down=[]
    return sr_value

#######################################################
global x_all,y_all,x_train,x_test,y_train,y_test
x_all = []     #输入数据
y_all = []     #输出数据
x_train=None
x_test=None
y_train=None
y_test=None

def sk_init(df='',x=[],y=['label'],test_size=0.10):
    global x_all,y_all,x_train,x_test,y_train,y_test
    df=df.fillna(value=0.00)
    ## 不设置学习字段，自动获取数字型数据字段
    if len(x)==0:
        x=[]
        x2=df.columns
        for s in x2:
            s2=str(type(df[s].iloc[0]))
            if 'int' in s2:
                x.append(s)
            if 'float' in s2:
                x.append(s)

    #装配神经网络学习数据
    for i in range(len(df)-1):

        # 输入数字数据
        features = []
        for col in x:
            features.append(df[col].iloc[i]) 
        
        x_all.append(features)

        # 输出学习参考数据为下一周期结果
        y_all.append(df['label'].iloc[i+1])
    
    #划分学习数据和验证数据
    l=len(x_all)
    l2=int(l*(1-test_size))
    x_train,x_test,y_train,y_test = x_all[:l2:],x_all[l2:],y_all[:l2],y_all[l2:]

    return x_train,x_test,y_train,y_test
 
#####################################################
#常用股票公式，需要预先处理股票数据
'''
#首先要对数据预处理
#df = hp.get_k_data('600080',ktype='D')
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

'''
"""
#常用指标库
#版本：Ver1.00
#设计人：独狼荷蒲
#电话:18578755056
#QQ：2775205
#百度：荷蒲指标
#开始设计日期: 2021-08-29
#公众号:独狼股票分析
#最后修改日期:2021年08月29日
"""

####超买超卖型
def CCI(N=14):
    """
    CCI 商品路径指标
    """
    TYP=(HIGH+LOW+CLOSE)/3;
    CCI=(TYP-MA(TYP,N))*1000/(15*AVEDEV(TYP,N));
    return CCI

def KDJ(N=9, M1=3, M2=3):
    """
    KDJ 随机指标
    """
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = EMA(RSV, (M1 * 2 - 1))
    D = EMA(K, (M2 * 2 - 1))
    J = K * 3 - D * 2
    return K, D, J

def MFI(N=14,N2=6):
    """
    MFI 资金流量指标
    """
    TYP = (HIGH + LOW + CLOSE)/3;
    V1=SUM(IF(TYP>REF(TYP,1),TYP*VOL,0),N)/SUM(IF(TYP<REF(TYP,1),TYP*VOL,0),N);
    MFI=100-(100/(1+V1));
    return MFI

def MTM(N=12,M=6):
    """
    MTM 动量线
    """
    MTM=CLOSE-REF(CLOSE,N);
    MTMMA=MA(MTM,M);
    return MTM,MTMMA

def OSC(N=20,M=6):
    """
    OSC 变动速率线
    """
    OSC:100*(CLOSE-MA(CLOSE,N));
    MAOSC:EXPMEMA(OSC,M);
    return OSC,MAOSC

def ROC(N=12,M=6):
    """
    ROC 变动率指标
    """
    ROC=100*(CLOSE-REF(CLOSE,N))/REF(CLOSE,N);
    MAROC=MA(ROC,M);
    return ROC,MAROC

def RSI(N1=6, N2=12, N3=24):
    """
    RSI 相对强弱指标
    """
    LC = REF(CLOSE, 1)
    RSI1 = SMA(MAX(CLOSE - LC, 0), N1, 1) / SMA(ABS(CLOSE - LC), N1, 1) * 100
    RSI2 = SMA(MAX(CLOSE - LC, 0), N2, 1) / SMA(ABS(CLOSE - LC), N2, 1) * 100
    RSI3 = SMA(MAX(CLOSE - LC, 0), N3, 1) / SMA(ABS(CLOSE - LC), N3, 1) * 100
    return RSI1, RSI2, RSI3

def KD(N=9, M1=3, M2=3):
    """
    KD 随机指标KD
    """
    RSV=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100;
    K=SMA(RSV,M1,1);
    D=SMA(K,M2,1);
    return K, D

def SKDJ(N=9, M=3):
    """
    SKDJ 慢速随机指标
    """
    LOWV=LLV(LOW,N);
    HIGHV=HHV(HIGH,N);
    RSV=EMA((CLOSE-LOWV)/(HIGHV-LOWV)*100,M);
    K=EMA(RSV,M);
    D=MA(K,M);
    return K, D

def UDL(N1=3, N2=5,N3=10,N4=20):
    """
    UDL 引力线
    """
    UDL=(MA(CLOSE,N1)+MA(CLOSE,N2)+MA(CLOSE,N3)+MA(CLOSE,N4))/4;
    MAUDL=MA(UDL,M);
    return UDL, MAUDL

def WR(N=10, N1=6):
    """
    W&R 威廉指标
    """
    WR1 = (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    WR2 = (HHV(HIGH, N1) - CLOSE) / (HHV(HIGH, N1) - LLV(LOW, N1)) * 100
    return WR1, WR2

def LWR(N=9, M1=3, M2=3):
    """
    LWR LWR威廉指标
    """
    RSV= (HHV(HIGH,N)-CLOSE)/(HHV(HIGH,N)-LLV(LOW,N))*100;
    LWR1=SMA(RSV,M1,1);
    LWR2SMA(LWR1,M2,1);
    return LWR1, LWR2

def MARSI(M1=10, M2=6):
    """
    MARSI 相对强弱平均线
    """
    DIF=CLOSE-REF(CLOSE,1);
    VU=IF(DIF>=0,DIF,0);
    VD=IF(DIF<0,-DIF,0);
    MAU1=MEMA(VU,M1);
    MAD1=MEMA(VD,M1);
    MAU2=MEMA(VU,M2);
    MAD2=MEMA(VD,M2);
    RSI1=MA(100*MAU1/(MAU1+MAD1),M1);
    RSI2=MA(100*MAU2/(MAU2+MAD2),M2);
    return RSI1, RSI2

def BIAS_QL(N=6, M=6):
    """
    BIAS_QL 乖离率-传统版
    """
    BIAS =(CLOSE-MA(CLOSE,N))/MA(CLOSE,N)*100;
    BIASMA =MA(BIAS,M);
    return BIAS, BIASMA

def BIAS(L1=5, L4=3, L5=10):
    """
    BIAS 乖离率
    """
    BIAS = (CLOSE - MA(CLOSE, L1)) / MA(CLOSE, L1) * 100
    BIAS2 = (CLOSE - MA(CLOSE, L4)) / MA(CLOSE, L4) * 100
    BIAS3 = (CLOSE - MA(CLOSE, L5)) / MA(CLOSE, L5) * 100
    return BIAS, BIAS2, BIAS3

def BIAS36(M=6):
    """
    BIAS36 三六乖离
    """
    BIAS36=MA(CLOSE,3)-MA(CLOSE,6);
    BIAS612=MA(CLOSE,6)-MA(CLOSE,12);
    MABIAS=MA(BIAS36,M);
    return BIAS36, BIAS612, MABIAS

def ACCER(N=8):
    """
    ACCER 幅度涨速
    """
    ACCER=SLOPE(CLOSE,N)/CLOSE;
    return ACCER

def ADTM(N=23,M=8):
    """
    ADTM 动态买卖气指标
    """
    DTM=IF(OPEN<=REF(OPEN,1),0,MAX((HIGH-OPEN),(OPEN-REF(OPEN,1))));
    DBM=IF(OPEN>=REF(OPEN,1),0,MAX((OPEN-LOW),(OPEN-REF(OPEN,1))));
    STM=SUM(DTM,N);
    SBM=SUM(DBM,N);
    ADTM=IF(STM>SBM,(STM-SBM)/STM,IF(STM==SBM,0,(STM-SBM)/SBM));
    MAADTM=MA(ADTM,M);
    return ADTM,MAADTM

def ATR(N=14):
    """
    ATR 真实波幅
    """
    MTR=MAX(MAX((HIGH-LOW),ABS(REF(CLOSE,1)-HIGH)),ABS(REF(CLOSE,1)-LOW));
    ATR=MA(MTR,N);
    return MTR,ATR

def DKX(M=10):
    """
    DKX 多空线
    """
    MID=(3*CLOSE+LOW+OPEN+HIGH)/6
    DKX(20*MID+19*REF(MID,1)+18*REF(MID,2)+17*REF(MID,3)+ \
        16*REF(MID,4)+15*REF(MID,5)+14*REF(MID,6)+ \
        13*REF(MID,7)+12*REF(MID,8)+11*REF(MID,9)+ \
        10*REF(MID,10)+9*REF(MID,11)+8*REF(MID,12)+ \
        7*REF(MID,13)+6*REF(MID,14)+5*REF(MID,15)+ \
        4*REF(MID,16)+3*REF(MID,17)+2*REF(MID,18)+REF(MID,20))/210
    MADKX:MA(DKX,M)
    return DKX,MADKX

###趋势型指标
def CHO(N1=10,N2=20,M=6):
    """
    CHO 佳庆指标
    """
    MID=SUM(VOL*(2*CLOSE-HIGH-LOW)/(HIGH+LOW),0);
    CHO=MA(MID,N1)-MA(MID,N2);
    MACHO=MA(CHO,M);
    return CHO,MACHO

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

def DPO(N=20,M=6):
    """
    DPO 区间震荡线
    """
    DPO=CLOSE-REF(MA(CLOSE,N),N/2+1);
    MADPO=MA(DPO,M);
    return DPO,MADPO

def EMV(N=14,M=9):
    """
    EMV 简易波动指标
    """
    VOLUME=MA(VOL,N)/VOL;
    MID=100*(HIGH+LOW-REF(HIGH+LOW,1))/(HIGH+LOW);
    EMV=MA(MID*VOLUME*(HIGH-LOW)/MA(HIGH-LOW,N),N);
    MAEMV=MA(EMV,M);
    return EMV,MAEMV

def MACD(SHORT=12, LONG=26, M=9):
    """
    MACD 指数平滑移动平均线
    """
    DIFF = EMA(CLOSE, SHORT) - EMA(CLOSE, LONG)
    DEA = EMA(DIFF, M)
    MACD = (DIFF - DEA) * 2
    return DIFF,DEA,MACD

def VMACD(SHORT=12, LONG=26, M=9):
    """
    VMACD 量平滑异同平均
    """
    DIF:EMA(VOL,SHORT)-EMA(VOL,LONG)
    DEA:EMA(DIF,MID)
    MACD:DIF-DEA
    return DIF,DEA,MACD

def QACD(N1=12, N2=26, M=9):
    """
    QACD 快速异同平均
    """
    DIF:EMA(CLOSE,N1)-EMA(CLOSE,N2);
    MACD:EMA(DIF,M);
    DDIF:DIF-MACD;
    return DIF,MACD,DDIF

def TRIX(N=12, M=9):
    """
    TRIX 三重指数平均线
    """
    MTR=EMA(EMA(EMA(CLOSE,N),N),N);
    TRIX=(MTR-REF(MTR,1))/REF(MTR,1)*100;
    MATRIX=MA(TRIX,M) ;
    return TRIX,MATRIX

def UOS(N1=7, N2=14,N3=28, M=6):
    """
    UOS 终极指标
    """
    TH=MAX(HIGH,REF(CLOSE,1));
    TL=MIN(LOW,REF(CLOSE,1));
    ACC1=SUM(CLOSE-TL,N1)/SUM(TH-TL,N1);
    ACC2=SUM(CLOSE-TL,N2)/SUM(TH-TL,N2);
    ACC3=SUM(CLOSE-TL,N3)/SUM(TH-TL,N3);
    UOS=(ACC1*N2*N3+ACC2*N1*N3+ACC3*N1*N2)*100/(N1*N2+N1*N3+N2*N3);
    MAUOS=EXPMEMA(UOS,M);
    return UOS,MAUOS

def VPT(N=51, M=6):
    """
    VPT 量价曲线
    """
    VPT=SUM(VOL*(CLOSE-REF(CLOSE,1))/REF(CLOSE,1),N);
    MAVPT=MA(VPT,M);
    return VPT,MAVPT

def WVAD(N=24, M=6):
    """
    WVAD 威廉变异离散量
    """
    WVAD=SUM((CLOSE-OPEN)/(HIGH-LOW)*VOL,N)/10000;
    MAWVAD=MA(WVAD,M);
    return WVAD,MAWVAD

def JS(N=5, M1=5, M2=10, M3=20):
    """
    JS 加速线
    """
    JS=100*(CLOSE-REF(CLOSE,N))/(N*REF(CLOSE,N));
    MAJS1=MA(JS,M1);
    MAJS2=MA(JS,M2);
    MAJS3=MA(JS,M3);
    return JS,MAJS1,MAJS2,MAJS3

def CYE():
    """
    CYE 市场趋势
    """
    MAL=MA(CLOSE,5);
    MAS=MA(MA(CLOSE,20),5);
    CYEL=(MAL-REF(MAL,1))/REF(MAL,1)*100;
    CYES=(MAS-REF(MAS,1))/REF(MAS,1)*100;
    return  CYEL,CYES

def GDX(N=30,M=9):
    """
    GDX 轨道线
    """
    AA=ABS((2*CLOSE+HIGH+LOW)/4-MA(CLOSE,N))/MA(CLOSE,N); 
    轨道=DMA(CLOSE,AA);
    压力线=(1+M/100)*轨道; 
    支撑线=(1-M/100)*轨道;  
    return  轨道,压力线,支撑线

def JLHB(N=7,M=5):
    """
    JLHB 绝路航标
    """
    VAR1=(CLOSE-LLV(LOW,60))/(HHV(HIGH,60)-LLV(LOW,60))*80; 
    B=SMA(VAR1,N,1); 
    VAR2=SMA(B,M,1); 
    绝路航标=IF(CROSS(B,VAR2)*IF(B<40,1,0),50,0); 
    return  B,VAR2,绝路航标

###能量型指标
def BRAR(N=26):
    """
    BRAR 情绪指标
    """
    BR=SUM(MAX(0,HIGH-REF(CLOSE,1)),N)/SUM(MAX(0,REF(CLOSE,1)-LOW),N)*100;
    AR=SUM(HIGH-OPEN,N)/SUM(OPEN-LOW,N)*100;
    return   BR,AR

def CR(N=26,M1=10,M2=20,M3=40,M4=62):
    """
    CR 带状能量线
    """
    MID=REF(HIGH+LOW,1)/2;
    CR=SUM(MAX(0,HIGH-MID),N)/SUM(MAX(0,MID-LOW),N)*100;
    MA1=REF(MA(CR,M1),M1/2.5+1);
    MA2=REF(MA(CR,M2),M2/2.5+1);
    MA3=REF(MA(CR,M3),M3/2.5+1);
    MA4=REF(MA(CR,M4),M4/2.5+1);
    return CR,MA1,MA2,MA3,MA4

def MASS(N1=9,N2=25,M=6):
    """
    MASS 梅斯线
    """
    MASS:SUM(MA(HIGH-LOW,N1)/MA(MA(HIGH-LOW,N1),N1),N2);
    MAMASS:MA(MASS,M);
    return MASS,MAMASS

def PSY(N=12,M=6):
    """
    PSY 心理线
    """
    PSY:COUNT(CLOSE>REF(CLOSE,1),N)/N*100;
    PSYMA:MA(PSY,M);
    return PSY,PSYMA

def VR2(N=26,M=6):
    """
    VR2 成交量变异率
    """
    TH=SUM(IF(CLOSE>REF(CLOSE,1),VOL,0),N);
    TL=SUM(IF(CLOSE<REF(CLOSE,1),VOL,0),N);
    TQ=SUM(IF(CLOSE==REF(CLOSE,1),VOL,0),N);
    VR=100*(TH*2+TQ)/(TL*2+TQ);
    MAVR=MA(VR,M);
    return VR,MAVR

def WAD(N=30):
    """
    WAD 威廉多空力度线
    """
    MIDA=CLOSE-MIN(REF(CLOSE,1),LOW);
    MIDB=IF(CLOSE<REF(CLOSE,1),CLOSE-MAX(REF(CLOSE,1),HIGH),0);
    WAD=SUM(IF(CLOSE>REF(CLOSE,1),MIDA,MIDB),0);
    MAWAD=MA(WAD,M);
    return WAD,MAWAD

def PCNT(N=5):
    """
    PCNT 幅度比
    """
    PCNT=(CLOSE-REF(CLOSE,1))/CLOSE*100;
    MAPCNT=EXPMEMA(PCNT,M);
    return PCNT,MAPCNT

def CYR(N=13,M=5):
    """
    CYR 市场强弱
    """
    DIVE=0.01*EMA(AMOUNT,N)/EMA(VOL,N);
    CYR=(DIVE/REF(DIVE,1)-1)*100;
    MACYR=MA(CYR,M);
    return CYR,MACYR


###均线型指标
def ACD(M=20):
    """
    ACD 升降线
    """
    LC=REF(CLOSE,1);
    DIF=CLOSE-IF(CLOSE>LC,MIN(LOW,LC),MAX(HIGH,LC));
    ACD=SUM(IF(CLOSE==LC,0,DIF),0);
    MAACD=EXPMEMA(ACD,M);
    return ACD,MAACD

def BBI(M1=3,M2=6,M3=12,M4=24):
    """
    BBI 多空均线
    """
    BBI=(MA(CLOSE,M1)+MA(CLOSE,M2)+MA(CLOSE,M3)+MA(CLOSE,M4))/4;
    return BBI

def BBIBOLL(N=11,M=6):
    """
    BBIBOLL 多空布林线
    """
    CV=CLOSE;
    BBIBOLL=(MA(CV,3)+MA(CV,6)+MA(CV,12)+MA(CV,24))/4;
    UPR=BBIBOLL+M*STD(BBIBOLL,N);
    DWN=BBIBOLL-M*STD(BBIBOLL,N);
    return BBIBOLL,UPR,DWN

def ALLIGAT():
    """
    ALLIGAT 鳄鱼线
    """
    NN=(H+L)/2;
    上唇=REF(MA(NN,5),3)
    牙齿=REF(MA(NN,8),5)
    下颚=REF(MA(NN,13),8)
    return 上唇,牙齿,下颚


####路径型指标
def BOLL(N=20, P=2):
    """
    BOLL 布林带
    """
    MID = MA(CLOSE, N)
    UPPER = MID + STD(CLOSE, N) * P
    LOWER = MID - STD(CLOSE, N) * P
    return UPPER, MID, LOWER

def ENE(N=25,M1=6,M2=6):
    """
    ENE 轨道线
    """
    UPPER:(1+M1/100)*MA(CLOSE,N);
    LOWER:(1-M2/100)*MA(CLOSE,N);
    ENE:(UPPER+LOWER)/2;
    return UPPER, LOWER, ENE

def XS(N=13):
    """
    XS 薛斯通道
    """
    VAR2=CLOSE*VOL;
    VAR3=EMA((EMA(VAR2,3)/EMA(VOL,3)+EMA(VAR2,6)/EMA(VOL,6)+EMA(VAR2,12)/EMA(VOL,12)+EMA(VAR2,24)/EMA(VOL,24))/4,N);
    SUP=1.06*VAR3;
    SDN=VAR3*0.94;
    VAR4=EMA(CLOSE,9);
    LUP=EMA(VAR4*1.14,5);
    LDN=EMA(VAR4*0.86,5);
    return SUP, SDN, LUP,LDN



###其他指标
def ASI(M1=26, M2=10):
    """
    ASI 震动升降指标
    """
    LC = REF(CLOSE, 1)
    AA = ABS(HIGH - LC)
    BB = ABS(LOW - LC)
    CC = ABS(HIGH - REF(LOW, 1))
    DD = ABS(LC - REF(OPEN, 1))
    R = IF((AA > BB) & (AA > CC), AA + BB / 2 + DD / 4, IF((BB > CC) & (BB > AA), BB + AA / 2 + DD / 4, CC + DD / 4))
    X = (CLOSE - LC + (CLOSE - OPEN) / 2 + LC - REF(OPEN, 1))
    SI = X * 16 / R * MAX(AA, BB)
    ASI = SUM(SI, M1)
    ASIT = MA(ASI, M2)
    return ASI, ASIT


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


def DPO(M1=20, M2=10, M3=6):
    DPO = CLOSE - REF(MA(CLOSE, M1), M2)
    MADPO = MA(DPO, M3)
    return DPO, MADPO


def TRIX(M1=12, M2=20):
    TR = EMA(EMA(EMA(CLOSE, M1), M1), M1)
    TRIX = (TR - REF(TR, 1)) / REF(TR, 1) * 100
    TRMA = MA(TRIX, M2)
    return TRIX, TRMA
   
def LON(N=10):
    """
    LON 龙系长线
    """
    LC = REF(CLOSE,1);
    VID = SUM(VOL,2)/(((HHV(HIGH,2)-LLV(LOW,2)))*100);
    RC = (CLOSE-LC)*VID;
    LONG = SUM(RC,0);
    DIFF = SMA(LONG,10,1);
    DEA = SMA(LONG,20,1);
    LON = DIFF-DEA;
    LONMA = MA(LON,N);
    return LON ,LONMA

def SHT(N=5):
    """
    SHT 龙系短线
    """
    VAR1=MA((VOL-REF(VOL,1))/REF(VOL,1),5);
    VAR2=(CLOSE-MA(CLOSE,24))/MA(CLOSE,24)*100;
    SHT= VAR2*(1+VAR1);
    SHTMA= MA(SHT,N);
    return SHT,SHTMA

def ZLJC():
    """
    ZLJC 主力进出
    """
    VAR1=(CLOSE+LOW+HIGH)/3; 
    VAR2=SUM(((VAR1-REF(LOW,1))-(HIGH-VAR1))*VOL/100000/(HIGH-LOW),0); 
    VAR3=EMA(VAR2,1); 
    JCS=VAR3; 
    JCM=MA(VAR3,12); 
    JCL=MA(VAR3,26);
    return JCS,JCM,JCL

def ZLMM():
    """
    ZLMM 主力买卖
    """
    LC =REF(CLOSE,1);
    RSI2=SMA(MAX(CLOSE-LC,0),12,1)/SMA(ABS(CLOSE-LC),12,1)*100;
    RSI3=SMA(MAX(CLOSE-LC,0),18,1)/SMA(ABS(CLOSE-LC),18,1)*100;
    MMS=MA(3*RSI2-2*SMA(MAX(CLOSE-LC,0),16,1)/SMA(ABS(CLOSE-LC),16,1)*100,3);
    MMM=EMA(MMS,8);
    MML=MA(3*RSI3-2*SMA(MAX(CLOSE-LC,0),12,1)/SMA(ABS(CLOSE-LC),12,1)*100,5);
    return MMS,MMM,MML

def SLZT():
    """
    SLZT 神龙在天
    """
    白龙= MA(CLOSE,125);
    黄龙=白龙+2*STD(CLOSE,170);
    紫龙=白龙-2*STD(CLOSE,145);
    VAR2=HHV(HIGH,70);
    VAR3=HHV(HIGH,20);
    红龙= VAR2*0.83;
    蓝龙= VAR3*0.91;
    return 白龙,黄龙,紫龙,红龙,蓝龙

def CYC(P1=5, P2=13, P3=34):
    """
    CYC 成本均线
    """    
    VAR1 = (CLOSE+OPEN)/200
    VAR2 = (3*HIGH+LOW+OPEN+2*CLOSE)/7
    VAR3 = SUM((CLOSE+OPEN) * VOL /2, P1)/VAR1/100
    VAR4 = SUM((CLOSE+OPEN) * VOL /2, P2)/VAR1/100
    VAR5 = SUM((CLOSE+OPEN) * VOL /2, P3)/VAR1/100
    CYC5 = DMA(VAR2, VOL/VAR3)
    CYC13 = DMA(VAR2, VOL/VAR4)
    CYC34 = DMA(VAR2, VOL/VAR5)
    return CYC5, CYC13, CYC34

def CYS():
    """
    CYS 市场盈亏
    """
    CYC13=0.01*EMA(AMOUNT,13)/EMA(VOL,13);
    CYS=(CLOSE-CYC13)/CYC13*100;
    return CYS

def CYW():
    """
    CYW 主力控盘
    """
    VAR1=CLOSE-LOW;
    VAR2=HIGH-LOW;
    VAR3=CLOSE-HIGH;
    VAR4=IF(HIGH>LOW,(VAR1/VAR2+VAR3/VAR2)*VOL,0);
    CYW= SUM(VAR4,10)/10000
    return CYW

def CJDX():
    """
    CJDX 超级短线
    """
    VAR1=(2*CLOSE+HIGH+LOW)/4;
    VAR2=EMA(EMA(EMA(VAR1,4),4),4);
    J= (VAR2-REF(VAR2,1))/REF(VAR2,1)*100
    D= MA(J,3);
    K= MA(J,1);
    return J,D,K

def LHXJ():
    """
    LHXJ 猎狐先觉
    """
    VAR1=(CLOSE*2+HIGH+LOW)/4;
    VAR2=EMA(VAR1,13)-EMA(VAR1,34);
    VAR3=EMA(VAR2,5);
    主力弃盘=(-2)*(VAR2-VAR3)*3.8;
    主力控盘= 2*(VAR2-VAR3)*3.8;
    return 主力弃盘,主力控盘

def LYJH():
    """
    LYJH 猎鹰歼狐
    """
    VAR1=(HHV(HIGH,36)-CLOSE)/(HHV(HIGH,36)-LLV(LOW,36))*100;
    机构做空能量线= SMA(VAR1,2,1);
    VAR2=(CLOSE-LLV(LOW,9))/(HHV(HIGH,9)-LLV(LOW,9))*100;
    机构做多能量线= SMA(VAR2,5,1)-8;
    LH=M;
    LH1= M1;
    return 机构做空能量线,机构做多能量线,LH,LH1

def JFZX(N=30):
    """
    JFZX 飓风智能中线
    """
    VAR2=SUM(IF(CLOSE>OPEN,VOL,0),N)/SUM(VOL,N)*100;
    VAR3=100-SUM(IF(CLOSE>OPEN,VOL,0),N)/SUM(VOL,N)*100;
    多头力量=VAR2;
    空头力量=VAR3;
    多空平衡= 50;
    return 多头力量,空头力量,多空平衡


#计算股票今日实时量比，代码贡献蔣曉強
def QRR(VOL):
    QR = VOL/REF(MA(VOL,5),1)
    DT= dt.datetime.now().strftime('%Y-%m-%d 15:00')
    qrr = REFDATE(QR,DT)       
    return round(qrr, 2)

#def WINNER():
#    WWW_999=IF(LOW>CLOSE,0,IF(HIGH<CLOSE,1,(CLOSE-LOW+0.01)/(HIGH-LOW+0.01)))
#    winner=DMA(WWW_999,VOL/hgs.CAPITAL)*100
#    return winner
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