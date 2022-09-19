#通达信行情学习
import HP_global as g   #建立全局数据域g
import HP_tdx as htdx   #导入小白通达信模块


#获取板块中包含的股票
df=htdx.getblock2('沪深300')
print(df)

#获取股票所属板块
df=htdx.getblock3('000001')
print(df)
