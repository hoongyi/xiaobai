import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from HP_formula import *  #小白量化公式函数库

a=np.arange(1,13).reshape(3,4)
df=pd.DataFrame(a,columns=list('abcd'))
df['nn']=OR(IF(df[(df.columns)[-1]]>=8,1,0),IF(df[(df.columns)[-2]]>=8,1,0))*2
print(df)