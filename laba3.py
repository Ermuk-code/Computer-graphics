import tkinter as tk
import numpy as np
from tkinter import filedialog
from PIL import Image, ImageEnhance, ImageChops, ImageTk

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Наложение")

        self.image1 = None
        self.image2 = None
        self.image1_max_saturation = None
        self.result_image = None

        self.image_frame1 = tk.Label(root, text="Первое изображение")
        self.image_frame1.grid(row=0, column=0, padx=10, pady=10)

        self.image_frame2 = tk.Label(root, text="Второе изображение")
        self.image_frame2.grid(row=0, column=1, padx=10, pady=10)

        self.image_frame3 = tk.Label(root, text="Изображение с насыщенностью 30%")
        self.image_frame3.grid(row=1, column=0, padx=10, pady=10)

        self.image_frame4 = tk.Label(root, text="Результат прозрачного наложения")
        self.image_frame4.grid(row=1, column=1, padx=10, pady=10)

        self.load_button1 = tk.Button(root, text="Выбрать первое изображение", command=self.load_image1)
        self.load_button1.grid(row=2, column=0, pady=10)

        self.load_button2 = tk.Button(root, text="Выбрать второе изображение", command=self.load_image2)
        self.load_button2.grid(row=2, column=1, pady=10)

        self.saturation_button = tk.Button(root, text="Повысить насыщенность", command=self.inc_sat)
        self.saturation_button.grid(row=3, column=0, pady=10)

        self.process_button = tk.Button(root, text="Объединить", command=self.process_images)
        self.process_button.grid(row=3, column=1, pady=10)

        self.save_saturation_button = tk.Button(root, text="Сохранить преобразованное", command=self.save_saturation_result)
        self.save_saturation_button.grid(row=4, column=0, pady=10)

        self.save_result_button = tk.Button(root, text="Сохранить наложенное", command=self.save_result)
        self.save_result_button.grid(row=4, column=1, pady=10)

    def load_image1(self):
        file_path1 = filedialog.askopenfilename(title="Выберите первое изображение")
        if file_path1:
            self.image1 = Image.open(file_path1)
            self.display_image(self.image1, self.image_frame1)

    def load_image2(self):
        file_path2 = filedialog.askopenfilename(title="Выберите второе изображение")
        if file_path2:
            self.image2 = Image.open(file_path2)
            self.display_image(self.image2, self.image_frame2)

    def display_image(self, image, frame):
        image_copy = image.copy()
        image_copy.thumbnail((200, 200))
        img_tk = ImageTk.PhotoImage(image_copy)
        frame.config(image=img_tk)
        frame.image = img_tk

    def inc_sat(self):
        if self.image1:
            self.image1_max_saturation = self.increase_saturation(self.image1)
            self.display_image(self.image1_max_saturation, self.image_frame3)

    def increase_saturation(self, image):
        hsv_image = image.convert("HSV")
        hsv_array = np.array(hsv_image)
        h, s, v = hsv_array[..., 0], hsv_array[..., 1], hsv_array[..., 2]
        mask = v < 128
        s[mask] = np.clip(s[mask] * 1.3, 0, 255).astype(np.uint8)
        hsv_array = np.dstack((h, s, v))
        result_image = Image.fromarray(hsv_array, mode="HSV").convert("RGB")
        return result_image

    def overlay_transparency(self, image1, image2):
        width = min(image1.width, image2.width)
        height = min(image1.height, image2.height)
        image1_resized = image1.resize((width, height))
        image2_resized = image2.resize((width, height))
        array1 = np.array(image1_resized)
        array2 = np.array(image2_resized)
        overlay_array = (array1.astype(np.float32) + array2.astype(np.float32)) / 2
        overlay_array = overlay_array.astype(np.uint8)
        overlay_image = Image.fromarray(overlay_array)
        return overlay_image

    def process_images(self):
        if self.image1_max_saturation and self.image2:
            self.result_image = self.overlay_transparency(self.image1_max_saturation, self.image2)
            self.display_image(self.result_image, self.image_frame4)

    def save_saturation_result(self):
        if self.image1_max_saturation:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.image1_max_saturation.save(file_path)

    def save_result(self):
        if self.result_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.result_image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()