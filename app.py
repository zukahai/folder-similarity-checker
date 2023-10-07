import tkinter as tk
from tkinter import filedialog
import json
from main import HaiZuka

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Kiểm tra thư mục tương đồng | HaiZuka")
        self.root.geometry("425x500")  # Đặt kích thước cửa sổ là 500x500

        self.folder1_path = ""
        self.folder2_path = ""

        self.create_ui()

    def create_ui(self):
        # TextArea để hiển thị đường dẫn
        self.text_area = tk.Text(self.root, wrap=tk.WORD, height=26, width=50)
        self.text_area.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Nút 1: Chọn đường dẫn cho thư mục 1
        button1 = tk.Button(self.root, text="Chọn Folder 1", command=self.select_folder1)
        button1.grid(row=1, column=0, padx=20, pady=10)

        # Nút 2: Chọn đường dẫn cho thư mục 2
        button2 = tk.Button(self.root, text="Chọn Folder 2", command=self.select_folder2)
        button2.grid(row=1, column=1, padx=20, pady=10)

        # Nút 3: Hiển thị đường dẫn của cả hai thư mục
        button3 = tk.Button(self.root, text="Hiển Thị Kết Quả", command=self.display_paths)
        button3.grid(row=1, column=2, padx=20, pady=10)

    def select_folder1(self):
        self.folder1_path = filedialog.askdirectory()
        print("Folder 1:", self.folder1_path)

    def select_folder2(self):
        self.folder2_path = filedialog.askdirectory()
        print("Folder 2:", self.folder2_path)

    def display_paths(self):
        haizuka = HaiZuka()
        similarities = haizuka.similarities_folder(self.folder1_path, self.folder2_path)

        # Biến đổi dữ liệu JSON thành chuỗi đẹp hơn
        formatted_json = json.dumps(similarities, indent=4)

        self.text_area.delete(1.0, tk.END)  # Xóa nội dung cũ
        self.text_area.insert(tk.END, formatted_json)  # Thêm nội dung mới

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
