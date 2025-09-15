import tkinter
from tkinter import messagebox
import webbrowser


class VIPVideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title('VIP Video Tool')
        self.root.geometry('480x240')
        self.root.configure(bg='#F0F8FF')  # 轻蓝色背景
        self.create_widgets()

    def create_widgets(self):
        # 提示标签
        label_movie_link = tkinter.Label(self.root, text='输入视频网址：', bg='#F0F8FF', font=('Microsoft YaHei', 10))
        label_movie_link.place(x=20, y=30, width=100, height=30)

        # 输入框
        self.entry_movie_link = tkinter.Entry(self.root, font=('Microsoft YaHei', 10))
        self.entry_movie_link.place(x=125, y=30, width=260, height=30)

        # 清空按钮
        button_movie_link = tkinter.Button(self.root, text='清空', command=self.empty, bg='#FF6347', fg='white',
                                           font=('Microsoft YaHei', 10), relief='flat')
        button_movie_link.place(x=400, y=30, width=50, height=30)

        # 第一行按钮
        start_x = 50  # 起始位置
        spacing = 70  # 按钮间距

        button_movie1 = tkinter.Button(self.root, text='腾讯视频', command=self.open_tx, bg='#4169E1', fg='white',
                                       font=('Microsoft YaHei', 10, 'bold'), relief='flat')
        button_movie1.place(x=start_x, y=90, width=80, height=40)

        button_movie2 = tkinter.Button(self.root, text='爱奇艺', command=self.open_iqy, bg='#FF6EB4', fg='white',
                                       font=('Microsoft YaHei', 10, 'bold'), relief='flat')
        button_movie2.place(x=start_x + spacing + 80, y=90, width=80, height=40)

        button_movie3 = tkinter.Button(self.root, text='优酷视频', command=self.open_yq, bg='#00BFFF', fg='white',
                                       font=('Microsoft YaHei', 10, 'bold'), relief='flat')
        button_movie3.place(x=start_x + 2*(spacing + 80), y=90, width=80, height=40)

        # 播放视频按钮单独一行并居中显示
        button_movie = tkinter.Button(self.root, text='播放VIP视频', command=self.play_video, bg='#32CD32', fg='white',
                                      font=('Microsoft YaHei', 12, 'bold'), relief='raised', width=15, height=2, activebackground='#228B22')
        # 居中计算: (480 - 200) / 2 = 140, y坐标设为140
        button_movie.place(x=140, y=140, width=200, height=40)

        # 提示标签
        text = '提示：一个小Demo，说不定什么时候就不管用了~'
        lab_remind = tkinter.Label(self.root, text=text, fg='red', font=('Microsoft YaHei', 10, 'italic'), bg='#F0F8FF')
        lab_remind.place(x=40, y=200, width=400, height=30)

        # 添加装饰性分割线
        separator = tkinter.Frame(self.root, height=2, width=440, bg="#D3D3D3")
        separator.place(x=20, y=70)

        # 设置窗口大小
        self.root.resizable(False, False)  # 禁止调整窗口大小

    def open_tx(self):
        webbrowser.open('https://v.qq.com')

    def open_iqy(self):
        webbrowser.open('https://www.iqiyi.com')

    def open_yq(self):
        webbrowser.open('https://www.youku.com/')

    def play_video(self):
        video = self.entry_movie_link.get()
        # 如果输入框为空，显示错误提示
        if not video:
            # tkinter.messagebox.showerror("错误", "请输入视频网址！")
            messagebox.showerror("错误", "请输入视频网址！")
            return
        # webbrowser.open('https://jx.xmflv.cc/?url=' + video)
        webbrowser.open('https://yparse.ik9.cc/index.php?url=' + video)

    def empty(self):
        self.entry_movie_link.delete(0, 'end')


if __name__ == '__main__':
    root = tkinter.Tk()
    app = VIPVideoApp(root)
    root.mainloop()
