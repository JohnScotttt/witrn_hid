import tkinter as tk
from tkinter import filedialog, messagebox


class FileProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV 文件处理工具")
        self.root.geometry("400x200")
        self.root.resizable(False, False)

        self.input_path = None
        self.output_path = None

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

        # 执行处理
        self.process_btn = tk.Button(root, text="开始处理", command=self.process_file)
        self.process_btn.pack(pady=10)

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

    def process_file(self):
        if not self.input_path:
            messagebox.showwarning("错误", "请先选择输入CSV文件")
            return
        if not self.output_path:
            messagebox.showwarning("错误", "请先选择保存路径")
            return

        try:
            old = open(self.input_path, 'rb')
            new = open(self.output_path, 'wb')
            lines = old.readlines()
            length = len(lines)
            total_time = lines[length - 1].strip().split(b",")[0]
            total_time = total_time[:9] + b"." + total_time[10:]
            new.write(b'\xef\xbb\xbf')  # Write BOM for UTF-8
            for i, line in enumerate(lines):
                if i == 0:
                    sample_sum = int(line.strip().split(b",")[1])
                    new_line = b"SUM," + str(sample_sum).encode() + b"\r\n"
                elif i == 1:
                    new_line = b"TotalTime,=" + total_time + b"\r\n"
                elif i == 2:
                    new_line = b"SampTime(ms),10\r\n"
                elif i == 3:
                    new_line = line[:9] + line[10:] + b"\r\n"
                elif i == 4:
                    new_line = b"Time(D.hh:mm:ss.ms),Voltage(V),Current(A),Power(W),Temp(\xc2\xb0C),\r\n"
                else:
                    l = [x.strip() for x in line.strip().split(b",")]
                    if l[4] == b"--":
                        l[4] = b"0.0"
                    l[0] = b"=" + l[0][:9] + b"." + l[0][10:]
                    new_line = b",".join(l) + b",\r\n"
                new.write(new_line)
            messagebox.showinfo("成功", "CSV 文件处理完成！")
        except Exception as e:
            messagebox.showerror("错误", f"处理失败: {e}")
        finally:
            if 'old' in locals():
                old.close()
            if 'new' in locals():
                new.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = FileProcessorApp(root)
    root.mainloop()
