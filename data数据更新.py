import HP_tdx as htdx
import HP_hz as hz

print("更新小白量化data目录中数据。估计需要几十分钟。")
tdxapi=htdx.TdxInit(ip='40.73.76.10',port=7709)

#更新板块信息
print('开始更新板块信息。')
BLOCK_DEFAULT = "block.dat"
BLOCK_SZ = "block_zs.dat"
BLOCK_FG = "block_fg.dat"
BLOCK_GN = "block_gn.dat"
htdx.get_block(bk=BLOCK_DEFAULT);
htdx.get_block(bk= BLOCK_SZ);
htdx.get_block(bk= BLOCK_FG);
htdx.get_block(bk= BLOCK_GN);
print('板块信息更新完成。')

hz.loadhzk2(file='./data/pinyin.csv')  #加载中文拼音
#'深圳股票代码表'
def szcode():
    #'深圳股票代码'
    sz=htdx.getSZ()
    sz=sz.dropna(axis=0,how='all')
    sz=sz.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    sz['type']=''
    sz['kind']=''
    sz['market']=0
    sz['type2']=10
    sz['py']=''
    for i in range(len(sz)):
        if i==9000 or i==13001:
            continue
        #print(i,sz['code'][i])
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
        elif x>=600000 and x<799999:
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
        #print(sz['name'][i])
        sz.loc[i,'py']=hz.firstpinyin(sz['name'][i])
    sz.to_csv('./data/sz.csv' , encoding= 'gbk')    
    return sz

#上海股票代码表
def shcode():
    #上海股票代码
    sh=htdx.getSH()
    sh=sh.dropna(axis=0,how='all')
    sh=sh.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    sh['type']=''
    sh['kind']=''
    sh['market']=1
    sh['type2']=10
    sh['py']=''
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
        elif x>=600000 and x<688000:
            sh.loc[i,'type']='证券'  
            sh.loc[i,'kind']='A股股票'  
            sh.loc[i,'type2']=1
        elif x>=688000 and x<700000:
            sh.loc[i,'type']='证券'
            sh.loc[i,'kind']='科创板'  
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
        sh.loc[i,'py']=hz.firstpinyin(sh['name'][i])
    sh.to_csv('./data/sh.csv' , encoding= 'gbk')
    return sh


print('开始更新深圳代码表，请等待...')
szcode()
print('深圳代码表更新完成。')

print('开始更新上海代码表，请等待...')
shcode()

print('上海代码表更新完成。')


##获取全部深圳财务数据
#print('开始获取全部深圳财务数据，请等待...')
#htdx.get_szcw()
#print('数据获取完成！')
#
##获取全部上海财务数据
#print('开始获取全部上海财务数据，请等待...')
#htdx.get_shcw()
#print('数据获取完成！')

htdx.disconnect()