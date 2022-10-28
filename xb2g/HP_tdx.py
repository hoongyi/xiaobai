# -*- coding: utf-8 -*-
#pytdx小白量化框架数据接口
##pip install pytdx
#买<零基础搭建量化投资系统>,送小白量化软件源代码。
#独狼荷蒲qq:2775205
#小白量化中文PythonTkinter群:983815766
#电话微信:18578755056
#版本：Ver1.04
#最后修改日期:2021年12月9日
import datetime as dt
import pandas as pd
from pytdx.hq import TdxHq_API
from pytdx.exhq import TdxExHq_API, TDXParams
from pytdx.config.hosts import hq_hosts

global tdxapiex

def exhq(ip='59.36.9.44',port=7711):
    global tdxapiex
    ex_api = TdxExHq_API(auto_retry=True, raise_exception=False)
    try:
        is_tdx_ex_connect = ex_api.connect(ip, port, time_out=30)
    except Exception as e:
        print('time out to connect to pytdx')
        print(e)
#    if is_tdx_ex_connect is not False:# 失败了返回False，成功了返回地址
#        print('connect to pytdx extend api successful')
#    else:
#        ex_api=None
    tdxapiex=ex_api
    return ex_api


global tdxapi,servers,hqhosts
global hqstop
hqstop=False
hqhosts=[]
tdxapi=None
global scode #股票代码
scode=''
global smarket #股票市场
smarket=0
global Cw
global Code,Market,Setcode,Name,Py
global Totalcapital,Capital


servers2=['59.173.18.140',\
         '119.147.212.81',\
         '183.60.224.178',\
         '183.60.224.178',\
         'tdx.xmzq.com.cn',\
         '58.23.131.163',\
         '218.6.170.47',\
         '123.125.108.14',\
         '59.110.61.176',\
         '106.14.76.29',\
         '139.196.174.113',\
         '139.196.175.118',\
         '120.77.76.11',\
         '180.153.18.170']

servers=['180.153.18.171',\
         '218.6.170.55',\
         '58.67.221.146',\
         '103.24.178.242',\
         '114.80.63.35',\
         '180.153.39.51',\
         '123.125.108.23',\
         '123.125.108.24',\
         '114.80.63.12',\
         '61.147.174.2',\
         '36.152.49.226',\
         '218.98.6.162',\
         '218.201.105.52',\
         '202.108.253.130',\
         '180.153.18.170']

#tdx接口初始化
def TdxInit(ip='59.173.18.140',port=7709):
    global tdxapi
    tdxapi = TdxHq_API(heartbeat=True)
    result=tdxapi.connect(ip, port)
    if result==None:
        return None
    return tdxapi

def 获取日线数据 (nCategory=4,nMarket = 0,code='000776',\
                    nStart=0, nCount=500):
    global tdxapi
    nMarket=get_market(code)
    result =tdxapi.get_security_bars(nCategory, nMarket,code, nStart, nCount)
    df=tdxapi.to_df(result)
    
    return df

def 连接通达信(code1,已经连接):
    global tdxapi
    if(已经连接<1):
        tdxapi=TdxInit(ip='183.60.224.178',port=7709)
    df=获取日线数据 (code=code1)
    return df




def 获取当天实时tick(code,已经连接,nStart):#成功
    global tdxapi
    if(已经连接<1):
        tdxapi=TdxInit(ip='183.60.224.178',port=7709)
    df=get_transaction_data(nMarket=0, code=code,\
                                        nStart=nStart, nCount=10000)
    df1 = pd.DataFrame(df)
    return df1



def 获取历史的tick(code,已经连接,nStart,date):#data不是‘’的类型，别搞错   
    global tdxapi
    if(已经连接<1):
        tdxapi=TdxInit(ip='183.60.224.178',port=7709)
    df=get_history_transaction_data(nMarket = 0,code=code,\
                    nStart=nStart, nCount=5000,date=date)
    df1 = pd.DataFrame(df)
    return df1


def 获取通达信某股的tick(code,已经连接,nStart):
    a=0
    df1=获取当天实时tick(code=code,已经连接=已经连接,nStart=0)
    if(df1['time'][0]!='09:25'):
        a=1
        df2=获取当天实时tick(code=code,已经连接=已经连接,nStart=len(df1['time']))
        if(str(df2['time'][0])!='09:25'):
            a=2      
            df3=获取当天实时tick(code=code,已经连接=已经连接,nStart=(len(df1['time'])+len(df2['time'])))
            if(str(df3['time'][0])!='09:25'):
                a=3      
                df4=获取当天实时tick(code=code,已经连接=已经连接,nStart=len(df1['time'])+len(df2['time'])+len(df3['time']))
                
                                
    if(a==0):result = df1
    if(a==1):result = df2.append(df1,ignore_index=True)
    if(a==2):
        result = df3.append(df2,ignore_index=True)
        result = result.append(df1,ignore_index=True)
    if(a==3):
        result = df4.append(df3,ignore_index=True)
        result = result.append(df2,ignore_index=True)
        result = result.append(df1,ignore_index=True)        

    return result



def 获取某股竞价数据(code,已经连接,nStart):
    if(已经连接<1):
        
        aa=获取通达信某股的tick(code,已经连接=0,nStart=nStart)
        bb=aa['vol'][0]*aa['price'][0]

    if(已经连接>0):
        
        aa=获取通达信某股的tick(code,已经连接=1,nStart=nStart)
        bb=aa['vol'][0]*aa['price'][0]

    return bb*0.01




#tdx接口初始化
def TdxInit2():
    global tdxapi,servers,hqhosts
    global hqstop
    tdxapi = TdxHq_API(heartbeat=True)
    for i in range(len(servers)):
        hq_hosts.insert(0,('新增',servers[i],7709))
    result=None
    hqhosts=hq_hosts
    #print(len(hq_hosts))
    i=0
    while result==False and i<len(hqhosts) and hqstop==False:
        result=tdxapi.connect(hqhosts[i][1], hqhosts[i][2])
        i+=1
        if i>10:
            break
    if result==None:
        return None
    return tdxapi

def tdx_ping_future(ip, port=7709, type_='stock'):
    apix = TdxExHq_API()
    __time1 = dt.datetime.now()
    try:
       with apix.connect(ip, port, time_out=0.7):
            res = apix.get_instrument_count()
            if res is not None:
                if res > 40000:
                    return dt.datetime.now() - __time1
                else:
                    #print('️Bad FUTUREIP REPSONSE {}'.format(ip))
                    return dt.timedelta(9, 9, 0)
            else:
                #print('️Bad FUTUREIP REPSONSE {}'.format(ip))
                return dt.timedelta(9, 9, 0)
    #
    except Exception as e:
        pass
        #print('BAD RESPONSE {}'.format(ip))
        return dt.timedelta(9, 9, 0)


def disconnect():
    global tdxapi
    tdxapi.disconnect()
    tdxapi=None
    return None


def get_market(code):
    c=code[0:1]
    y=0
    if c=='6' or c=='5':
        y=1
    return y

#获取股票代码表
def GetSecurityList(nMarket = 0):
    global tdxapi
    #nMarket = 0    # 0 - 深圳  1 - 上海
    nStart = 0
    
    m=tdxapi.get_security_count(nMarket)
    df=tdxapi.to_df(tdxapi.get_security_list(nMarket, nStart))
    df=pd.DataFrame(columns = ['code','name','pre_close']) 
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    while nStart<m:
        result = tdxapi.get_security_list(nMarket, nStart)
        df2=tdxapi.to_df(result)
        df=df.append( df2,ignore_index=True)            
        nStart=nStart+1000
    return df

#获取深圳股票代码表
def getSZ():
    base=GetSecurityList(0)
    base.code = base.code.fillna('')
    base.to_csv('./data/sz.csv' , encoding= 'gbk')
    return base

#获取上海股票代码表
def getSH():
    base=GetSecurityList(1)
    base.code = base.code.fillna('')
    base.to_csv('./data/sh.csv' , encoding= 'gbk')
    return base

#日线级别k线获取函数
def get_k_data(code='600030',ktype='D',start='1991-01-01',end='2021-10-22',\
               index=False,autype='qfq'):
    global tdxapi,scode,smarket
    global Cw
    global Code,Market,Setcode,Name,Py
    global Totalcapital,Capital    
    scode=code
    smarket=get_market(code)
    Cw=readbase(nMarket=smarket,code=scode)
    df1 = tdxapi.get_k_data(code, start, end)
    df1=df1.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    df1.rename(columns={'vol':'volume'}, inplace = True)
    df1['code']=code
    df1['ktype']=ktype
    df1['smarket']=smarket
    df1['capital']=Capital
    df1['liutongguben']=int(Cw['liutongguben'])
    df1['totalcapital']=Totalcapital    
    return df1


#获取除权除息数据
def get_xdxr_info(nMarket = 0,code='000001'):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    #nMarket = 0    # 0 - 深圳  1 - 上海
    result= tdxapi.get_xdxr_info(nMarket, code)
    df=tdxapi.to_df(result)
    df['code']=code
    df['market']=nMarket    
    return df

#获取财物数据
def readbase(nMarket =-1,code='000776'):
    global Cw
    global Code,Market,Setcode,Name,Py
    global Totalcapital,Capital
    if nMarket<0:
        nMarket=get_market(code)
    Code=code
    Market=nMarket
    Cw= tdxapi.get_finance_info(nMarket, code)
    Totalcapital=Cw['zongguben']
    Capital=int(Cw['liutongguben']/100)
    return Cw

#(nCategory, nMarket, sStockCode, nStart, nCount) 
#获取市场内指定范围的证券K 线， 
#指定开始位置和指定K 线数量，指定数量最大值为800。 
#参数： 
#nCategory -> K 线种类 
#0 5 分钟K 线 
#1 15 分钟K 线 
#2 30 分钟K 线 
#3 1 小时K 线 
#4 日K 线 
#5 周K 线 
#6 月K 线 
#7 1 分钟 
#8 1 分钟K 线 
#9 日K 线 
#10 季K 线 
#11 年K 线 
#nMarket -> 市场代码0:深圳，1:上海 
#sStockCode -> 证券代码； 
#nStart -> 指定的范围开始位置； 
#nCount -> 用户要请求的K 线数目，最大值为800。
def get_security_bars(nCategory=4,nMarket = -1,code='000776',\
                    nStart=0, nCount=240):
    global tdxapi,scode,smarket
    global Cw
    global Code,Market,Setcode,Name,Py
    global Totalcapital,Capital
    scode=code
    if nMarket == -1:
        nMarket=get_market(code)
    smarket=nMarket
    Cw=readbase(nMarket=nMarket,code=scode)
    result =tdxapi.get_security_bars(nCategory, nMarket,code, nStart, nCount)
    df=tdxapi.to_df(result)
    if nCategory in [0,1,2,3,7,8,]:
        a=[x[0:10] for x in df.datetime]
        df.insert(0,'date',a)
    elif 'datetime' in  df.columns:
        df['date']=df.datetime
    if 'vol' in  df.columns:
        df['volume']=df.vol
        
    df['code']=code
    df['market']=nMarket
    df['category']=nCategory
    df['capital']=Capital
    df['liutongguben']=int(Cw['liutongguben'])
    df['totalcapital']=Totalcapital
    return df

def get_all_data(nCategory=4,nMarket = 0,code='000776'):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    data=[]
    for i in range(10):
          data+=tdxapi.get_security_bars(nCategory, nMarket,code,(9-i)*800,800)
    df=tdxapi.to_df(data)
    df['date']=df['datetime']
    df['volume']=df['vol']
    df['code']=code
    df['market']=nMarket
    df['category']=nCategory    
    return df

def get_index_bars(nCategory=4,nMarket = 1,code='000001',\
                    nStart=0, nCount=240):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    result =tdxapi.get_index_bars(nCategory, nMarket,code, nStart, nCount)
    df=tdxapi.to_df(result)
    return df

#"查询分时行情"
def get_minute_time_data(nMarket = 0,code='000776'):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    #nMarket = 0    # 0 - 深圳  1 - 上海
    result= tdxapi.get_minute_time_data(nMarket, code)
    df=tdxapi.to_df(result)
    df['code']=code
    df['market']=nMarket
    return df


#"查询历史分时行情
def get_history_minute_time_data(nMarket = 0,code='000776',date=20190829):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    #nMarket = 0    # 0 - 深圳  1 - 上海
    result= tdxapi.get_history_minute_time_data(nMarket, code,date)
    df=tdxapi.to_df(result)
    df['code']=code
    df['market']=nMarket
    return df

#查询分笔数据
def get_transaction_data(nMarket = 0,code='000776',\
                    nStart=0, nCount=5000):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    nMarket=get_market(code)
    result= tdxapi.get_transaction_data(nMarket, code,nStart, nCount)
    df=tdxapi.to_df(result)
    df['code']=code
    df['market']=nMarket
    return df    
    
#查询历史分时成交
def get_history_transaction_data(nMarket = 0,code='000776',\
                    nStart=0, nCount=5000,date=20170209):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    nMarket=get_market(code)
    result= tdxapi.get_history_transaction_data(nMarket, code,nStart,\
                                                nCount,date)
    df=tdxapi.to_df(result)
    df['code']=code
    df['market']=nMarket    
    return df   

#查询公司信息目录
def get_company_info_category(nMarket = 0,code='000776'):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    #nMarket = 0    # 0 - 深圳  1 - 上海
    result= tdxapi.get_company_info_category(nMarket, code)
    df=tdxapi.to_df(result)
    df['code']=code
    df['market']=nMarket    
    return df

#查询公司信息目录
def get_F10(code='000776',item='股东研究'):
    global tdxapi,scode
    scode=code
    #nMarket = 0    # 0 - 深圳  1 - 上海
    nMarket=get_market(code)
    result= tdxapi.get_company_info_category(nMarket, code)
    df=tdxapi.to_df(result)
    df2=df[df.name==item]
    f=df2.iat[0,1]
    ls=df2.iat[0,2]
    le=df2.iat[0,3]
    result= tdxapi.get_company_info_content(nMarket,code,\
                                            f,ls,le)
    return result

#读取公司信息-最新提示
def get_company_info_content(nMarket = 0,code='000776',filename='000776.txt',
                             start=0, length=13477):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    nMarket=get_market(code)
    result= tdxapi.get_company_info_content(nMarket,code,\
                                            filename,start,length)
    return result


#读取财务信息
def get_finance_info(nMarket = 0,code='000776'):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    nMarket=get_market(code)
    result= tdxapi.get_finance_info(nMarket, code)
    df=tdxapi.to_df(result)
    df['code']=code
    df['market']=nMarket    
    return df    


#日线级别k线获取函数
def get_k_data2(code='600030', start='2005-07-01', end='2021-10-22'):
    global tdxapi,scode,smarket
    global Cw
    global Code,Market,Setcode,Name,Py
    global Totalcapital,Capital    
    scode=code
    smarket=get_market(code)
    Cw=readbase(nMarket=smarket,code=scode)
    df= tdxapi.get_k_data(code,start,end)
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='') 
    df.rename(columns={'vol':'volume'}, inplace = True)
    df['code']=code
    df['market']=smarket
    df['capital']=Capital
    df['liutongguben']=int(Cw['liutongguben'])
    df['totalcapital']=Totalcapital
    
    return df


#获取多个证券的盘口五档报价数据 
#stocks = api.get_security_quotes([(0, "000002"), (1, "600300")])
#stocks = api.get_security_quotes([(0, "000002")])
def get_security_quotes(code='000776'):
    global tdxapi,scode,smarket
    scode=code
    nMarket = get_market(code)
    smarket=nMarket    
    result= tdxapi.get_security_quotes(nMarket, code)
    return result    

def get_security_quotes2(market=0,code='000776'):
    global tdxapi,scode,smarket
    scode=code
    smarket=market
    result= tdxapi.get_security_quotes(market, code)
    return result    

def get_hq(codes=[ "000001","600000"]):
    global tdxapi
    mk=get_market(codes[0])
    result= tdxapi.get_security_quotes(mk, codes[0])
    df2=tdxapi.to_df(result)
    for  i in range(1,len(codes)):
        mk=get_market(codes[i])
        result= tdxapi.get_security_quotes(mk,codes[i])
        df=tdxapi.to_df(result)
        df2=df2.append( df,ignore_index=True)    
    df2.to_csv('./data/hq.csv' , encoding= 'gbk')
    return df2

def get_hq2(codes=[[0,"000001"],[1,"600000"]]):
    global tdxapi
    result= tdxapi.get_security_quotes(codes)
    df2=tdxapi.to_df(result)
    return df2

#获取全部深圳行情
def get_szhq():
    global tdxapi
    df1=getSZ()
    codes=list(df1.code)
    result= tdxapi.get_security_quotes(0, codes[0])
    df2=tdxapi.to_df(result)
    cs=[]
    for  i in range(1,len(codes)):
        cs.append((0,codes[i]))
        if i%100==0:
            result= tdxapi.get_security_quotes(cs)
            df=tdxapi.to_df(result)
            df2=df2.append( df,ignore_index=True)      
            cs=[]
    result= tdxapi.get_security_quotes(cs)
    df=tdxapi.to_df(result)
    df2=df2.append( df,ignore_index=True)              
    df2.to_csv('./data/shhq.csv' , encoding= 'gbk')
    return df2

#获取全部上海行情
def get_shhq():
    global tdxapi
    df1=getSH()
    codes=list(df1.code)
    result= tdxapi.get_security_quotes(1, codes[0])
    df2=tdxapi.to_df(result)
    cs=[]
    for  i in range(1,len(codes)):
        cs.append((1,codes[i]))
        if i%100==0:
            result= tdxapi.get_security_quotes(cs)
            df=tdxapi.to_df(result)
            df2=df2.append( df,ignore_index=True)      
            cs=[]
    result= tdxapi.get_security_quotes(cs)
    df=tdxapi.to_df(result)
    df2=df2.append( df,ignore_index=True)              
    df2.to_csv('./data/shhq.csv' , encoding= 'gbk')
    return df2

#获取全部深圳财务数据
def get_szcw():
    global tdxapi
    df1=getSZ()
    codes=list(df1.code)
    result= tdxapi.get_finance_info(0, '000001')
    df2=tdxapi.to_df(result)
    for  code in codes:
        result= tdxapi.get_finance_info(0,code)
        df=tdxapi.to_df(result)
        df2=df2.append( df,ignore_index=True)    
    df2.to_csv('./data/szcw.csv' , encoding= 'gbk')
    return df2

#获取全部上海财务数据
def get_shcw():
    global tdxapi
    df1=getSH()
    codes=list(df1.code)
    result= tdxapi.get_finance_info(1, '600000')
    df2=tdxapi.to_df(result)
    for  code in codes:
        result= tdxapi.get_finance_info(1,code)
        df=tdxapi.to_df(result)
        df2=df2.append( df,ignore_index=True)   
    df2.to_csv('./data/shcw.csv' , encoding= 'gbk')
    return df2

#'深圳股票代码表'
def szcode():
    #'深圳股票代码'
    sz=getSZ()
    sz['type']=''
    sz['kind']=''
    sz['market']=0
    sz['type2']=10
    for i in range(len(sz)):
        #print(i,sh['code'][i])
        x=int(sz['code'][i])
        if x<2000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='A股股票'
            sz.loc[i,'type2']=1
        elif x>=2000 and x<31000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='中小板'
            sz.loc[i,'type2']=2
        elif x>=31000 and x<80000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='权证'
            sz.loc[i,'type2']=8
        elif x>=80000 and x<100000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='配股'
            sz.loc[i,'type2']=1
        elif x>=100000 and x<150000:
            sz.loc[i,'type']='证券'    
            sz.loc[i,'kind']='债券'
            sz.loc[i,'type2']=6
        elif x>=150000 and x<200000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='基金'   
            sz.loc[i,'type2']=7
        elif x>=200000 and x<300000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='B股股票'
            sz.loc[i,'type2']=5
        elif x>=300000 and x<380000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='创业板'
            sz.loc[i,'type2']=3
        elif x>=390000 and x<400000:
            sz.loc[i,'type']='指数板块'
            sz.loc[i,'kind']='指数'         
            sz.loc[i,'type2']=0
        elif x>=400000 and x<500000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='三板'  
            sz.loc[i,'type2']=1            
        elif x>=500000 and x<600000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='基金'    
            sz.loc[i,'type2']=7
        elif x>=600000 and x<800000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='A股股票'  
            sz.loc[i,'type2']=1
        elif x>=800000 and x<900000:
            sz.loc[i,'type']='指数板块'
            sz.loc[i,'kind']='板块'       
            sz.loc[i,'type2']=0
        elif x>=900000 and x<999000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='B股股票'  
            sz.loc[i,'type2']=5
        elif x>=999000 :
            sz.loc[i,'type']='指数板块'  
            sz.loc[i,'kind']='指数'  
            sz.loc[i,'type2']=0
    sz.to_csv('./data/sz.csv' , encoding= 'gbk')    
    return sz

#上海股票代码表
def shcode():
    #上海股票代码
    sh=getSH()
    sh['type']=''
    sh['kind']=''
    sh['market']=1
    sh['type2']=10
    for i in range(len(sh)):
        #print(i,sh['code'][i])
        x=int(sh['code'][i])
        if x<1000:
            sh.loc[i,'type']='指数板块'
            sh.loc[i,'kind']='指数'
            sh.loc[i,'type2']=0
        elif x>=1000 and x<30000:
            sh.loc[i,'type']='证券'
            sh.loc[i,'kind']='债券'
            sh.loc[i,'type2']=6
        elif x>=30000 and x<200000:
            sh.loc[i,'type']='证券'  
            sh.loc[i,'kind']='债券'  
            sh.loc[i,'type2']=6
        elif x>=200000 and x<500000:
            sh.loc[i,'type']='证券'              
            sh.loc[i,'kind']='债券'  
            sh.loc[i,'type2']=6
        elif x>=500000 and x<600000:
            sh.loc[i,'type']='证券'       
            sh.loc[i,'kind']='基金'
            sh.loc[i,'type2']=7
        elif x>=600000 and x<700000:
            sh.loc[i,'type']='证券'  
            sh.loc[i,'kind']='A股股票'  
            sh.loc[i,'type2']=1
        elif x>=700000 and x<750000:
            sh.loc[i,'type']='证券'  
            sh.loc[i,'kind']='新股申购'  
            sh.loc[i,'type2']=1
        elif x>=750000 and x<800000:
            sh.loc[i,'type']='其他'  
            sh.loc[i,'kind']='其他'  
            sh.loc[i,'type2']=9
        elif x>=800000 and x<900000:
            sh.loc[i,'type']='指数板块'              
            sh.loc[i,'kind']='板块'
            sh.loc[i,'type2']=0
        elif x>=900000 and x<999000:
            sh.loc[i,'type']='证券'  
            sh.loc[i,'kind']='B股股票'  
            sh.loc[i,'type2']=5
        elif x>=999000 :
            sh.loc[i,'type']='指数板块'  
            sh.loc[i,'kind']='指数'  
            sh.loc[i,'type2']=0
        #print(i,sh['code'][i], sh['type'][i])
    sh.to_csv('./data/sh.csv' , encoding= 'gbk')
    return sh


#获取深圳股票代码表
def get_szcode2(t=''):
    base=pd.read_csv('./data/sz.csv' , encoding= 'gbk')
    base= base.drop('Unnamed: 0', axis=1)
    if t!='':
        base=base[base['type']==t]
        base=base.reset_index(drop=True)
    base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]
    return base

#获取上海股票代码表
def get_shcode2(t=''):
    base=pd.read_csv('./data/sh.csv' , encoding= 'gbk')
    base= base.drop('Unnamed: 0', axis=1)
    if t!='':
        base=base[base['type']==t]    
        base=base.reset_index(drop=True)
    base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]
    return base


# 板块相关参数
BLOCK_DEFAULT = "block.dat"
BLOCK_SZ = "block_zs.dat"
BLOCK_FG = "block_fg.dat"
BLOCK_GN = "block_gn.dat"

#获取板块信息
def get_block(bk=BLOCK_DEFAULT):
    global tdxapi
    result= tdxapi.get_and_parse_block_info(bk)
    df=tdxapi.to_df(result)
    df.to_csv('./data/'+bk+'.csv' , encoding= 'gbk')
    return df

#获取本地板块信息
def get_block2(bk=BLOCK_DEFAULT):
    global tdxapi
    base=pd.read_csv('./data/'+bk+'.csv', encoding= 'gbk')
    base= base.drop('Unnamed: 0', axis=1)
    base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]    
    return base

def getblock(bk=''):
    df=get_block("block.dat")
    bk2=list(df['blockname'])
    bk3=set(bk2)
    bk2=list(bk3)
    if bk in bk2:
        df=df[df.blockname==bk]
        df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
        return df
    df=get_block("block_zs.dat")
    bk2=list(df['blockname'])
    bk3=set(bk2)
    bk2=list(bk3)
    if bk in bk2:
        df=df[df.blockname==bk]
        df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
        return df
    df=get_block("block_fg.dat")
    bk2=list(df['blockname'])
    bk3=set(bk2)
    bk2=list(bk3)
    if bk in bk2:
        df=df[df.blockname==bk]
        df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
        return df
    df=get_block("block_gn.dat")
    bk2=list(df['blockname'])
    bk3=set(bk2)
    bk2=list(bk3)
    df=df[df.blockname==bk]
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
    return df


#返回板块中的股票
def getblock2(bk=''):
    df=getblock(bk)
    if len(df) == 0:
        return []
    else:
        bks2=df['code']
        bks=list(bks2)
        return bks

#返回股票所属板块
def getblock3(code=''):
    df=get_block("block.dat")
    df2=get_block("block_zs.dat")
    df=df.append(df2)
    df2=get_block("block_fg.dat")
    df=df.append(df2)
    df2=get_block("block_gn.dat")
    df=df.append(df2)
    df=df[df.code==code]
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
    bk2=list(df['blockname'])
    bk3=set(bk2)
    bk2=list(bk3)
    return bk2


#返回通达信股票代码格式
def tdxcode(code):
    market=get_market(code)
    return (market,code)

#返回通达信板块代码格式
def tdxcodes(codes):
    bk=[]
    for code in codes:
        market=get_market(code)
        bk.append((market,code))
    return bk

#自选股数据转通达信股票列表
def getzxg(z):
    z2=z.split(chr(10))
    l=[]
    for i in range(1,len(z2)):
        z3=z2[i]
        l.append((int(z3[0:1]),z3[1:9]))
    return l

def getzxgfile(file='ZXG.blk'):
    f = open(file,'r')
    z=f.read()
    f.close()
    return getzxg(z)

#通达信股票列表转自选股数据转
def putzxg(l):
    s=''
    for i in range(len(l)):
        l2,l3=l[i]
        s=s+chr(10)+str(l2)+l3
    return s

def putzxgfile(l,file='ZXG2.blk'):
    f = open(file,'w')
    s=putzxg(l)
    f.write(s)
    f.close()
    return s

##日线后复权
def data_hfq(market = 1,code='600080'):
     # 从服务器获取该股的股本变迁数据
    category = {
        '1': '除权除息', '2': '送配股上市', '3': '非流通股上市', '4': '未知股本变动', '5': '股本变化',
        '6': '增发新股', '7': '股份回购', '8': '增发新股上市', '9': '转配股上市', '10': '可转债上市',
        '11': '扩缩股', '12': '非流通股缩股', '13': '送认购权证', '14': '送认沽权证'}
    data = get_xdxr_info(market, code)
    data = data \
        .assign(date=pd.to_datetime(data[['year', 'month', 'day']])) \
        .drop(['year', 'month', 'day'], axis=1) \
        .assign(category_meaning=data['category'].apply(lambda x: category[str(x)])) \
        .assign(code=str(code)) \
        .rename(index=str, columns={'panhouliutong': 'liquidity_after',
                                    'panqianliutong': 'liquidity_before', 'houzongguben': 'shares_after',
                                    'qianzongguben': 'shares_before'}) \
        .set_index('date', drop=False, inplace=False)
    xdxr_data = data.assign(date=data['date'].apply(lambda x: str(x)[0:10]))  # 该股的股本变迁DF处理完成
    df_gbbq = xdxr_data[xdxr_data['category'] == 1]  # 提取只有除权除息的行保存到DF df_gbbq
    # print(df_gbbq)

    a=get_security_bars(9, market, code, 0, 800)

    # 从服务器读取该股的全部历史不复权K线数据，保存到data表，  只包括 日期、开高低收、成交量、成交金额数据
    data = pd.concat([get_security_bars(9, market, code, (9 - i) * 800, 800) for i in range(10)], axis=0)

    # 从data表加工数据，保存到bfq_data表
    df_code = data \
        .assign(date=pd.to_datetime(data['datetime'].apply(lambda x: x[0:10]))) \
        .assign(code=str(code)) \
        .set_index('date', drop=False, inplace=False) \
        .drop(['year', 'month', 'day', 'hour',
               'minute', 'datetime'], axis=1)
    df_code['if_trade'] = True
    # 不复权K线数据处理完成，保存到bfq_data表

    # 提取info表的category列的值，按日期一一对应，列拼接到bfq_data表。也就是标识出当日是除权除息日的行
    data = pd.concat([df_code, df_gbbq[['category']][df_code.index[0]:]], axis=1)
    # print(data)

    data['date'] = data.index
    data['if_trade'].fillna(value=False, inplace=True)  # if_trade列，无效的值填充为False
    data = data.fillna(method='ffill')  # 向下填充无效值

    # 提取info表的'fenhong', 'peigu', 'peigujia',‘songzhuangu'列的值，按日期一一对应，列拼接到data表。
    # 也就是将当日是除权除息日的行，对应的除权除息数据，写入对应的data表的行。
    data = pd.concat([data, df_gbbq[['fenhong', 'peigu', 'peigujia',
                                  'songzhuangu']][df_code.index[0]:]], axis=1)
    data = data.fillna(0)  # 无效值填空0

    data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu']
                        * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
    data['adj'] = (data['preclose'].shift(-1) / data['close']).fillna(1)[::-1].cumprod()  # 计算每日复权因子
    data['open'] = data['open'] * data['adj']
    data['high'] = data['high'] * data['adj']
    data['low'] = data['low'] * data['adj']
    data['close'] = data['close'] * data['adj']
    data['preclose'] = data['preclose'] * data['adj']

    data = data[data['if_trade']]
    result = data \
        .drop(['fenhong', 'peigu', 'peigujia', 'songzhuangu', 'if_trade', 'category'], axis=1)[data['open'] != 0] \
        .assign(date=data['date'].apply(lambda x: str(x)[0:10]))
    #print(result)
    return result


##复权数据计算
def data_fq2(market = 1,code='600080',fqtype='01'):
    '使用数据库数据进行复权'
    data=get_all_data(4,market, code)
    data['date2']=[x[0:10] for x in data.date.astype(str)]
    data['rc']=data['close'].shift(1)
    data.to_csv('./data/ls1.csv' , encoding= 'gbk')
    xdxr_data=get_xdxr_info(market, code)
    xdxr_data=xdxr_data.fillna(value=0)
    xdxr_data['date']=''
    xdxr_data['av']=1.0
    xdxr_data['ac']=0.0
    xdxr_data['ac2']=0.0
    xdxr_data['rc']=0.0
    av=1.0
    ac=1.0
    print(xdxr_data)
    for i in range(len(xdxr_data)):
        s=str(xdxr_data['year'].iloc[i]).zfill(4)+'-'+str(xdxr_data['month'].iloc[i]).zfill(2)+"-"+str(xdxr_data['day'].iloc[i]).zfill(2)
        print(s)
        xdxr_data['date'].iloc[i]=s
        try:
            xdxr_data['rc'].iloc[i]=list(data[data['date2']==s]['rc'])[0]
        except Exception as e:
            print('\n代码出错:'+str(e)+'\n')            
        if xdxr_data['panhouliutong'].iloc[i]!=0 and xdxr_data['panqianliutong'].iloc[i] !=0:
            xdxr_data['av'].iloc[i]=xdxr_data['panhouliutong'].iloc[i]/xdxr_data['panqianliutong'].iloc[i]
        xdxr_data['ac'].iloc[i]=xdxr_data['fenhong'].iloc[i]/10.0
        if xdxr_data['peigujia'].iloc[i]!=0:
            xdxr_data['ac2'].iloc[i]=xdxr_data['rc'].iloc[i]-(10*xdxr_data['rc'].iloc[i]+xdxr_data['peigujia'].iloc[i]*xdxr_data['peigu'].iloc[i])/(10+xdxr_data['peigu'].iloc[i])

    xdxr_data.to_csv('./data/ls2.csv' , encoding= 'gbk')
    return

def tdx_ping_stk(ip,port,type):
    pass
def tdx_ping100():
    #
    future_ip_list=[]
    stock_ip_list=[]
    data_future = [tdx_ping_future(x['ip'], x['port'], 'future') for x in future_ip_list]
    best_future_ip = future_ip_list[data_future.index(min(data_future))]
    print('\nbest_future_ip',best_future_ip)
    #
    print('')
    data_stock = [tdx_ping_stk(x['ip'], x['port'], 'stock') for x in stock_ip_list]
    best_stock_ip = stock_ip_list[data_stock.index(min(data_stock))]
    print('\nbest_stock_ip',best_stock_ip)
    #
    x=best_stock_ip
    tim=tdx_ping_stk(x['ip'], x['port'], 'stock') 
    x=best_future_ip
    tim2=tdx_ping_future(x['ip'], x['port'], 'future') 
    #
    print('')
    print('股票 stock best_ip',best_stock_ip,tim)
    print('期货 future best_ip',best_future_ip,tim2)
    #
    #best_stock_ip {'ip': '119.147.164.60', 'port': 7709} 0:00:00.258858
    #best_future_ip {'ip': '119.97.185.5', 'port': 7727, 'name': '扩展市场武汉主站1'} 0:00:00.055968
    #
    return best_stock_ip

def 获取日线数据 (nCategory=4,nMarket = 0,code='000776',\
                    nStart=0, nCount=500):
    global tdxapi
    
    nMarket=get_market(code)
    result =tdxapi.get_security_bars(nCategory, nMarket,code, nStart, nCount)
    df=tdxapi.to_df(result)
    
    return df

def 日线数据包含日期段(code,起始日期,结束日期):
    global tdxapi
    nCategory=4
    try:
        df=获取日线数据 (nCategory=nCategory,code=code,nStart=0, nCount=800)
    except:
        tdxapi=TdxInit(ip='183.60.224.178',port=7709)
        df=获取日线数据 (nCategory=nCategory,code=code,nStart=0, nCount=800)
    历史日期表=df['datetime']
    天数=0
    超出范围=0
    for i in range(len(历史日期表)):
        
        if(起始日期>=历史日期表[len(df)-1-i][0:10]):
            超出范围=0
            break
        天数=天数+1
        超出范围=1
    df=df[800-天数:800]
    if(天数==800 and 超出范围==1):
        df1=获取日线数据 (nCategory=nCategory,code=code,nStart=800, nCount=800)
        历史日期表=df1['datetime']
        超出范围=1
        for i in range(len(历史日期表)):
            
            if(起始日期>=历史日期表[len(df)-1-i][0:10]):
                超出范围=1
                break
            天数=天数+1
            超出范围=2
        df1=df1[800-(天数-800):800] 
    if(天数==1600 and 超出范围==2):
        df2=获取日线数据 (nCategory=nCategory,code=code,nStart=天数, nCount=800)
        历史日期表=df2['datetime']
        超出范围=2
        for i in range(len(历史日期表)):
            
            if(起始日期>=历史日期表[len(df)-1-i][0:10]):
                超出范围=2
                break
            天数=天数+1
            超出范围=3
        df2=df2[800-(天数-1600):800]
    if(天数==2400 and 超出范围==3):
        df3=获取日线数据 (nCategory=nCategory,code=code,nStart=天数, nCount=800)
        历史日期表=df3['datetime']
        超出范围=3
        for i in range(len(历史日期表)):
            
            if(起始日期>=历史日期表[len(df)-1-i][0:10]):
                超出范围=3
                break
            天数=天数+1
            超出范围=4
        df3=df3[800-(天数-2400):800]    
    if(天数==3200 and 超出范围==4):
        df4=获取日线数据 (nCategory=nCategory,code=code,nStart=天数, nCount=800)
        历史日期表=df4['datetime']
        超出范围=4
        for i in range(len(历史日期表)):
            
            if(起始日期>=历史日期表[len(df)-1-i][0:10]):
                超出范围=4
                break
            天数=天数+1
            超出范围=5
        df4=df4[800-(天数-3200):800]
    if(天数==4000 and 超出范围==5):
        df5=获取日线数据 (nCategory=nCategory,code=code,nStart=天数, nCount=800)
        历史日期表=df5['datetime']
        超出范围=5
        for i in range(len(历史日期表)):
            
            if(起始日期>=历史日期表[len(df)-1-i][0:10]):
                超出范围=5
                break
            天数=天数+1
            超出范围=6
        df5=df5[800-(天数-4000):800]
    if(超出范围==0):result = df
    if(超出范围==1):result = df1.append(df,ignore_index=True)
    if(超出范围==2):
        result = df2.append(df1,ignore_index=True)
        result = result.append(df,ignore_index=True)
    if(超出范围==3):
        result = df3.append(df2,ignore_index=True)
        result = result.append(df1,ignore_index=True)
        result = result.append(df,ignore_index=True) 
    if(超出范围==4):
        result = df4.append(df3,ignore_index=True)
        result = result.append(df2,ignore_index=True)
        result = result.append(df1,ignore_index=True)
        result = result.append(df,ignore_index=True)
    if(超出范围==5):
        result = df5.append(df4,ignore_index=True)
        result = result.append(df3,ignore_index=True)
        result = result.append(df2,ignore_index=True)
        result = result.append(df1,ignore_index=True)
        result = result.append(df,ignore_index=True)
    result=result.reset_index()
    result=result.drop(labels='index',axis=1)
    历史日期表=result['datetime']
    天数2=0
    
    for i in range(len(历史日期表)):
        
        if(结束日期>=历史日期表[len(历史日期表)-1-i][0:10]):
            
            break
        天数2=天数2+1
    result=result[0:len(result)-天数2]
    result=result.reset_index()
    result=result.drop(labels='index',axis=1)
    return result

    
#测试
if __name__ == '__main__':
    from HP_formula import *
    tdxapi=TdxInit(ip='40.73.76.10',port=7709)
    df=data_hfq(0,'000001')
    print(df)
    print(SLOPE(df.close,10))
    print(SLOPE2(df.close,10))
    #df=data_fq2(0,'000776')
#    bb=get_history_minute_time_data(TDXParams.MARKET_SH, '600519', 20210525)
#    print(bb)
    #pys=hhz.loadhzk2('data/pinyin.csv')
#    getSZ()
#    getSH()
#    tdxapi=TdxInit()
    #cd=get_szcode()
    #cd2=get_shcode()
    #print(cd)
#    cd=cd.append(cd2)
#    cd=cd.reset_index(level=None, drop=True ,col_level=0, col_fill='')
#    cd.to_csv('./data/codes.csv' , encoding= 'gbk')
#    cds={}
#    for i in range(len(cd)):
#        cds[(cd.market[i],cd.code[i])]=cd.name[i]
#    
#    print(cds)
#    df= get_hq2([[0,'000001'],[1,'600030']])
#    print(df)
#    df['zd']=df['price']-df['last_close']  #涨跌
#    df['zdf1']=df['zd']*100/df['last_close']  #涨跌幅
#    df=df.round(2)  #改变符点数小数点后2位
#    df['zdf']=df['zdf1'].astype(str)+'%'
#    df['code2']=['0'*(6-len(x)) + x for x in df.code.astype(str)]
#    df['name']=''
#    for i in range(len(df)):
#        df.loc[i,'name']=cds[(df.loc[i,'market'],df.loc[i,'code2'])]
#
#    df.to_csv('./data/hq.csv' , encoding= 'gbk')
#    aa=get_block(BLOCK_GN)
#    #print(aa)
#    bb=list(aa['blockname'])
#    bb1=set(bb)
#    bb2=list(bb1)
#    print(bb2)
#    bfq_data=get_all_data(9,1, '600030')
#    bfq_data.to_csv('./data/cq1.csv' , encoding= 'gbk')
#    print(bfq_data)
#    xdxr_data=get_xdxr_info(1, '600030')
#    print(xdxr_data)
#    exhq()
#    result= tdxapi.get_finance_info(0, '000001')
#    print(result['gudingzichan'])
#    aa=data_fq()
#    print(aa)
#    aa.to_csv('./data/cq2.csv' , encoding= 'gbk')
#    print(aa.columns)
#    print(get_all_data())
    
#    df=df=get_szhq()
#    print(df.columns)

#    sh=shcode()
#    sz=szcode()
#    print(sh)
#    print(sz)
#    
#    print('深圳股票代码\n')
#    df=get_k_data()
#    print(df)
#    #print(df.columns)
#    sz=getSZ()
#    print(sz)
    
#    sz=get_shcode('A股股票')
#    
#    #sh=sh[sh.type=='A股股票']
#    print(sz)

    df=get_transaction_data()
    print(df)
    获取某股竞价数据('688002',0,0)
#    df=get_xdxr_info(1,'600020')
#    df=get_company_info_category()
#    df=get_index_bars()
#    print(df)  
#    df=TdxExHq_API.get_instrument_quote(0)
#    print(df)
#    df2=get_xdxr_info()
#    print(df2)
#    print('查询公司信息目录')
#    df=get_company_info_category()
#    print(df.name)
#    t=get_F10('600010','最新提示')
#    print(t)
#    txt=get_company_info_content(nMarket = 0,code='000776',filename='000776.txt',\
#                             start=60463, length=16935)
#    print(txt)
#    ex_api=exhq()
#    a=ex_api.get_history_minute_time_data(1,'600030',date='2019-12-16')
#    b=ex_api.get_markets()
#    c=ex_api.to_df(b)
#    print(c)
#    aa=ex_api.get_instrument_info(0, 100)
#    bb=ex_api.to_df(aa)
#    print(bb)
