from tkinter import *
from tkinter import filedialog
root=Tk("Text Editor")
text=Text(root)
text.grid()
def saveas():
    global text
    t = text.get("1.0","end-1c") #限定范围
    saveloacation = filedialog.askopenfilename()
    file1 = open(saveloacation, "w+")
    file1.write(t) #保存
    file1.close()
def FontHelvetica():
    global text
    text.config(font="Helvetica")
def FontCourier():
    global text
    text.config(font="Courier")
button = Button(root, text="Save",command=saveas) # GUI界面上指定按钮对应的函数
button.grid()
font = Menubutton(root, text="Font") #调用方式还是很好懂的，设置一个menubutton
font.grid()
font.menu = Menu(font, tearoff=0)
font["menu"] = font.menu
helvetica = IntVar() # 用于了解用户点击了哪个选择框，从而根据command选择回调函数
courier = IntVar()
font.menu.add_checkbutton(label="Courier", variable=courier, command=FontCourier)
font.menu.add_checkbutton(label="Helvetica", variable=helvetica, command=FontHelvetica)
root.mainloop() #这句话启动GUI界面的时间循环，所以要放在最后
