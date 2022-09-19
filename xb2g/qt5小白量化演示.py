import sys
import numpy as np
import matplotlib
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
matplotlib.use("Qt5Agg")  # 声明使用QT5
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget
from HP_formula import *
#import tushare as ts
import HP_data  as ts
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

global CLOSE,LOW,HIGH,OPEN,VOL
def KDJ(N=9, M1=3, M2=3):
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = SMA(RSV,M1,1)
    D = SMA(K,M2,1)
    J = 3*K-2*D
    return K, D, J

#首先要对数据预处理
df = ts.get_k_data('600080',ktype='D')
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

k,d,j=KDJ()

mydf = mydf.join(pd.Series( k,name='K'))  
mydf = mydf.join(pd.Series( d,name='D'))  
mydf = mydf.join(pd.Series( j,name='J')) 
mydf['S80']=80  #增加上轨80轨迹线
mydf['X20']=20  #增加下轨20轨迹线

mydf=mydf.tail(100)  #显示最后100条数据线 
 


class QtDraw(QMainWindow):
    flag_btn_start = True
 
    def __init__(self):
        super(QtDraw, self).__init__()
        self.init_ui()
 
    def init_ui(self):
        self.resize(800, 600)
        self.setWindowTitle('PyQt5 小白量化演示')
 
        # TODO:这里是结合的关键
        self.fig = plt.Figure()
        self.canvas = FC(self.fig)
 
        ax = self.fig.add_subplot(111)
        ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
        ax.plot(mydf.date.values,mydf.S80,label='S80', linewidth=1.5)
        ax.plot(mydf.date.values,mydf.X20,label='S80', linewidth=1.5)
        ax.plot(mydf.date.values,mydf.S80,label='S20', linewidth=1.5)
        ax.plot(mydf.date.values,mydf.K,label='K', linewidth=1.5)
        ax.plot(mydf.date.values,mydf.D,label='D', linewidth=1.5)
        ax.plot(mydf.date.values,mydf.J,label='J', linewidth=1.5)
        self.canvas.draw()  # TODO:这里开始绘制

    
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
 

 
 
def ui_main():
    app = QApplication(sys.argv)
    w = QtDraw()
    w.show()
    sys.exit(app.exec_())
 
 
if __name__ == '__main__':
    ui_main()
 