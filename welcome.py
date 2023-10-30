import tkinter as tk
from PIL import Image, ImageTk
import requests

# Tạo hàm để mở liên kết
def open_link(url):
    import webbrowser
    webbrowser.open_new_tab(url)

# Tạo hàm để đóng ứng dụng
def close_app():
    app.destroy()

# Tạo cửa sổ ứng dụng
app = tk.Tk()
app.title("Thank you for installing the application | HaiZuka -  Folder Similarity Checker")

# Lấy kích thước màn hình
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Kích thước cửa sổ
window_width = 800  # Đặt chiều rộng của cửa sổ
window_height = 600  # Đặt chiều cao của cửa sổ

# Tính toán vị trí để căn giữa cửa sổ
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Đặt kích thước và vị trí của cửa sổ
app.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Thêm một Label cho dòng chữ ở phía trên
top_label = tk.Label(app, text="Installation complete, thank you for using the software", font=("Helvetica", 16, "bold"), fg="red")
top_label.pack(pady=20)

# Tạo Frame chứa chữ và biểu tượng
frame = tk.Frame(app)
frame.pack()

# Tải hình ảnh từ tệp ảnh (đảm bảo thay thế 'your_image_path' bằng đường dẫn đến tệp ảnh thực tế)
image_path = 'https://raw.githubusercontent.com/zukahai/folder-similarity-checker/main/demo/fsc2.png'
image = Image.open(requests.get(image_path, stream=True).raw)
image = ImageTk.PhotoImage(image)


# Hiển thị hình ảnh và liên kết đến trang web (chưa có liên kết thực tế)
def open_webpage(event):
    open_link("https://example.com")

# Bỏ viền cho hình ảnh
image_button = tk.Button(frame, image=image, command=open_webpage, cursor="hand2", borderwidth=0, highlightthickness=0)
image_button.pack()

# Tạo một Frame để chứa biểu tượng GitHub và Facebook
icon_frame = tk.Frame(frame)
icon_frame.pack()

# Tải hình ảnh biểu tượng GitHub (thay thế 'github_icon.png' bằng đường dẫn đến biểu tượng GitHub)
image_path = 'https://raw.githubusercontent.com/zukahai/folder-similarity-checker/main/demo/github_icon.png'
github_icon = Image.open(requests.get(image_path, stream=True).raw)
github_icon = ImageTk.PhotoImage(github_icon)

# Tạo nút hình ảnh cho GitHub và bỏ viền
github_button = tk.Button(icon_frame, image=github_icon, command=lambda: open_link("https://github.com/zukahai"), borderwidth=0, highlightthickness=0)
github_button.pack(side=tk.LEFT, padx=10)

# Tải hình ảnh biểu tượng Facebook (thay thế 'facebook_icon.png' bằng đường dẫn đến biểu tượng Facebook)
image_path = 'https://raw.githubusercontent.com/zukahai/folder-similarity-checker/main/demo/facebook_icon.png'
facebook_icon = Image.open(requests.get(image_path, stream=True).raw)
facebook_icon = ImageTk.PhotoImage(facebook_icon)

# Tạo nút hình ảnh cho Facebook và bỏ viền
facebook_button = tk.Button(icon_frame, image=facebook_icon, command=lambda: open_link("https://www.facebook.com/chiatayde"), borderwidth=0, highlightthickness=0)
facebook_button.pack(side=tk.LEFT, padx=10)

# Tạo nút để đóng ứng dụng và đặt pady cho nó
close_button = tk.Button(app, text="Close", command=close_app)
close_button.pack(pady=5)

# Hiển thị cửa sổ
app.mainloop()
