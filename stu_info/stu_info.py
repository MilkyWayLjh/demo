import tkinter as tk
from tkinter import messagebox

class StudentManagementSystem:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("班级学生信息管理系统")

        self.label_name = tk.Label(self.window, text="姓名:")
        self.label_name.pack()
        self.entry_name = tk.Entry(self.window)
        self.entry_name.pack()

        self.label_age = tk.Label(self.window, text="年龄:")
        self.label_age.pack()
        self.entry_age = tk.Entry(self.window)
        self.entry_age.pack()

        self.button_add = tk.Button(self.window, text="添加学生", command=self.add_student)
        self.button_add.pack()

        self.student_listbox = tk.Listbox(self.window)
        self.student_listbox.pack()

        self.button_edit = tk.Button(self.window, text="修改选中学生", command=self.edit_student)
        self.button_edit.pack()

        self.button_delete = tk.Button(self.window, text="删除选中学生", command=self.delete_student)
        self.button_delete.pack()

        self.load_students()

        self.window.mainloop()

    def load_students(self):
        # 在这里从数据库或文件中加载学生信息，并将其添加到Listbox中
        # 这里只是一个示例，使用了固定的学生信息
        students = [("张三", 18), ("李四", 19), ("王五", 20)]
        for student in students:
            self.student_listbox.insert(tk.END, f"姓名: {student[0]}  年龄: {student[1]}")

    def add_student(self):
        name = self.entry_name.get()
        age = self.entry_age.get()
        if name and age:
            self.student_listbox.insert(tk.END, f"姓名: {name}  年龄: {age}")
            self.entry_name.delete(0, tk.END)
            self.entry_age.delete(0, tk.END)
        else:
            messagebox.showerror("错误", "姓名和年龄不能为空")

    def edit_student(self):
        selected_index = self.student_listbox.curselection()
        if selected_index:
            selected_student = self.student_listbox.get(selected_index)
            name = self.entry_name.get()
            age = self.entry_age.get()
            if name and age:
                self.student_listbox.delete(selected_index)
                self.student_listbox.insert(selected_index, f"姓名: {name}  年龄: {age}")
                self.entry_name.delete(0, tk.END)
                self.entry_age.delete(0, tk.END)
            else:
                messagebox.showerror("错误", "姓名和年龄不能为空")
        else:
            messagebox.showerror("错误", "请先选择要修改的学生")

    def delete_student(self):
        selected_index = self.student_listbox.curselection()
        if selected_index:
            self.student_listbox.delete(selected_index)
        else:
            messagebox.showerror("错误", "请先选择要删除的学生")

if __name__ == "__main__":
    StudentManagementSystem()
