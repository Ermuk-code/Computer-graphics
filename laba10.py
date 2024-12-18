import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
from tkinter import filedialog, messagebox
import numpy as np
import cv2

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

def bilinear_interpolation(img, x, y):
    h, w = img.shape[:2]
    if x < 0 or x >= w or y < 0 or y >= h:
        return 0  # Возвращаем черный цвет, если координаты выходят за пределы изображения

    l = int(np.floor(x))
    k = int(np.floor(y))
    a = x - l
    b = y - k

    # Получаем значения пикселей
    f_lk = img[k, l] if k < h and l < w else 0
    f_l1k = img[k, l + 1] if k < h and l + 1 < w else 0
    f_lk1 = img[k + 1, l] if k + 1 < h and l < w else 0
    f_l1k1 = img[k + 1, l + 1] if k + 1 < h and l + 1 < w else 0

    # Билинейная интерполяция
    g = (1 - a) * (1 - b) * f_lk + \
        a * (1 - b) * f_l1k + \
        b * (1 - a) * f_lk1 + \
        a * b * f_l1k1

    return g

def apply_affine_transform(img, transformation_matrix, output_shape):
    output_img = np.zeros(output_shape, dtype=img.dtype)
    
    for y in range(output_shape[0]):
        for x in range(output_shape[1]):
            # Применяем обратное преобразование для получения исходных координат
            original_coords = np.dot(np.linalg.inv(transformation_matrix), np.array([x, y, 1]))
            orig_x, orig_y = original_coords[0], original_coords[1]

            # Используем билинейную интерполяцию для получения значения пикселя
            pixel_value = bilinear_interpolation(img, orig_x, orig_y)
            output_img[y, x] = pixel_value

    return output_img

def scale_image(img, scale_factor):
    transformation_matrix = np.array([
        [scale_factor, 0, 0],
        [0, scale_factor, 0],
        [0, 0, 1]
    ])
    
    output_shape = (int(img.shape[0] * scale_factor), int(img.shape[1] * scale_factor), img.shape[2])
    
    return apply_affine_transform(img, transformation_matrix, output_shape)

def rotate_image(img, angle):
    angle_rad = np.radians(angle)
    transformation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad), 0],
        [np.sin(angle_rad), np.cos(angle_rad), 0],
        [0, 0, 1]
    ])
    
    # Определяем размер выходного изображения
    height, width = img.shape[:2]
    
    # Вычисляем размеры нового изображения после поворота
    new_width = int(abs(width * np.cos(angle_rad)) + abs(height * np.sin(angle_rad)))
    new_height = int(abs(height * np.cos(angle_rad)) + abs(width * np.sin(angle_rad)))
    
    output_shape = (new_height, new_width, img.shape[2])
    
    return apply_affine_transform(img, transformation_matrix, output_shape)

def shear_image(img, shear_factor):
    transformation_matrix = np.array([
        [1, shear_factor, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])
    
    output_shape = (img.shape[0], int(img.shape[1] + img.shape[0] * shear_factor), img.shape[2])
    
    return apply_affine_transform(img, transformation_matrix, output_shape)

def main():
    # Загружаем изображение
    img = cv2.imread(self.image)
    scale_factor = float(input("Введите масштабирование "))
    angle = float(input("Введите угол поворота "))
    shear_factor = float(input("Введите скос "))
    if img is None:
        print("Ошибка: изображение не найдено.")
        return
    
    # Применяем масштабирование
    scaled_img = scale_image(img, scale_factor)
    cv2.imwrite('scaled_image.jpg', scaled_img)

    # Применяем поворот
    rotated_img = rotate_image(img, angle)
    cv2.imwrite('rotated_image.jpg', rotated_img)

    # Применяем скошение
    sheared_img = shear_image(img, shear_factor)
    cv2.imwrite('sheared_image.jpg', sheared_img)

if __name__ == '__main__':
    main()
