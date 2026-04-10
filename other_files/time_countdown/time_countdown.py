import tkinter as tk
from datetime import datetime, timedelta

try:
    # pip install zhdate
    from zhdate import ZhDate
except Exception:  # pragma: no cover
    ZhDate = None


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


def _next_spring_festival_datetime(now: datetime) -> datetime:
    """
    返回“下一次到来的春节(农历正月初一 00:00:00)”对应的公历时间。
    通过 zhdate 在候选年份里取最早且 >= now 的日期。
    """
    if ZhDate is None:
        raise RuntimeError("缺少依赖：请先执行 pip install zhdate")

    candidates: list[datetime] = []
    for lunar_year in range(now.year - 1, now.year + 3):
        dt = ZhDate(lunar_year, 1, 1).to_datetime().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        candidates.append(dt)

    future = [dt for dt in candidates if dt >= now.replace(microsecond=0)]
    if not future:
        # 极端情况下兜底：取最后一个候选的下一年
        lunar_year = now.year + 3
        return ZhDate(lunar_year, 1, 1).to_datetime().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
    return min(future)


def _fmt_date(dt: datetime) -> str:
    return dt.strftime("%Y.%m.%d")


def update_countdown():
    """更新两个倒计时的显示，每秒调用一次"""
    now = datetime.now()

    try:
        target_spring_festival = _next_spring_festival_datetime(now)
    except Exception as e:
        # 依赖缺失或换算失败时，给出明确提示，但不让窗口崩掉
        label_newyears_eve.config(text=str(e))
        label_spring_festival.config(text=str(e))
        root.after(1000, update_countdown)
        return

    target_newyears_eve = target_spring_festival - timedelta(days=1)

    # 动态更新标题（只在需要时刷新文本）
    title_newyears_eve_text = f"距离除夕（公历{_fmt_date(target_newyears_eve)}）还有："
    if title_newyears_eve.cget("text") != title_newyears_eve_text:
        title_newyears_eve.config(text=title_newyears_eve_text)

    title_spring_festival_text = f"距离春节（公历{_fmt_date(target_spring_festival)}）还有："
    if title_spring_festival.cget("text") != title_spring_festival_text:
        title_spring_festival.config(text=title_spring_festival_text)

    # 1) 除夕倒计时
    days1, hours1, minutes1, seconds1 = get_time_difference(target_newyears_eve)
    if days1 == 0 and hours1 == 0 and minutes1 == 0 and seconds1 == 0:
        label_newyears_eve.config(text="除夕已至！🎉 阖家欢乐！")
    else:
        label_newyears_eve.config(
            text=f"{days1:02d} 天 {hours1:02d} 时 {minutes1:02d} 分 {seconds1:02d} 秒"
        )

    # 2) 春节倒计时
    days2, hours2, minutes2, seconds2 = get_time_difference(target_spring_festival)
    if days2 == 0 and hours2 == 0 and minutes2 == 0 and seconds2 == 0:
        label_spring_festival.config(text="春节已到！🎆 新年快乐！")
    else:
        label_spring_festival.config(
            text=f"{days2:02d} 天 {hours2:02d} 时 {minutes2:02d} 分 {seconds2:02d} 秒"
        )

    # 1000毫秒（1秒）后再次调用自身，实现实时更新
    root.after(1000, update_countdown)


# 主窗口设置
root = tk.Tk()
root.title("双节倒计时 - 除夕 & 春节")
root.geometry("720x200")  # 微调窗口尺寸，适配文字
root.resizable(False, False)  # 禁止调整窗口大小
root.configure(bg="#f0f0f0")  # 窗口背景色

# ========== 第一个模块：除夕倒计时 ==========
frame_newyears_eve = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.GROOVE, padx=20, pady=15)
frame_newyears_eve.pack(fill=tk.X, padx=30, pady=20)  # 水平填充，加外间距

# 除夕标题（动态标注公历日期，避免歧义）
title_newyears_eve = tk.Label(
    frame_newyears_eve,
    text="距离除夕（公历----.--.--）还有：",
    font=("微软雅黑", 14, "bold"),
    bg="#ffffff",
    fg="#e74c3c"  # 红色系，贴合除夕氛围
)
title_newyears_eve.pack(side=tk.LEFT)

# 除夕倒计时内容
label_newyears_eve = tk.Label(
    frame_newyears_eve,
    font=("微软雅黑", 14),
    bg="#ffffff",
    fg="#34495e"
)
label_newyears_eve.pack(side=tk.LEFT, padx=10)

# ========== 第二个模块：春节倒计时 ==========
frame_spring_festival = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.GROOVE, padx=20, pady=15)
frame_spring_festival.pack(fill=tk.X, padx=30, pady=0)

# 春节标题（动态标注公历日期，避免歧义）
title_spring_festival = tk.Label(
    frame_spring_festival,
    text="距离春节（公历----.--.--）还有：",
    font=("微软雅黑", 14, "bold"),
    bg="#ffffff",
    fg="#27ae60"  # 绿色系，贴合春节氛围
)
title_spring_festival.pack(side=tk.LEFT)

# 春节倒计时内容
label_spring_festival = tk.Label(
    frame_spring_festival,
    font=("微软雅黑", 14),
    bg="#ffffff",
    fg="#34495e"
)
label_spring_festival.pack(side=tk.LEFT, padx=10)

# 启动倒计时更新
update_countdown()

# 主循环
root.mainloop()
