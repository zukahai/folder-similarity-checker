import tkinter as tk
from tkinter import filedialog
import json
from main import HaiZuka
from util import Util
from scan import check_folder
import os
import ctypes
import sys

class App:
    def __init__(self, root):
        Util.info()
        self.root = root
        self.root.title("Kiểm tra thư mục tương đồng | HaiZuka")
        self.root.geometry("425x500")
        self.root.resizable(False, False)
        self.root.geometry("425x550+{}+{}".format(self.root.winfo_screenwidth() // 2 - 425 // 2, self.root.winfo_screenheight() // 2 - 500 // 2))

        self.folder1_path = ""
        self.folder2_path = ""
        self.folder_all_path = ""
        self.dark_mode = True

        self.template_json = {
            "folder1": "",
            "folder2": "",
        }

        self.create_ui()

    def create_ui(self):
        self.text_area = tk.Text(self.root, wrap=tk.WORD, height=26, width=50)
        self.text_area.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Hàng 1
        self.frame1 = tk.Frame(self.root)
        self.frame1.configure(bg="#333333")
        self.frame1.grid(row=1, column=0, columnspan=4, padx=10, pady=1)
        
        self.button1 = tk.Button(self.frame1, text="Chọn Folder 1", command=self.select_folder1)
        self.button1.grid(row=0, column=0, padx=10, pady=10)

        self.button2 = tk.Button(self.frame1, text="Chọn Folder 2", command=self.select_folder2)
        self.button2.grid(row=0, column=1, padx=10, pady=10)

        self.compare_button = tk.Button(self.frame1, text="So sánh từng cặp", command=self.compare_pairs)
        self.compare_button.grid(row=0, column=2, padx=10, pady=10)

        # Hàng 2
        self.frame2 = tk.Frame(self.root)
        self.frame2.configure(bg="#333333")
        self.frame2.grid(row=2, column=0, columnspan=4, padx=10, pady=1)
        
        self.result_button = tk.Button(self.frame2, text="Hiển Thị Kết Quả", command=self.display_paths)
        self.result_button.grid(row=0, column=0, padx=10, pady=10)
        self.result_button.config(state=tk.DISABLED)

        self.refresh_button = tk.Button(self.frame2, text="Làm mới", command=self.refresh)
        self.refresh_button.grid(row=0, column=1, padx=10, pady=10)

        self.theme_button = tk.Button(self.frame2, text="Đổi Theme", command=self.toggle_theme)
        self.theme_button.grid(row=0, column=2, padx=10, pady=10)

        self.open_folder_button = tk.Button(self.frame2, text="File kết quả", command=self.open_folder)
        self.open_folder_button.grid(row=0, column=3, padx=10, pady=10)

        self.update_ui()


    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.update_ui()

    def update_ui(self):
        if self.dark_mode:
            self.frame1.configure(bg="#333333")
            self.frame2.configure(bg="#333333")
            self.root.configure(bg="#333333")
            self.text_area.configure(bg="#444444", fg="#FFFFFF")
            button_style = {"bg": "#444444", "fg": "#FFFFFF"}
        else:
            self.root.configure(bg="white")
            self.frame1.configure(bg="white")
            self.frame2.configure(bg="white")
            self.text_area.configure(bg="lightgray", fg="black")
            button_style = {"bg": "lightgray", "fg": "black"}

        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(**button_style)

    def select_folder1(self):
        self.folder1_path = filedialog.askdirectory()
        print("Folder 1:", self.folder1_path)
        self.template_json['folder1'] = self.folder1_path
        self.set_textarea(self.template_json)

        self.disable_buttons()

    def select_folder2(self):
        self.folder2_path = filedialog.askdirectory()
        print("Folder 2:", self.folder2_path)
        self.template_json['folder2'] = self.folder2_path
        self.set_textarea(self.template_json)

        self.disable_buttons()

    def compare_pairs(self):
        self.template_json = {}
        self.folder_all_path = filedialog.askdirectory()
        print("Folde:", self.folder1_path)
        self.template_json['folder'] = self.folder_all_path
        self.set_textarea(self.template_json)

        self.disable_buttons()

    def display_paths(self):
        if (self.folder1_path == "" or self.folder2_path == "") and self.folder_all_path == "":
            return
        if self.folder_all_path == "":
            haizuka = HaiZuka()
            similarities = haizuka.similarities_folder(self.folder1_path, self.folder2_path)
            self.set_textarea(similarities)
            haizuka.write_json_utf8()
        else:
            similarities = check_folder(self.folder_all_path)
            self.set_textarea(similarities)
            HaiZuka.write_json_utf8_2(similarities)
        self.disable_buttons()

    def refresh(self):
        self.folder1_path = ""
        self.folder2_path = ""
        self.folder_all_path = ""

        self.template_json = {
            "folder1": "",
            "folder2": "",
        }
        self.set_textarea(self.template_json)

        self.result_button.config(state=tk.DISABLED)
        self.compare_button.config(state=tk.NORMAL)
        self.button1.config(state=tk.NORMAL)
        self.button2.config(state=tk.NORMAL)

    def open_folder(self):
        # Mở thư mục results trong explorer
        os.startfile('results')

    def set_textarea(self, text):
        formatted_json = json.dumps(text, indent=4)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, formatted_json)
    
    def disable_buttons(self):
        self.button1.config(state=tk.NORMAL)
        self.button2.config(state=tk.NORMAL)
        self.compare_button.config(state=tk.NORMAL)
        self.result_button.config(state=tk.DISABLED)

        if self.folder1_path != "" and self.folder2_path != "" or self.folder_all_path != "":
            self.result_button.config(state=tk.NORMAL)

        if self.folder_all_path != "":
            self.button1.config(state=tk.DISABLED)
            self.button2.config(state=tk.DISABLED)

        if self.folder1_path != "" or self.folder2_path != "":
            self.compare_button.config(state=tk.DISABLED)
   

if __name__ == "__main__":
    def run_as_admin():
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            # If not running as administrator, relaunch as administrator
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
    run_as_admin()
    root = tk.Tk()
    app = App(root)
    root.mainloop()

