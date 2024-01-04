import tkinter as tk
from tkinter import messagebox
import random


def confirm():
    top_name = top_entry.get()
    jug_name = jug_entry.get()
    mid_name = mid_entry.get()
    ad_name = ad_entry.get()
    sup_name = sup_entry.get()

    if not top_name or not jug_name or not mid_name or not ad_name or not sup_name:
        messagebox.showinfo("提示", "请完整输入每个位置的选手ID")
        return

    top_score = random.randint(80, 100)
    jug_score = random.randint(80, 100)
    mid_score = random.randint(80, 100)
    ad_score = random.randint(80, 100)
    sup_score = random.randint(80, 100)

    message = f"Top: {top_name} {top_score}分\nJug: {jug_name} {jug_score}分\nMid: {mid_name} {mid_score}分\n" \
              f"AD: {ad_name} {ad_score}分\nSup: {sup_name} {sup_score}分\n你是一个优秀的电竞经理，你的队伍下赛季一定会夺取冠军！"

    result_label.config(text=message)


root = tk.Tk()
root.title("电竞经理")
root.geometry("400x400")

top_label = tk.Label(root, text="请买入选手\n⬇⬇⬇⬇⬇")
top_label.pack()


top_label = tk.Label(root, text="Top:")
top_label.pack()
top_entry = tk.Entry(root)
top_entry.pack()

jug_label = tk.Label(root, text="Jug:")
jug_label.pack()
jug_entry = tk.Entry(root)
jug_entry.pack()

mid_label = tk.Label(root, text="Mid:")
mid_label.pack()
mid_entry = tk.Entry(root)
mid_entry.pack()

ad_label = tk.Label(root, text="AD:")
ad_label.pack()
ad_entry = tk.Entry(root)
ad_entry.pack()

sup_label = tk.Label(root, text="Sup:")
sup_label.pack()
sup_entry = tk.Entry(root)
sup_entry.pack()

confirm_button = tk.Button(root, text="确认", command=confirm)
confirm_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
