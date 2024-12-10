import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk

class PolygonApp:
    def __init__(self, master):
        self.master = master
        master.title("Polygon Drawing and Clipping")

        self.label = tk.Label(master, text="1) Для отрисовки многоугольника нажать первую кнопку\n"
                                           "2) Для отсекания многоугольника нажать вторую кнопку\n"
                                           "3) Для заливки фигуры нажать третью кнопку")
        self.label.pack()

        self.button_draw = tk.Button(master, text="Отрисовать многоугольник", command=self.draw_polygon)
        self.button_draw.pack()

        self.button_cut = tk.Button(master, text="Отсечь многоугольник", command=self.clip_polygon)
        self.button_cut.pack()

        self.button_fill = tk.Button(master, text="Залить обрезанную фигуру", command=self.fill_clipped_polygon)
        self.button_fill.pack()

        self.canvas = tk.Canvas(master, width=570, height=300)
        self.canvas.pack()

        self.points = []
        self.clipped_points = []
        self.state = 0
        self.image = None

    def draw_polygon(self):
        self.state = 1
        self.points = [
            (40, 190), (140, 120), (230, 100), (340, 70),
            (380, 150), (440, 125), (350, 200), (290, 180)
        ]

        self.image = Image.new('RGB', (570, 300), color='white')
        draw = ImageDraw.Draw(self.image)

        draw.polygon(self.points, outline='black')
        draw.rectangle([295, 50, 560, 210], outline='red')

        self.update_canvas()

    def clip_polygon(self):
        if self.state != 1:
            messagebox.showwarning("Предупреждение", "Сначала отрисуйте многоугольник")
            return

        self.state = 2
        clip_box = (295, 50, 560, 210)
        self.clipped_points = self.sutherland_hodgman_clip(self.points, clip_box)
        self.image = Image.new('RGB', (570, 300), color='white')
        draw = ImageDraw.Draw(self.image)

        if self.clipped_points:
            draw.polygon(self.clipped_points, outline='black')

        draw.rectangle(clip_box, outline='red')

        self.update_canvas()

    def sutherland_hodgman_clip(self, polygon, clip_box):
        
        def inside(p):
            return clip_box[0] <= p[0] <= clip_box[2] and clip_box[1] <= p[1] <= clip_box[3]

        def compute_intersection(p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = clip_box[0], clip_box[1]
            x4, y4 = clip_box[0], clip_box[3]
            
            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if denom == 0:
                return None
            
            px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
            py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
            
            return px, py

        output_list = polygon
        for edge in [(clip_box[0], clip_box[1], clip_box[0], clip_box[3]), 
                     (clip_box[0], clip_box[3], clip_box[2], clip_box[3]),
                     (clip_box[2], clip_box[3], clip_box[2], clip_box[1]),
                     (clip_box[2], clip_box[1], clip_box[0], clip_box[1])]:
            
            input_list = output_list
            output_list = []
            if not input_list:
                break
            
            p1 = input_list[-1]
            for p2 in input_list:
                if inside(p2):
                    if not inside(p1):
                        output_list.append(compute_intersection(p1, p2))
                    output_list.append(p2)
                elif inside(p1):
                    output_list.append(compute_intersection(p1, p2))
                p1 = p2
        
        return [p for p in output_list if p is not None]

    def fill_clipped_polygon(self):
        if self.state != 2 or not self.clipped_points:
            messagebox.showwarning("Предупреждение", "Сначала отсеките многоугольник окном")
            return

        self.state = 3

        fill_image = Image.new('RGB', (570, 300), color='white')
        fill_draw = ImageDraw.Draw(fill_image)
        fill_draw.polygon(self.clipped_points, fill=(64, 44, 168))
        self.image = fill_image
        self.update_canvas()
        
    def update_canvas(self):
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.canvas.photo = self.photo  

root = tk.Tk()
app = PolygonApp(root)
root.mainloop()