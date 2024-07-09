import tkinter as tk
import threading
import requests

class ArmControlGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("机械臂控制程序By_MilkyWay_豪呀~")
        self.geometry("400x150")

        # 创建标签和输入框
        tk.Label(self, text="样本板起始位置编号:").pack()
        self.pos_number_entry = tk.Entry(self)
        self.pos_number_entry.pack()

        tk.Label(self, text="样本板装载卸载次数:").pack()
        self.iterations_entry = tk.Entry(self)
        self.iterations_entry.pack()

        # 创建开始和停止按钮
        self.start_button = tk.Button(self, text="开始", command=self.start_thread)
        self.start_button.pack()

        self.stop_button = tk.Button(self, text="停止", state=tk.DISABLED, command=self.stop_thread)
        self.stop_button.pack()

        # 设置线程停止标志
        self.running = False

    def start_thread(self):
        self.running = True
        self.thread = threading.Thread(target=self.run_arm_control)
        self.thread.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_thread(self):
        self.running = False
        self.thread.join()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def run_arm_control(self):
        pos_number = int(self.pos_number_entry.get())
        iterations = int(self.iterations_entry.get())

        am = DebugArmMove()
        for i in range(iterations):
            if not self.running:
                break
            if pos_number == 81:
                pos_number = 41
            am.arm_grab(pos_number, 1)
            am.arm_put(81, 1)
            am.arm_grab(81, 1)
            am.arm_put(pos_number, 1)
            pos_number += 1

class DebugArmMove:
    def __init__(self):
        self.url = 'http://10.3.0.100:8081/api/v1'

    def arm_grab(self, pos_num, consume_type):
        """
        机械臂抓取耗材
        @param pos_num: 抓的位置编号
        @param consume_type: 耗材类型（样本板是1，反应板是2）
        @return:
        """
        url = self.url + '/device/debug/arm/grab'
        payload = {
            'posNum': pos_num,
            'consumeType': consume_type
        }
        return requests.request('post', url, params=payload)

    def arm_put(self, pos_num, consume_type):
        """
        机械臂放置耗材
        @param pos_num: 放的位置编号
        @param consume_type: 耗材类型（样本板是1，反应板是2）
        @return:
        """
        url = self.url + '/device/debug/arm/put'
        payload = {
            'posNum': pos_num,
            'consumeType': consume_type
        }
        return requests.request('post', url, params=payload)

if __name__ == "__main__":
    app = ArmControlGUI()
    app.mainloop()

