#增强通达信公式演示
'''
这个要完全依赖通达信行情,获取股票行情和财务基本数据.
用get_security_bars(nCategory=4,nMarket =-1,code='000776',\
                    nStart=0, nCount=240)
在读取股票行情时,顺便获取股票的基本数据.
下面一是一个演示.
'''

import HP_tdx as htdx
from HP_formula import *
import HP_tdxgs as hgs


def FINANCE(x):
    return hgs.FINANCE(x)

tdxapi=htdx.TdxInit(ip='180.153.18.171')
df=hgs.get_security_bars()
print(FINANCE(30))