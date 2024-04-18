import os
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox
from PIL import Image


image_files = []
def select_images():
    """弹出对话框选择图片，返回选中的图片路径列表"""
    return filedialog.askopenfilenames(
        title='选择图像',
        filetypes=[('Image files', '*.jpg *.jpeg *.png *.gif *.bmp *.tiff'), ('All files', '*.*')]
    )


def resize_images():
    """根据用户输入的宽度和高度，选择图片并调整其分辨率"""
    global image_files
    new_width = int(width_entry.get())
    new_height = int(height_entry.get())

    if not image_files:
        messagebox.showerror("错误", "请先选择图像。")
        return

    for image_file in image_files:
        file_name_without_ext, file_ext = os.path.splitext(os.path.basename(image_file))
        target_folder = create_folder_based_on_resolution(image_file, new_width, new_height)

        with Image.open(image_file) as img:
            img_resized = img.resize((new_width, new_height), Image.LANCZOS)
            output_file = os.path.join(target_folder, file_name_without_ext + file_ext)
            img_resized.save(output_file)
            print(f"Resized image saved: {output_file}")

    # 清空选择的图片，以便下次选择
    image_files = []


def create_folder_based_on_resolution(image_file, new_width, new_height):
    """创建一个基于新分辨率的文件夹并返回其路径"""
    folder_name = f"{new_width}x{new_height}"
    target_folder = os.path.join(os.path.dirname(image_file), folder_name)
    os.makedirs(target_folder, exist_ok=True)
    return target_folder


def on_closing():
    """关闭窗口前确认是否退出程序"""
    if messagebox.askokcancel("退出", "你想退出吗？"):
        root.destroy()


# 创建主窗口
root = Tk()
root.title("图像缩放器")
root.geometry("300x200")

# 设置窗口关闭事件
root.protocol("WM_DELETE_WINDOW", on_closing)

# 创建并放置宽度输入框
width_label = Label(root, text="输入新宽度:")
width_label.pack()
width_entry = Entry(root)
width_entry.pack()

# 创建并放置高度输入框
height_label = Label(root, text="输入新高度:")
height_label.pack()
height_entry = Entry(root)
height_entry.pack()

# 创建选择图片按钮
select_button = Button(root, text="选择图像", command=lambda: [image_files.extend(select_images())])
select_button.pack()

# 创建调整图片分辨率按钮
resize_button = Button(root, text="调整图像大小", command=resize_images)
resize_button.pack()

# 创建退出按钮
exit_button = Button(root, text="退出", command=root.destroy)
exit_button.pack()

# 运行主循环
root.mainloop()