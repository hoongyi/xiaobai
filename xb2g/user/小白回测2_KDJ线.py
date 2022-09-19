#小白回测买点信号B,卖点信号S
# 最新版支持常用系统指标
# KDJ、TRIX、DMI、CCI、WR、MACD、RSI、
# CR、BOLL、OSC、MOM、DPO、EXPMA、VHF、PUCU、
# ASI、BIAS、WVAD、VR、PVI、NVI、

k,d,j=KDJ(22,11,22)

##下面开始生成KDJ指标买卖点
##买点J上穿数值20
B=CROSS(j,20)

##卖点J下穿80
s1=CROSS(80,j)

#卖点J下穿50
s2=CROSS(50,j)

#合并所有卖点信号相当于公式的OR
S=s1 | s2

g.hctitle='KDJ交易策略'



