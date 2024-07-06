import tkinter as tk
from tkinter import filedialog
from pathlib import Path


def convert_to_utf8():
    # 获取文件路径
    filepath = file_path.get()
    if not filepath:
        result_label.config(text="请选择一个文件")
        return

    try:
        # 读取文件内容
        with open(filepath, 'rb') as file:
            content = file.read()

        # 尝试将内容解码为utf-8
        text_content = content.decode('utf-8', errors='replace')

        # 再次编码为utf-8
        utf8_content = text_content.encode('utf-8')

        # 创建新文件名
        filename = Path(filepath)
        ext = filename.suffix
        new_filename = f"{filepath}_utf8{ext}"

        # 写入新文件
        with open(new_filename, 'wb') as new_file:
            new_file.write(utf8_content)

        result_label.config(text=f"文件已成功转换并保存为 {new_filename}")

    except Exception as e:
        result_label.config(text=f"发生错误：{str(e)}")


root = tk.Tk()
root.title("文件编码转换器")

# 文件路径输入框
file_path = tk.StringVar()
file_entry = tk.Entry(root, textvariable=file_path, width=50)
file_entry.grid(row=0, column=0, padx=10, pady=10)

# 浏览按钮
browse_button = tk.Button(root, text="浏览", command=lambda: file_path.set(filedialog.askopenfilename()))
browse_button.grid(row=0, column=1, padx=10, pady=10)

# 转换按钮
convert_button = tk.Button(root, text="转换为UTF-8", command=convert_to_utf8)
convert_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# 结果标签
result_label = tk.Label(root, text="", fg="green")
result_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
