import tkinter as tk
import random

# 创建一个窗口
root = tk.Tk()
root.title("数字绘制猫")

# 创建一个画布
canvas = tk.Canvas(root, width=200, height=200)
canvas.pack()

# 定义一个数字矩阵来表示猫的图像
cat_image = [
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 1, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0]
]

# 绘制猫的图像
cell_size = 20
for i in range(8):
    for j in range(8):
        if cat_image[i][j] == 1:
            color = 'black'
        else:
            color = 'white'
        canvas.create_rectangle(j*cell_size, i*cell_size, (j+1)*cell_size, (i+1)*cell_size, fill=color)

# 运行程序
root.mainloop()