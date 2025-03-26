# 实现真正的AI问答 --- by：天青色等烟雨_1ijunha0
from openai import OpenAI
import tkinter as tk
from tkinter import ttk, scrolledtext
import re
import threading


class DeepShitChatAIApp:
    def __init__(self, root):
        self.answer_area = None
        self.root = root
        self.animation_id = None
        self.dot_count = None
        self.loop_count = None
        root.title("DeepShit-你的智障AI <Copyright©2025 by 天青色等烟雨_1ijunha0>")
        root.geometry("600x600")

        # 增加API客户端初始化
        self.client = OpenAI(
            api_key="sk-mzsxdllbdabrmybzgmlermighzrhbvqzqevxsfttcvsxepnt",
            base_url="https://api.siliconflow.cn/v1"
        )
        self.messages = [
            {"role": "system", "content": "你是一个AI助手"},
            {"role": "user", "content": "你好"}
        ]
        self.is_streaming = False   # 添加is_streaming状态标志防止重复请求

        # 配置网格布局权重
        root.rowconfigure(0, weight=1)  # 输入框区域
        root.rowconfigure(1, weight=0)  # 按钮区域
        root.rowconfigure(2, weight=4)  # 回答区域
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
            font=("幼圆", 12),
            # font=("华文行楷", 12),
            # font=("华文隶书", 12),
            padx=10,
            pady=10,
            undo=True,
            foreground="#999"  # 提示语初始灰色文字
        )
        self.text_input.pack(expand=True, fill="both")
        self.text_input.insert("1.0", "给DeepShit这个智障AI发送消息")  # 插入提示语
        self.text_input.tag_configure("placeholder", foreground="#999")

        # 绑定事件
        self.text_input.bind("<FocusIn>", self.clear_placeholder)
        self.text_input.bind("<FocusOut>", self.check_placeholder)
        self.text_input.bind("<Key>", self.on_key_press)

        # 搜索按钮
        self.btn_frame = ttk.Frame(root)
        self.btn_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        self.search_btn = ttk.Button(
            self.btn_frame,
            text="发送",
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

    def clear_placeholder(self, event):
        """清除提示文字"""
        current_text = self.text_input.get("1.0", "end-1c")
        if current_text == "给DeepShit这个智障AI发送消息":
            self.text_input.delete("1.0", "end")
            self.text_input.config(foreground="#000")  # 恢复黑色文字

    def check_placeholder(self, event):
        """检查是否需要恢复提示文字"""
        current_text = self.text_input.get("1.0", "end-1c").strip()
        if not current_text:
            self.text_input.delete("1.0", "end")
            self.text_input.insert("1.0", "给DeepShit这个智障AI发送消息")
            self.text_input.config(foreground="#999")

    def on_key_press(self, event):
        """实时监测键盘输入"""
        current_text = self.text_input.get("1.0", "end-1c")
        if current_text == "给DeepShit这个智障AI发送消息":
            self.text_input.delete("1.0", "end")
            self.text_input.config(foreground="#000")

    def on_window_resize(self, event):
        # 动态调整输入框高度
        total_weight = 1 + 0 + 4  # 总权重
        new_height = max(2, int(self.root.winfo_height() * 1 / total_weight / 20))
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

        if self.is_streaming:
            return

        # 获取问题并清空输入框
        question = self.text_input.get("1.0", tk.END).strip()
        if not question or question == "给DeepShit这个智障AI发送消息":
            return
        self.text_input.delete("1.0", tk.END)
        self.add_message("user", question)

        # 创建独立线程处理请求
        threading.Thread(target=self.stream_response).start()

    def is_valid_input(self, text):
        """输入验证逻辑"""
        # 排除提示文字本身
        if text == "给DeepShit这个智障AI发送消息":
            return False
        # 正则表达式验证
        pattern = r'[^\s\W]'
        return re.match(pattern, text) is not None

    def stream_response(self):
        self.is_streaming = True
        self.search_btn.config(state=tk.DISABLED)

        try:
            full_response = ""
            reasoning_content = ""

            # 发送流式请求
            response = self.client.chat.completions.create(
                model="Pro/deepseek-ai/DeepSeek-R1",
                messages=self.messages,
                stream=True,
                temperature=0.7,
                top_p=0.95,
                frequency_penalty=0.5
            )

            # 处理流式响应
            for chunk in response:
                if not chunk.choices:
                    continue

                # 处理推理内容
                if chunk.choices[0].delta.reasoning_content:
                    reasoning = chunk.choices[0].delta.reasoning_content.replace('\n\n', '\n')
                    reasoning_content += reasoning
                    self.update_answer_box(f"推理：{reasoning}\n", "reasoning")

                # 处理回答内容
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content.replace('\n\n', '\n')
                    full_response += content
                    self.update_answer_box(content, "answer")

            # 保存完整响应
            self.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            self.update_answer_box(f"\n错误：{str(e)}\n", "error")

        finally:
            self.is_streaming = False
            self.search_btn.config(state=tk.NORMAL)

    def update_answer_box(self, content, msg_type):
        def _update():
            self.answer_area.config(state=tk.NORMAL)

            # 根据消息类型添加前缀
            if msg_type == "reasoning" and not self.answer_area.search("推理：", "end-1c", backwards=True):
                self.answer_area.insert(tk.END, "推理：", "reasoning_tag")

            elif msg_type == "answer" and not self.answer_area.search("回答：", "end-1c", backwards=True):
                self.answer_area.insert(tk.END, "\n回答：", "answer_tag")

            # 插入内容
            self.answer_area.insert(tk.END, content)
            self.answer_area.see(tk.END)
            self.answer_area.config(state=tk.DISABLED)

        # 通过主线程更新UI
        self.root.after(0, _update)

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
