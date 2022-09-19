#小白回测买点信号B,卖点信号S

##KDJ交易策略 
def KDJ(N=9, M1=3, M2=3):
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = SMA(RSV,M1,1)
    D = SMA(K,M2,1)
    J = 3*K-2*D
    return K, D, J

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



