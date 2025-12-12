import tkinter as tk
from datetime import datetime


def get_time_difference(target_datetime):
    """计算当前时间与目标时间的时间差，返回天、时、分、秒"""
    current_datetime = datetime.now()
    time_delta = (target_datetime - current_datetime).total_seconds()
    
    if time_delta <= 0:
        return (0, 0, 0, 0)  # 目标时间已过
    
    # 转换为天、时、分、秒
    days = int(time_delta // 86400)  # 一天86400秒
    hours = int((time_delta % 86400) // 3600)
    minutes = int((time_delta % 3600) // 60)
    seconds = int(time_delta % 60)
    return (days, hours, minutes, seconds)

def update_countdown():
    """更新两个倒计时的显示，每秒调用一次"""
    # 1. 农历2025年除夕（公历2026年2月16日 00:00:00）
    target_2025_newyears_eve = datetime(2026, 2, 16, 0, 0, 0)
    days1, hours1, minutes1, seconds1 = get_time_difference(target_2025_newyears_eve)
    # 更新2025除夕的显示
    if days1 == 0 and hours1 == 0 and minutes1 == 0 and seconds1 == 0:
        label_2025.config(text="2025年除夕已至！🎉 阖家欢乐！")
    else:
        text_2025 = f"{days1:02d} 天 {hours1:02d} 时 {minutes1:02d} 分 {seconds1:02d} 秒"
        label_2025.config(text=text_2025)

    # 2. 农历2026年春节（公历2026年2月17日 00:00:00）
    target_2026_spring_festival = datetime(2026, 2, 17, 0, 0, 0)
    days2, hours2, minutes2, seconds2 = get_time_difference(target_2026_spring_festival)
    # 更新2026春节的显示
    if days2 == 0 and hours2 == 0 and minutes2 == 0 and seconds2 == 0:
        label_2026.config(text="2026年春节已到！🎆 新年快乐！")
    else:
        text_2026 = f"{days2:02d} 天 {hours2:02d} 时 {minutes2:02d} 分 {seconds2:02d} 秒"
        label_2026.config(text=text_2026)

    # 1000毫秒（1秒）后再次调用自身，实现实时更新
    root.after(1000, update_countdown)


# 主窗口设置
root = tk.Tk()
root.title("双节倒计时 - 2025年除夕 & 2026年春节")
root.geometry("720x200")  # 微调窗口尺寸，适配文字
root.resizable(False, False)  # 禁止调整窗口大小
root.configure(bg="#f0f0f0")  # 窗口背景色

# ========== 第一个模块：2025年除夕倒计时 ==========
frame_2025 = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.GROOVE, padx=20, pady=15)
frame_2025.pack(fill=tk.X, padx=30, pady=20)  # 水平填充，加外间距

# 2025除夕标题（标注公历日期，避免歧义）
title_2025 = tk.Label(
    frame_2025,
    text="距离2025年除夕（公历2026.02.16）还有：",
    font=("微软雅黑", 14, "bold"),
    bg="#ffffff",
    fg="#e74c3c"  # 红色系，贴合除夕氛围
)
title_2025.pack(side=tk.LEFT)

# 2025除夕倒计时内容
label_2025 = tk.Label(
    frame_2025,
    font=("微软雅黑", 14),
    bg="#ffffff",
    fg="#34495e"
)
label_2025.pack(side=tk.LEFT, padx=10)

# ========== 第二个模块：2026年春节倒计时 ==========
frame_2026 = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.GROOVE, padx=20, pady=15)
frame_2026.pack(fill=tk.X, padx=30, pady=0)

# 2026春节标题（标注公历日期，避免歧义）
title_2026 = tk.Label(
    frame_2026,
    text="距离2026年春节（公历2026.02.17）还有：",
    font=("微软雅黑", 14, "bold"),
    bg="#ffffff",
    fg="#27ae60"  # 绿色系，贴合春节氛围
)
title_2026.pack(side=tk.LEFT)

# 2026春节倒计时内容
label_2026 = tk.Label(
    frame_2026,
    font=("微软雅黑", 14),
    bg="#ffffff",
    fg="#34495e"
)
label_2026.pack(side=tk.LEFT, padx=10)

# 启动倒计时更新
update_countdown()

# 主循环
root.mainloop()
