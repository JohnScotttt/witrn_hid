# WITRN conversion UI
# Created by JohnScotttt on 2025/8/16, modified on 2025/8/18
# Copyright (c) 2025 JohnScotttt
# Version 1.1

import tkinter as tk
from tkinter import filedialog, messagebox
from witrn_conversion import old_to_new, new_to_old


class FileProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("维简新旧上位机数据转换")
        self.set_window_center(400, 250)
        self.root.resizable(False, False)

        self.input_path = None
        self.output_path = None
        self.mode = "o2n"  # 默认模式

        # 输入文件
        self.input_label = tk.Label(root, text="未选择输入CSV文件")
        self.input_label.pack(pady=5)

        self.input_btn = tk.Button(root, text="选择输入CSV文件", command=self.select_input_file)
        self.input_btn.pack(pady=5)

        # 输出文件
        self.output_label = tk.Label(root, text="未选择保存路径")
        self.output_label.pack(pady=5)

        self.output_btn = tk.Button(root, text="选择输出CSV路径", command=self.select_output_file)
        self.output_btn.pack(pady=5)

        # 模式切换
        self.mode_btn = tk.Button(root, text="当前模式: old to new", command=self.toggle_mode)
        self.mode_btn.pack(pady=10)

        # 执行处理
        self.process_btn = tk.Button(root, text="开始处理", command=self.process_file)
        self.process_btn.pack(pady=10)

    def set_window_center(self, width, height):
        """设置窗口固定大小并居中"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def select_input_file(self):
        file_path = filedialog.askopenfilename(
            title="选择输入CSV文件", filetypes=[("CSV文件", "*.csv")]
        )
        if file_path:
            self.input_path = file_path
            self.input_label.config(text=f"输入文件: {file_path}")

    def select_output_file(self):
        file_path = filedialog.asksaveasfilename(
            title="选择保存路径", defaultextension=".csv", filetypes=[("CSV文件", "*.csv")]
        )
        if file_path:
            self.output_path = file_path
            self.output_label.config(text=f"输出文件: {file_path}")

    def toggle_mode(self):
        """切换处理模式"""
        self.mode = "n2o" if self.mode == "o2n" else "o2n"
        if self.mode == "o2n":
            self.mode_btn.config(text=f"当前模式: old to new")
        else:
            self.mode_btn.config(text=f"当前模式: new to old")

    def process_file(self):
        if not self.input_path:
            messagebox.showwarning("错误", "请先选择输入CSV文件")
            return
        if not self.output_path:
            messagebox.showwarning("错误", "请先选择保存路径")
            return

        try:
            if self.mode == "o2n":
                old_to_new(self.input_path, self.output_path)
            if self.mode == "n2o":
                new_to_old(self.input_path, self.output_path)
            messagebox.showinfo("成功", f"CSV 文件处理完成！")
        except Exception as e:
            messagebox.showerror("错误", f"处理文件时出错: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileProcessorApp(root)
    root.mainloop()
