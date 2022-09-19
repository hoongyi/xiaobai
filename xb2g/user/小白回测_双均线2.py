#双均线策略
#买信号B
B=CROSS(MA(C,5),MA(C,20))

#卖信号S
S=CROSS(MA(C,20),MA(C,5))
