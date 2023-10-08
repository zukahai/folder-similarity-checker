import tkinter as tk
from tkinter import filedialog
import json
from main import HaiZuka

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Kiểm tra thư mục tương đồng | HaiZuka")
        self.root.geometry("425x500")  # Đặt kích thước cửa sổ là 500x500
        # không thể thay đổi kích thước
        self.root.resizable(False, False)  # Không thể thay đổi kích thước cửa sổ
        # Hiện thị giữa màn hình
        self.root.geometry("425x500+{}+{}".format(self.root.winfo_screenwidth() // 2 - 425 // 2, self.root.winfo_screenheight() // 2 - 500 // 2))

        self.folder1_path = ""
        self.folder2_path = ""
        self.dark_mode = True  # Biến để theo dõi chế độ light mode

        self.template_json = {
            "folder1": "",
            "folder2": "",
        }

        self.create_ui()

    def create_ui(self):
        # TextArea để hiển thị đường dẫn
        self.text_area = tk.Text(self.root, wrap=tk.WORD, height=26, width=50)
        self.text_area.grid(row=0, column=0, columnspan=4, padx=10, pady=10)  # Thay đổi columnspan thành 4

        # Nút 1: Chọn đường dẫn cho thư mục 1
        button1 = tk.Button(self.root, text="Chọn Folder 1", command=self.select_folder1)
        button1.grid(row=1, column=0, padx=10, pady=10)  # Điều chỉnh cột

        # Nút 2: Chọn đường dẫn cho thư mục 2
        button2 = tk.Button(self.root, text="Chọn Folder 2", command=self.select_folder2)
        button2.grid(row=1, column=1, padx=10, pady=10)  # Điều chỉnh cột

        # Nút 3: Hiển thị đường dẫn của cả hai thư mục
        button3 = tk.Button(self.root, text="Hiển Thị Kết Quả", command=self.display_paths)
        button3.grid(row=1, column=2, padx=10, pady=10)  # Điều chỉnh cột

        # Nút 4: Đổi theme
        theme_button = tk.Button(self.root, text="Đổi Theme", command=self.toggle_theme)
        theme_button.grid(row=1, column=3, padx=10, pady=10)  # Điều chỉnh cột

        self.update_ui()

    def toggle_theme(self):
        # Chuyển đổi giữa light và dark theme bằng cách thay đổi màu sắc
        self.dark_mode = not self.dark_mode
        self.update_ui()

    def update_ui(self):
        if self.dark_mode:
            # Dark theme
            self.root.configure(bg="#333333")
            self.text_area.configure(bg="#444444", fg="#FFFFFF")
            button_style = {"bg": "#444444", "fg": "#FFFFFF"}
        else:
            # Light theme
            self.root.configure(bg="white")
            self.text_area.configure(bg="lightgray", fg="black")
            button_style = {"bg": "lightgray", "fg": "black"}

        # Cập nhật màu sắc của các nút
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(**button_style)

    def select_folder1(self):
        self.folder1_path = filedialog.askdirectory()
        print("Folder 1:", self.folder1_path)
        self.template_json['folder1'] = self.folder1_path
        self.set_textarea(self.template_json)

    def select_folder2(self):
        self.folder2_path = filedialog.askdirectory()
        print("Folder 2:", self.folder2_path)
        self.template_json['folder2'] = self.folder2_path
        self.set_textarea(self.template_json)

    def display_paths(self):
        haizuka = HaiZuka()
        similarities = haizuka.similarities_folder(self.folder1_path, self.folder2_path)
        self.set_textarea(similarities)
        haizuka.write_json_utf8()
        

    def set_textarea(self, text):
        formatted_json = json.dumps(text, indent=4)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, formatted_json)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
