# by：天青色等烟雨_1ijunha0
import tkinter as tk
from tkinter import ttk, scrolledtext
import re


class DeepShitChatAIApp:
    def __init__(self, root):
        self.root = root
        self.animation_id = None
        self.dot_count = None
        self.loop_count = None
        root.title("DeepShit-你的智障AI")
        root.geometry("600x600")

        # 配置网格布局权重
        root.rowconfigure(0, weight=1)  # 输入框区域
        root.rowconfigure(1, weight=0)  # 按钮区域
        root.rowconfigure(2, weight=2)  # 回答区域
        root.columnconfigure(0, weight=1)

        # 配置主题和样式
        self.style = ttk.Style()
        self.style.theme_use('clam')  # 使用支持颜色定制的主题

        # 输入框区域（带滚动条）
        self.input_frame = ttk.Frame(root)
        self.input_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

        self.text_input = scrolledtext.ScrolledText(
            self.input_frame,
            wrap=tk.WORD,
            # font=("Times New Roman", 12),
            font=("幼圆", 12),
            # font=("华文行楷", 12),
            # font=("华文隶书", 12),
            padx=10,
            pady=10,
            undo=True,
            foreground="#999"  # 提示语初始灰色文字
        )
        self.text_input.pack(expand=True, fill="both")
        self.showing_placeholder = True
        self.set_placeholder("给DeepShit这个智障AI发送消息")

        # 绑定事件
        self.text_input.bind("<FocusIn>", self.on_focus_in)
        self.text_input.bind("<FocusOut>", self.on_focus_out)
        self.text_input.bind("<<Modified>>", self.on_text_modified)
        self.text_input.bind("<Key>", self.on_key_press)

        # 搜索按钮
        self.btn_frame = ttk.Frame(root)
        self.btn_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        self.search_btn = ttk.Button(
            self.btn_frame,
            text="搜索",
            command=self.on_search,
            style="Primary.TButton"
        )
        self.search_btn.pack(pady=5)

        # 自定义按钮样式
        self.style.configure('Primary.TButton',
                             background='#7FFFD4',  # 按钮主背景颜色-蓝色
                             foreground='black',  # 文字颜色
                             bordercolor='#5F9EA0',  # 边框颜色
                             lightcolor='#7FFFD4',  # 正常状态颜色-亮色
                             darkcolor='#1976D2',  # 按下状态颜色-暗色
                             font=('幼圆', 12, 'bold'),
                             padding=10,
                             relief='raised')

        # 回答区域（居中显示）
        self.answer_frame = ttk.Frame(root)
        self.answer_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

        # 使用Canvas实现完美居中
        self.answer_canvas = tk.Canvas(self.answer_frame, highlightthickness=0)
        self.answer_canvas.pack(fill="both", expand=True)

        # 创建居中文本容器
        self.text_container = self.answer_canvas.create_text(
            300, 150,  # 初始位置
            width=550,
            text="",
            # font=("微软雅黑", 14),
            # font=("Times New Roman", 14),
            font=("幼圆", 14),
            # font=("华文行楷", 14),
            # font=("华文隶书", 14),
            anchor="center",  # 居中锚点
            justify="center"  # 居中对齐
        )

        # 动画相关变量
        self.animation_id = None
        self.dot_count = 0
        self.loop_count = 0

        # 绑定窗口大小变化事件
        self.root.bind("<Configure>", self.on_window_resize)

    def set_placeholder(self, text):
        """设置提示文字（新增光标定位）"""
        self.text_input.delete("1.0", "end")
        self.text_input.insert("1.0", text)
        self.text_input.config(foreground="#999")
        self.text_input.mark_set("insert", "1.0")  # 强制光标到开头
        self.text_input.edit_modified(False)
        self.showing_placeholder = True

    def on_focus_in(self, event):
        """获得焦点时的处理（优化光标行为）"""
        if self.showing_placeholder:
            # 保持提示文字但移动光标到开头
            self.text_input.mark_set("insert", "1.0")
            # 绑定按键事件立即清除提示
            self.text_input.bind("<KeyPress>", self.on_first_key_press, add="+")

    def on_first_key_press(self, event):
        """首次按键处理"""
        if self.showing_placeholder:
            self.text_input.delete("1.0", "end")
            self.text_input.config(foreground="#000")
            self.showing_placeholder = False
        # 解绑临时事件
        self.text_input.unbind("<KeyPress>")

    def on_focus_out(self, event):
        """失去焦点时的处理（优化空内容检测）"""
        current_text = self.text_input.get("1.0", "end-1c").strip()
        if not current_text:
            self.set_placeholder("给DeepShit这个智障AI发送消息")

    def on_text_modified(self, event):
        """文本修改事件处理（增强空内容检测）"""
        if self.text_input.edit_modified():
            current_text = self.text_input.get("1.0", "end-1c").strip()
            if not current_text and not self.text_input.focus_get():
                self.set_placeholder("给DeepShit这个智障AI发送消息")
            self.text_input.edit_modified(False)

    def on_key_press(self, event):
        """处理删除键的特殊情况"""
        if event.keysym == "BackSpace" or event.keysym == "Delete":
            current_text = self.text_input.get("1.0", "end-1c").strip()
            if not current_text:
                self.set_placeholder("给DeepShit这个智障AI发送消息")

    def on_window_resize(self, event):
        # 动态调整输入框高度
        new_height = max(4, int(self.root.winfo_height() / 3 / 20))
        self.text_input.config(height=new_height)
        # 更新居中文本位置
        self.update_text_position()

    def update_text_position(self):
        # 获取Canvas当前尺寸
        canvas_width = self.answer_canvas.winfo_width()
        canvas_height = self.answer_canvas.winfo_height()

        # 更新文本位置到Canvas中心
        self.answer_canvas.coords(
            self.text_container,
            canvas_width / 2,
            canvas_height / 2
        )

    def on_search(self):
        # 清空上次的回答
        self.answer_canvas.itemconfig(self.text_container, text="")

        # 取消正在进行的动画
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None

        # 获取并验证输入
        input_text = self.text_input.get("1.0", "end-1c").strip()
        if not self.is_valid_input(input_text):
            return

        # 启动加载动画
        self.dot_count = 0
        self.loop_count = 0
        self.start_loading_animation()

    def is_valid_input(self, text):
        """输入验证逻辑"""
        """输入验证逻辑（增强空内容检测）"""
        if self.showing_placeholder or text == "":
            return False
        # 正则表达式验证
        pattern = r'[^\s\W]'
        return re.match(pattern, text) is not None

    def start_loading_animation(self):
        """加载动画逻辑"""
        if self.dot_count <= 5:
            dots = "." * self.dot_count
            self.answer_canvas.itemconfig(
                self.text_container,
                text=f"加载中{dots}"
            )
            self.dot_count += 1
        else:
            self.dot_count = 0
            self.loop_count += 1
            if self.loop_count >= 3:
                self.answer_canvas.itemconfig(
                    self.text_container,
                    text="""服务器繁忙，请重试！
(☉д⊙)
(๑・̀ㅂ・́)و✧
(¬‿¬)"""
                )
                return

        self.animation_id = self.root.after(250, self.start_loading_animation)


if __name__ == "__main__":
    root = tk.Tk()
    app = DeepShitChatAIApp(root)
    root.mainloop()
