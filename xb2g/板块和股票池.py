#小白量化:板块与自选股 股票池

#购买<零基础搭建量化投资系统>正版书,送小白量化软件源代码。
# https://item.jd.com/61567375505.html
#独狼荷蒲qq:2775205
#通通python量化群:524949939
#电话微信:18578755056
#微信公众号：独狼股票分析
#日期:2021-01-09
import HP_tdx as htdx   #小白量化通达信行情模块

#连接通达信行情服务器
hq=htdx.TdxInit(ip='183.57.72.22',port=7709)  ##初始化通达信

#获取股票所属板块
code='000776'
bk=htdx.getblock3(code)
print(code,' 所属板块 :',bk)

code='600655'
bk=htdx.getblock3(code)
print(code,' 所属板块 :',bk)

#获取板块的所有股票代码
bkn='特斯拉'
codes=htdx.getblock2(bkn) #返回板块中的股票
print(bkn,' 板块的所有股票 :',codes)

#板块股票代码合并
codes1=htdx.getblock2('近期强势') #返回板块中的股票
codes2=htdx.getblock2('深证300') #返回板块中的股票
codes3=htdx.getblock2('深证成指') #返回板块中的股票
codes4=htdx.getblock2('上证380') #返回板块中的股票
codes=codes1+codes2+codes3+codes4
print(len(codes),codes)

#股票代码去重
codes=list(set(codes))  #利用集合去掉重复代码
print(len(codes),codes)

#保存为通达信自选股，需要重新启动通达信软件，才能看到
#通达信软件的自选股文件的目录为：C:\tdx目录\T0002\blocknew
path='C:\\zd_gfzq\\T0002\\blocknew\\'  #通道信软件自选股路径

#转化为通达信板块数据格式
bk2=htdx.tdxcodes(codes)
print(bk2)

#保存到通达信自选股2板块文件中
htdx.putzxgfile(bk2,path+'ZXG2.blk')

#断开连接行情服务器
htdx.disconnect()