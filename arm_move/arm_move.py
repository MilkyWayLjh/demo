import tkinter as tk
import threading
import requests

class ArmControlGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("机械臂控制程序By_MilkyWay")
        self.geometry("400x200")

        # 创建一个Frame来容纳Radiobuttons
        radio_frame = tk.Frame(self)
        radio_frame.pack()

        # 耗材选择 Radiobuttons 横向排列
        tk.Label(radio_frame, text="堆站耗材选择：").pack(side=tk.LEFT)
        self.consumable_var = tk.StringVar(value="all")
        tk.Radiobutton(radio_frame, text="全部(80)", variable=self.consumable_var, value="all").pack(side=tk.LEFT)
        tk.Radiobutton(radio_frame, text="反应板(前40)", variable=self.consumable_var, value="reaction_plate").pack(side=tk.LEFT)
        tk.Radiobutton(radio_frame, text="样本板(后40)", variable=self.consumable_var, value="sample_plate").pack(side=tk.LEFT)

        # 创建标签和输入框
        tk.Label(self, text="起始位置编号:").pack()
        self.pos_number_entry = tk.Entry(self)
        self.pos_number_entry.pack()

        tk.Label(self, text="装载卸载次数:").pack()
        self.iterations_entry = tk.Entry(self)
        self.iterations_entry.pack()

        # 创建已完成次数的标签
        # 添加已完成次数的计数器
        self.completed_count = 0
        self.completed_label = tk.Label(self, text=f"已完成次数：{self.completed_count}")
        self.completed_label.pack()

        # 创建开始和停止按钮
        self.start_button = tk.Button(self, text="开始", command=self.start_thread)
        self.start_button.pack()

        self.stop_button = tk.Button(self, text="停止", state=tk.DISABLED, command=self.stop_thread)
        self.stop_button.pack()

        # 设置线程停止标志
        self.running = False

    def start_thread(self):
        # 重置已完成次数的计数器
        self.completed_count = 0
        self.update_completed_count(self.completed_count)

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

    def update_completed_count(self, count):
        # 在主线程中安全更新已完成次数的标签
        self.completed_count = count
        self.completed_label.config(text=f"已完成次数：{self.completed_count}")

    def run_arm_control(self):
        pos_number = int(self.pos_number_entry.get())
        iterations = int(self.iterations_entry.get())
        consumable_type = self.consumable_var.get()

        am = DebugArmMove()
        if consumable_type == "all":
            # 执行所有类型的循环
            for i in range(iterations):
                if not self.running:
                    break
                if pos_number >= 81:
                    pos_number = 1
                if pos_number <= 40:
                    am.arm_grab(pos_number, 2)
                    am.arm_put(85, 2)
                    am.arm_grab(85, 2)
                    am.arm_put(pos_number, 2)
                else:
                    am.arm_grab(pos_number, 1)
                    am.arm_put(81, 1)
                    am.arm_grab(81, 1)
                    am.arm_put(pos_number, 1)
                pos_number += 1
                self.update_completed_count(i+1)  # 更新已完成次数
                self.update()  # 强制刷新GUI
                self.after(100)  # 暂停100毫秒，让GUI有时间更新
        elif consumable_type == "reaction_plate":
            # 执行反应板的循环
            for i in range(iterations):
                if not self.running:
                    break
                if pos_number >= 41:
                    pos_number = 1
                am.arm_grab(pos_number, 2)
                am.arm_put(85, 2)
                am.arm_grab(85, 2)
                am.arm_put(pos_number, 2)
                pos_number += 1
                self.update_completed_count(i+1)  # 更新已完成次数
                self.update()  # 强制刷新GUI
                self.after(100)  # 暂停100毫秒，让GUI有时间更新
        elif consumable_type == "sample_plate":
            # 执行样本板的循环
            for i in range(iterations):
                if not self.running:
                    break
                # 循环执行样本板抓放动作(堆栈后40位)
                if pos_number >= 81:
                    pos_number = 41
                am.arm_grab(pos_number, 1)
                am.arm_put(81, 1)
                am.arm_grab(81, 1)
                am.arm_put(pos_number, 1)
                pos_number += 1
                self.update_completed_count(i+1)  # 更新已完成次数
                self.update()  # 强制刷新GUI
                self.after(100)  # 暂停100毫秒，让GUI有时间更新

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

