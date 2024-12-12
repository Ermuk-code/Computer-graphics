import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
import numpy as np
from tkinter import filedialog, messagebox
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
        
        self.R_label = tk.Label(root, text="Радиус размытия:")
        self.R_label.grid(row=2, column=0, pady=5)
        self.radius_entry = tk.Entry(root)
        self.radius_entry.grid(row=2, column=1, pady=5)
        
        self.T_label = tk.Label(root, text="T:")
        self.T_label.grid(row=3, column=0, pady=5)
        self.T_entry = tk.Entry(root)
        self.T_entry.grid(row=3, column=1, pady=5)

        self.accept_button = tk.Button(root, text="Принять данные", command=self.accept_dimensions)
        self.accept_button.grid(row=4, column=0, pady=10)
        
        self.load_button = tk.Button(root, text="Загрузить изображение", command=self.load_image)
        self.load_button.grid(row=1, column=0, pady=10)

        self.lpf_button = tk.Button(root, text="Размытие гауссианом", command=self.low_pass_filter)
        self.lpf_button.grid(row=5, column=0, pady=5)

        self.hpf_button = tk.Button(root, text="Повышение резкости", command=self.high_pass_filter)
        self.hpf_button.grid(row=6, column=0, pady=5)

        self.save_button = tk.Button(root, text="Сохранить изображение", command=self.save_result)
        self.save_button.grid(row=6, column=1, pady=10)
        
        self.radiusnew_entry = None
        self.Tnew_entry = None
 
    def accept_dimensions(self):
        try:
            radius = int(self.radius_entry.get())
            T = int(self.T_entry.get())
            self.radiusnew_entry = radius
            self.Tnew_entry = T
            messagebox.showinfo("Данные введены", f"R: {radius}, T: {T}")
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные целые числа.")
          
    def load_image(self):
        file_path = filedialog.askopenfilename(title="Выберите изображение")
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(self.image, self.image_frame)
    def low_pass_filter(self):

        image = self.image.convert("RGB")
        width, height = image.size
        pixels = np.array(image)

        Y, X = np.ogrid[:height, :width]
        center = (width // 2, height // 2)
        mask = (X - center[0])**2 + (Y - center[1])**2 <= self.radiusnew_entry**2


        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=10))
        pixels[~mask] = np.array(blurred_image)[~mask]

        self.transformed_image = Image.fromarray(pixels)
        self.display_image(self.transformed_image, self.transformed_frame)

    def high_pass_filter(self):

        image = self.image.convert("L")  
        pixels = np.array(image)


        mask = pixels > self.Tnew_entry

        sharpened_image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150))


        result_pixels = np.where(mask, np.array(sharpened_image), pixels)

        self.transformed_image = Image.fromarray(result_pixels.astype(np.uint8))
        self.display_image(self.transformed_image, self.transformed_frame)

    def display_image(self, image, frame):
        image_copy = image.copy()
        image_copy.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(image_copy)
        frame.config(image=img_tk)
        frame.image = img_tk
    

    def save_result(self):
        if self.transformed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.transformed_image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageTransformApp(root)
    root.mainloop()


