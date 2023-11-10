import tkinter as tk
from tkinter import filedialog
import json
from main import HaiZuka
from util import Util
from scan import check_folder
import os
import ctypes
import sys
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Similarity Checker | HaiZuka")
        self.width = 583
        self.root.geometry(str(self.width) + "x570")
        self.root.resizable(False, False)
        self.root.geometry(str(self.width) + "x570+{}+{}".format(self.root.winfo_screenwidth() // 2 - self.width // 2, self.root.winfo_screenheight() // 2 - 600 // 2))

        self.style = ThemedStyle(self.root)
        self.style.set_theme("scidblue")

        self.folder1_path = ""
        self.folder2_path = ""
        self.folder_all_path = ""
        self.dark_mode = True

        json_data = Util.read_file_json("theme.json")
        self.index_theme = int(json_data["index"]) - 1
        #https://paletton.com/#uid=13a0u0kqft9gjCWllvetvo4wOj5
        self.theme = json_data["themes"]

        self.template_json = {
            "folder1": "",
            "folder2": "",
        }

        self.create_ui()

    def create_ui(self):
        Util.info()
        select_icon = Image.open("./assets/icons/1.png")
        select_icon = select_icon.resize((32, 32), Image.LANCZOS)
        select_icon = ImageTk.PhotoImage(select_icon)

        compare_icon = Image.open("./assets/icons/2.png")
        compare_icon = compare_icon.resize((32, 32), Image.LANCZOS)
        compare_icon = ImageTk.PhotoImage(compare_icon)

        result_icon = Image.open("./assets/icons/3.png")
        result_icon = result_icon.resize((32, 32), Image.LANCZOS)
        result_icon = ImageTk.PhotoImage(result_icon)

        refesh_icon = Image.open("./assets/icons/4.png")
        refesh_icon = refesh_icon.resize((32, 32), Image.LANCZOS)
        refesh_icon = ImageTk.PhotoImage(refesh_icon)

        change_theme_icon = Image.open("./assets/icons/5.png")
        change_theme_icon = change_theme_icon.resize((32, 32), Image.LANCZOS)
        change_theme_icon = ImageTk.PhotoImage(change_theme_icon)

        folder_result_icon = Image.open("./assets/icons/6.png")
        folder_result_icon = folder_result_icon.resize((32, 32), Image.LANCZOS)
        folder_result_icon = ImageTk.PhotoImage(folder_result_icon)

        self.text_area = tk.Text(self.root, wrap=tk.WORD, height=26, width=70)
        self.text_area.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.text_area.bind("<KeyPress>", lambda e: "break")



        # Hàng 1
        self.frame1 = tk.Frame(self.root)
        self.frame1.configure(bg="#333333")
        self.frame1.grid(row=1, column=0, columnspan=4, padx=10, pady=1)
        self.frame1.grid_columnconfigure(0, weight=1)
        
        button_font = ("Arial", 12)
        button_bg_color = "#776B5D"
        button_fg_color = "#F3EEEA"

        # Đường viền (border) cho các button
        button_borderwidth = 2
        button_relief = "groove"  # Loại border

        self.button1 = tk.Button(self.frame1, text="Select Folder 1", command=self.select_folder1, font=button_font, bg=button_bg_color, fg=button_fg_color, borderwidth=button_borderwidth, relief=button_relief, image=select_icon, compound="left")
        self.button1.image = select_icon  # Giữ tham chiếu đến biểu tượng
        self.button1.grid(row=0, column=0, padx=10, pady=10)

        self.button2 = tk.Button(self.frame1, text="Select Folder 2", command=self.select_folder2, font=button_font, bg=button_bg_color, fg=button_fg_color, borderwidth=button_borderwidth, relief=button_relief, image=select_icon, compound="left")
        self.button2.image = select_icon  # Giữ tham chiếu đến biểu tượng
        self.button2.grid(row=0, column=1, padx=10, pady=10)

        self.compare_button = tk.Button(self.frame1, text="Compare Each Pair", command=self.compare_pairs, font=button_font, bg=button_bg_color, fg=button_fg_color, borderwidth=button_borderwidth, relief=button_relief, image=compare_icon, compound="left")
        self.compare_button.image = compare_icon  # Giữ tham chiếu đến biểu tượng
        self.compare_button.grid(row=0, column=2, padx=10, pady=10)

        # Hàng 2
        self.frame2 = tk.Frame(self.root)
        self.frame2.configure(bg="#333333")
        self.frame2.grid(row=2, column=0, columnspan=4, padx=10, pady=1)
        self.frame2.grid_columnconfigure(0, weight=1)

        self.result_button = tk.Button(self.frame2, text="Start", command=self.display_paths, font=button_font, bg=button_bg_color, fg=button_fg_color, borderwidth=button_borderwidth, relief=button_relief, image=result_icon, compound="left")
        self.result_button.image = result_icon  # Giữ tham chiếu đến biểu tượng
        self.result_button.grid(row=0, column=0, padx=10, pady=10)
        self.result_button.config(state=tk.DISABLED)

        self.refresh_button = tk.Button(self.frame2, text="Refresh", command=self.refresh, font=button_font, bg=button_bg_color, fg=button_fg_color, borderwidth=button_borderwidth, relief=button_relief, image=refesh_icon, compound="left")
        self.refresh_button.image = refesh_icon  # Giữ tham chiếu đến biểu tượng
        self.refresh_button.grid(row=0, column=1, padx=10, pady=10)

        self.theme_button = tk.Button(self.frame2, text="Change Theme", command=self.toggle_theme, font=button_font, bg=button_bg_color, fg=button_fg_color, borderwidth=button_borderwidth, relief=button_relief, image=change_theme_icon, compound="left")
        self.theme_button.image = change_theme_icon  # Giữ tham chiếu đến biểu tượng
        self.theme_button.grid(row=0, column=2, padx=10, pady=10)

        self.open_folder_button = tk.Button(self.frame2, text="Results Container", command=self.open_folder, font=button_font, bg=button_bg_color, fg=button_fg_color, borderwidth=button_borderwidth, relief=button_relief, image=folder_result_icon, compound="left")
        self.open_folder_button.image = folder_result_icon  # Giữ tham chiếu đến biểu tượng
        self.open_folder_button.grid(row=0, column=3, padx=10, pady=10)


        self.update_ui()


    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.update_ui()

    def update_ui(self):
        self.index_theme += 1
        self.index_theme %= len(self.theme)
        bg = self.theme[self.index_theme]["bg_button"]
        fg = self.theme[self.index_theme]["fg"]
        text_area_bg = self.theme[self.index_theme]["textarea"]
        frame_bg = self.theme[self.index_theme]["bg"]
        self.frame1.configure(bg=frame_bg)
        self.frame2.configure(bg=frame_bg)
        self.root.configure(bg=frame_bg)
        self.text_area.configure(bg=text_area_bg, fg=fg)

        self.refresh_button.configure(bg=bg, fg=fg)
        self.result_button.configure(bg=bg, fg=fg)
        self.compare_button.configure(bg=bg, fg=fg)
        self.button1.configure(bg=bg, fg=fg)
        self.button2.configure(bg=bg, fg=fg)
        self.theme_button.configure(bg=bg, fg=fg)
        self.open_folder_button.configure(bg=bg, fg=fg)

        Util.write_json_utf8("theme.json", {'index': self.index_theme, 'themes': self.theme})
        try:
            current_text = self.text_area.get("1.0", "end-1c")
            json_data = json.loads(current_text)
        except:
            json_data = self.template_json
        self.set_textarea(json_data)

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
        print("Folder path:", self.folder_all_path)
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
        
        self.text_area.tag_configure("red_text", foreground="red")
        self.text_area.tag_configure("bracket_text", foreground="#34ebde")
        self.text_area.tag_configure("true_text", foreground=self.theme[self.index_theme]["fg_textarea_1"])
        self.text_area.tag_configure("false_text", foreground=self.theme[self.index_theme]["fg_textarea_2"])
        self.text_area.tag_configure("yellow_text", foreground="yellow")
        self.text_area.tag_configure("custom_bold", font=("Arial", 10, "bold"))
        
        flag = False
        for ch in str(formatted_json):
            if ch in ['{', '}', ':']:
                self.text_area.insert("insert", ch, "custom_bold false_text")
            elif ch in ['/', '[', ']']:
                self.text_area.insert("insert", ch, "custom_bold true_text")
            else:
                if ch == '"':
                    flag = not flag
                    self.text_area.insert("insert", ch, "custom_bold fg_text")
                else:
                    if flag:
                        self.text_area.insert("insert", ch, "custom_bold true_text")
                    else:
                        self.text_area.insert("insert", ch, "custom_bold false_text")
    
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

