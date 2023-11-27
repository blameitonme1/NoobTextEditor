from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

# 保存文件
def save_as():
    global buffer_start  # 声明为全局变量
    t = text.get("1.0", "end-1c")
    # 弹出文件保存对话框
    save_location = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if save_location:
        with open(save_location, "w+") as file:
            file.write(t)
        # 更新缓冲区的起始位置，因为刚刚save过了
        buffer_start = text.index("end-1c")

# 设置字体为Helvetica
def font_helvetica():
    text.config(font="Helvetica")

# 设置字体为Courier
def font_courier():
    text.config(font="Courier")

# 撤销操作
def undo(event=None):
    text.edit_undo()

def show_help():
    help_text = (
        "保存: 保存当前文本内容\n"
        "字体 -> Courier: 设置文本框字体为Courier\n"
        "字体 -> Helvetica: 设置文本框字体为Helvetica\n"
        "撤销: 撤销上一步操作\n"
        "查找: 在文本中查找指定字符串\n"
        "查看缓冲区: 查看当前保存位置后的文本内容\n"
        "退出: 关闭文本编辑器"
    )
    messagebox.showinfo("帮助", help_text)

# 查找文本
def find_text():
    target = entry.get()
    if target:
        start_index = text.index(INSERT)
        # 在文本中查找目标字符串，从当前位置开始，不区分大小写
        found_index = text.search(target, start_index, stopindex="end", nocase=True, count=END)
        if found_index:
            text.tag_remove("found", "1.0", "end")
            text.tag_add("found", found_index, f"{found_index.split('.')[0]}.end")
            text.mark_set(INSERT, found_index)
        else:
            messagebox.showinfo("查找", f"未找到包含 '{target}' 的文本。")

# 关闭窗口时的处理
def on_closing():
    if messagebox.askyesno("退出", "是否保存并退出？"):
        save_as()
        root.destroy()
    else:
        # 记得还是要退出
        root.destroy()

def view_buffer():
    # 获取当前保存位置后的文本内容，读取缓冲区的内容，使用gui上的按钮实现功能
    global buffer_start  # 声明为全局变量
    buffer_text = text.get(buffer_start, "end-1c")
    buffer_window = Toplevel(root)
    buffer_window.title("缓冲区内容")
    buffer_textbox = Text(buffer_window, wrap="none")
    buffer_textbox.insert("1.0", buffer_text)
    buffer_textbox.pack()

# 绑定快捷键ctrl 加 ? 访问帮助界面
def show_help_with_ctrl_question(event=None):
    show_help()

# 创建主窗口
root = Tk()
root.title("简单的文本编辑器")

# 创建文本框，启用撤销功能
text = Text(root, undo=True)
text.grid()

# 保存按钮
button_save = Button(root, text="保存", command=save_as)
button_save.grid()

# 字体菜单
button_font = Menubutton(root, text="字体")
button_font.grid()
button_font.menu = Menu(button_font, tearoff=0)
button_font["menu"] = button_font.menu
button_font.menu.add_command(label="Courier", command=font_courier)
button_font.menu.add_command(label="Helvetica", command=font_helvetica)

# 查找按钮
button_find = Button(root, text="查找", command=find_text)
button_find.grid()

# 查找目标输入框
entry = Entry(root, width=20)
entry.grid()

# 设置查找到的文本的背景色
text.tag_configure("found", background="yellow")

# 初始缓冲区起始位置为文本末尾
buffer_start = "1.0"
# 设置相关按钮
button_view_buffer = Button(root, text="查看缓冲区", command=view_buffer)
button_view_buffer.grid()
# 根据操作系统设置撤销的快捷键
if root.tk.call('tk', 'windowingsystem') == 'win32':
    root.bind("<Control-z>", undo)
else:
    root.bind("<Command-z>", undo)
# 设置帮助按钮，可以转到一个帮助界面
button_help = Button(root, text="帮助", command=show_help)
button_help.grid()

# 绑定 Ctrl+Shift+? 快捷键事件， 显示帮助界面
root.bind("<Control-Shift-?>", show_help_with_ctrl_question)

# 设置窗口关闭时的处理函数
root.protocol("WM_DELETE_WINDOW", on_closing)

# 进入主循环
root.mainloop()
