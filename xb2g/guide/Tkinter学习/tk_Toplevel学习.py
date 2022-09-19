import tkinter as tk   #导入Tkinter
#本软件由Tkinter开发,如果需要获取root的管理权
#需要导入模块HP_global设置别名g  
import HP_global as g  
#此后,可以创建Toplevel窗口
#下面是演示
top=tk.Toplevel(g.root)   #创建Toplevel窗口
top.title(string = 'top子窗口')  #设置窗口标题。
top.geometry('200x100')   #改变窗口大小
top.attributes("-toolwindow", 1)  #参数1，设置工具栏样式窗口。

