def msg():
    import tkinter as tk
    from tkinter import messagebox as msgbox
    import os
    path2='/cp'
    os.chdir(path2)
    import HP_global as g  

    #自动移动窗口到屏幕中央       
    def setCenter(window,w=0,h=0):
        ws = window.winfo_screenwidth()  #获取屏幕宽度（单位：像素）
        hs = window.winfo_screenheight()  #获取屏幕高度（单位：像素） 
        if (w==0  or  h==0):
            w = window.winfo_width()   #获取窗口宽度（单位：像素）
            h = window.winfo_height()  #获取窗口高度（单位：像素）
        x = int( (ws/2) - (w/2) )
        y = int( (hs/2) - (h/2) )
        window.geometry('{}x{}+{}+{}'.format(w, h, x, y))

     
    def btn1_clicked():
                    msgbox.showinfo("Info", "Showinfo test.")
    def btn2_clicked():
                    msgbox.showwarning("Warning", "Showwarning test.")
    def btn3_clicked():
                    msgbox.showerror("Error", "Showerror test.")               
    def btn4_clicked():
                    msgbox.askquestion("Question", "Askquestion test.")
    def btn5_clicked():
                    msgbox.askokcancel("OkCancel", "Askokcancel test.")
    def btn6_clicked():
                    msgbox.askyesno("YesNo", "Askyesno test.")               
    def btn7_clicked():
                    msgbox.askretrycancel("Retry", "Askretrycancel test.")
                   
    top = tk.Toplevel(g.root)   #创建Toplevel窗口
    top.title("MsgBox Test")
     
    btn1 = tk.Button(top, text = "showinfo", command = btn1_clicked)
    btn1.pack(fill = tk.X)
    btn2 = tk.Button(top, text = "showwarning", command = btn2_clicked)
    btn2.pack(fill = tk.X)
    btn3 = tk.Button(top, text = "showerror", command = btn3_clicked)
    btn3.pack(fill = tk.X)
    btn4 = tk.Button(top, text = "askquestion", command = btn4_clicked)
    btn4.pack(fill = tk.X)
    btn5 = tk.Button(top, text = "askokcancel", command = btn5_clicked)
    btn5.pack(fill = tk.X)
    btn6 = tk.Button(top, text = "askyesno", command = btn6_clicked)
    btn6.pack(fill = tk.X)
    btn7 = tk.Button(top, text = "askretrycancel", command = btn7_clicked)
    btn7.pack(fill = tk.X)
    setCenter(top,w=200,h=300)
    top.attributes('-topmost',1)  #参数1，设置顶层窗口，覆盖其它窗口。
msg()


