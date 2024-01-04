# 打包命令：pyinstaller -F -w --hidden-import=mmcv._ext timestamp_conversion.py
import tkinter as tk
from datetime import datetime
import time
import math, pyperclip, os


class DateTimeConverterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Kirin-时间戳工具")

        # Left Frame
        self.left_frame = tk.Frame(self.master)
        self.left_frame.grid(row=0, column=0, padx=20, pady=20)
        self.clock_canvas = tk.Canvas(self.left_frame, width=300, height=300)
        self.clock_canvas.grid(row=0, column=0, columnspan=2)

        # Current DateTime Label and Copy Button
        self.current_datetime_label = tk.Label(self.left_frame, text="时间:")
        self.current_datetime_label.grid(row=1, column=0, sticky="e", padx=10)
        self.copy_datetime_button = tk.Button(self.left_frame, text="复制", command=self.copy_current_datetime)
        self.copy_datetime_button.grid(row=1, column=1, sticky="w", pady=5)

        # Current Timestamp Label and Copy Button
        self.current_timestamp_label = tk.Label(self.left_frame, text="时间戳:")
        self.current_timestamp_label.grid(row=2, column=0, sticky="e", padx=10)
        self.copy_timestamp_button = tk.Button(self.left_frame, text="复制", command=self.copy_current_timestamp)
        self.copy_timestamp_button.grid(row=2, column=1, sticky="w", pady=5)

        # Right Frame
        self.right_frame = tk.Frame(self.master)
        self.right_frame.grid(row=0, column=2, padx=20, pady=20)

        self.right_label1 = tk.Label(self.right_frame, text="请输入时间戳")
        self.right_label1.grid(row=1, column=0, padx=10)

        self.timestamp_entry = tk.Entry(self.right_frame)
        self.timestamp_entry.grid(row=1, column=1, padx=10)

        self.convert_button = tk.Button(self.right_frame, text="转为时间", command=self.convert_to_datetime)
        self.convert_button.grid(row=1, column=2, padx=10)

        self.right_label2 = tk.Label(self.right_frame, text="转换结果")
        self.right_label2.grid(row=2, column=0, padx=10)

        self.result_label = tk.Label(self.right_frame, text="1970-01-01 00:00:00")
        self.result_label.grid(row=2, column=1, padx=10)

        self.copy_result_button = tk.Button(self.right_frame, text="复制结果", command=self.copy_result_datetime)
        self.copy_result_button.grid(row=2, column=2, padx=10)

        tk.Label(self.right_frame, text="").grid(row=3)
        tk.Label(self.right_frame, text="").grid(row=4)

        self.right_label3 = tk.Label(self.right_frame, text="请输入日期时间")
        self.right_label3.grid(row=5, column=0, padx=10)

        self.datetime_entry = tk.Entry(self.right_frame)
        self.datetime_entry.grid(row=5, column=1, padx=10)

        self.convert_button2 = tk.Button(self.right_frame, text="转为时间戳", command=self.convert_to_timestamp)
        self.convert_button2.grid(row=5, column=2, padx=10)

        self.right_label4 = tk.Label(self.right_frame, text="转换结果")
        self.right_label4.grid(row=6, column=0, padx=10)

        self.result_label2 = tk.Label(self.right_frame, text="0000000000", anchor="w")
        self.result_label2.grid(row=6, column=1, padx=10)

        self.copy_result_button2 = tk.Button(self.right_frame, text="复制结果", command=self.copy_result_timestamp)
        self.copy_result_button2.grid(row=6, column=2, padx=10)

        # Start updating the clock
        self.update_clock()

        # Start updating current time and timestamp
        self.update_current_datetime_and_timestamp()

    def update_current_datetime_and_timestamp(self):
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        current_timestamp = self.datetime_to_timestamp(datetime.now())
        self.current_datetime_label.config(text=f"时间: {current_datetime}")
        self.current_timestamp_label.config(text=f"时间戳: {current_timestamp}")

        # Schedule the update after 1000 milliseconds (1 second)
        self.master.after(1000, self.update_current_datetime_and_timestamp)

    def update_clock(self):
        # Clear the canvas
        self.clock_canvas.delete("all")

        # Get the current time
        current_time = datetime.now()
        hours = current_time.hour
        minutes = current_time.minute
        seconds = current_time.second

        # Draw clock face
        self.clock_canvas.create_oval(50, 50, 250, 250, fill="#C7DFEE")

        # Draw hour hand
        hour_angle = math.radians((hours % 12) * 30 - 90)
        hour_length = 50
        hour_x = 150 + hour_length * math.cos(hour_angle)
        hour_y = 150 + hour_length * math.sin(hour_angle)
        self.clock_canvas.create_line(150, 150, hour_x, hour_y, width=4, fill="blue")

        # Draw minute hand
        minute_angle = math.radians(minutes * 6 - 90)
        minute_length = 80
        minute_x = 150 + minute_length * math.cos(minute_angle)
        minute_y = 150 + minute_length * math.sin(minute_angle)
        self.clock_canvas.create_line(150, 150, minute_x, minute_y, width=3, fill="green")

        # Draw second hand
        second_angle = math.radians(seconds * 6 - 90)
        second_length = 100
        second_x = 150 + second_length * math.cos(second_angle)
        second_y = 150 + second_length * math.sin(second_angle)
        self.clock_canvas.create_line(150, 150, second_x, second_y, width=2, fill="red")

        # Draw clock numbers
        for i in range(12):
            angle = math.radians(i * 30 - 60)
            num_x = 150 + 90 * math.cos(angle)
            num_y = 150 + 90 * math.sin(angle)
            self.clock_canvas.create_text(num_x, num_y, text=str(i + 1), font=("Helvetica", 12, "bold"))

        # Schedule the update after 1000 milliseconds (1 second)
        self.master.after(1000, self.update_clock)

    def convert_to_datetime(self):
        input_str = self.timestamp_entry.get()
        try:
            timestamp = float(input_str)
            result = self.timestamp_to_datetime(timestamp)
            self.result_label.config(text=result)
        except ValueError:
            self.result_label.config(text="输入的格式错误")

    def convert_to_timestamp(self):
        input_str = self.datetime_entry.get()
        try:
            datetime_obj = datetime.strptime(input_str, '%Y-%m-%d %H:%M:%S')
            result = self.datetime_to_timestamp(datetime_obj)
            self.result_label2.config(text=result)
        except ValueError:
            self.result_label2.config(text="输入的格式错误")

    def datetime_to_timestamp(self, dt):
        dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        dt_t = time.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        timestamp = time.mktime(dt_t)
        # timestamp = (dt - datetime(1970, 1, 1)).total_seconds()
        return int(timestamp)

    def timestamp_to_datetime(self, timestamp):
        # dt = datetime.utcfromtimestamp(timestamp)
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    def copy_result_datetime(self):
        result_datetime = self.result_label.cget("text")
        pyperclip.copy(result_datetime)

    def copy_result_timestamp(self):
        result_timestamp = self.result_label2.cget("text")
        pyperclip.copy(result_timestamp)

    def copy_current_datetime(self):
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        pyperclip.copy(current_datetime)

    def copy_current_timestamp(self):
        current_timestamp = self.datetime_to_timestamp(datetime.now())
        pyperclip.copy(str(current_timestamp))


if __name__ == "__main__":
    root = tk.Tk()
    app = DateTimeConverterApp(root)
    root.mainloop()

