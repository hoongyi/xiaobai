import tkinter as tk   #导入Tkinter
#本软件由Tkinter开发,如果需要获取root的管理权
# 导入ttk
from tkinter import ttk
#需要导入模块HP_global设置别名g  
import HP_global as g  
#此后,可以创建Toplevel窗口
#下面是演示
top=tk.Toplevel(g.root)   #创建Toplevel窗口
top.geometry('200x100')   #改变窗口大小
top.attributes("-toolwindow", 1)  #参数1，设置工具栏样式窗口。

class App:
    def __init__(self, master):
        self.master = master
        self.initWidgets()
    def initWidgets(self):
        # 创建Style
        style = ttk.Style()
        style.configure("fkit.TPanedwindow",
            background='darkgray', relief=RAISED)
        # 创建Panedwindow组件，通过style属性配置分隔线
        pwindow = ttk.Panedwindow(self.master,
            orient=HORIZONTAL, style="fkit.TPanedwindow")
        pwindow.pack(fill=BOTH, expand=YES)
        left = ttk.Label(pwindow, text="左边标签", background='pink')
        pwindow.add(left)
        # 创建第二个Panedwindow组件，该组件的方向为垂直方向
        rightwindow = PanedWindow(pwindow, orient=VERTICAL)
        pwindow.add(rightwindow)
        top = Label(rightwindow, text="右上标签", background='lightgreen')
        rightwindow.add(top) 
        bottom = Label(rightwindow, text="右下标签", background='lightblue')
        rightwindow.add(bottom) 

top.title("Panedwindow测试")
App(top)
