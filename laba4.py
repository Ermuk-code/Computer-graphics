import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

class ImageTransformApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Вариант 2")

        self.image = None
        self.transformed_image = None

        self.image_frame = tk.Label(root, text="Исходное изоражение")
        self.image_frame.grid(row=0, column=0, padx=10, pady=10)

        self.transformed_frame = tk.Label(root, text="Обработанное изображение")
        self.transformed_frame.grid(row=0, column=1, padx=10, pady=10)

        self.load_button = tk.Button(root, text="Загрузить изображение", command=self.load_image)
        self.load_button.grid(row=1, column=0, pady=10)

        self.scale_button = tk.Button(root, text="Масштабирование", command=self.scale_image)
        self.scale_button.grid(row=2, column=0, pady=5)

        self.translate_button = tk.Button(root, text="Перенос", command=self.translate_image)
        self.translate_button.grid(row=3, column=0, pady=5)

        self.transform_button = tk.Button(root, text="Функциональное преобразование", command=self.custom_transform)
        self.transform_button.grid(row=4, column=0, pady=5)

        self.save_button = tk.Button(root, text="Сохранить изображение", command=self.save_result)
        self.save_button.grid(row=5, column=0, pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Выберите изображение")
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(self.image, self.image_frame)

    def display_image(self, image, frame):
        image_copy = image.copy()
        image_copy.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(image_copy)
        frame.config(image=img_tk)
        frame.image = img_tk

    def scale_image(self):
        if self.image:
            scale_factor = float(tk.simpledialog.askstring("Масштабирование", "Введите размер масштабирования:"))
            width, height = self.image.size
            new_size = (int(width * scale_factor), int(height * scale_factor))
            self.transformed_image = self.image.resize(new_size, Image.LANCZOS)
            self.display_image(self.transformed_image, self.transformed_frame)

    def translate_image(self):
        if self.image:
            dx = int(tk.simpledialog.askstring("Перенос", "Введите x:"))
            dy = int(tk.simpledialog.askstring("Перенос", "Введите y:"))
            width, height = self.image.size
            self.transformed_image = Image.new('RGB', (width, height), (255, 255, 255))
            self.transformed_image.paste(self.image, (dx, dy))
            self.display_image(self.transformed_image, self.transformed_frame)

    def custom_transform(self):
        if self.image:
            width, height = self.image.size
            result = Image.new('RGB', (width, height))
            
            for x in range(width):
                for y in range(height):
                    new_x = np.log2(x + 1)
                    new_y = y
                    if 0 <= new_x < width and 0 <= new_y < height:
                        color = self.image.getpixel((x, y))
                        result.putpixel((int(new_x), int(new_y)), color)
            
            self.transformed_image = result
            self.display_image(self.transformed_image, self.transformed_frame)

    def save_result(self):
        if self.transformed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.transformed_image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageTransformApp(root)
    root.mainloop()