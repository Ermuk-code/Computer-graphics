import tkinter as tk


WIDTH, HEIGHT = 800, 600
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
SCALE = 20  

class Segment:
    def __init__(self, x1, y1, x2, y2):
        self.start = (x1, y1)
        self.end = (x2, y2)

    def draw(self, canvas):

        canvas.create_line(self.start[0], self.start[1], self.end[0], self.end[1], fill="white", width=2)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритм Ньюэла-Ньюэла-Санча")
        
 
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()


        self.segments = [
            Segment(100, 100, 300, 300), 
            Segment(100, 300, 300, 100)  
        ]
        

        self.scale_factor = SCALE
        

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.increase_button = tk.Button(self.button_frame, text="+ Увеличить масштаб", command=self.increase_scale)
        self.increase_button.pack(side=tk.LEFT)

        self.decrease_button = tk.Button(self.button_frame, text="- Уменьшить масштаб", command=self.decrease_scale)
        self.decrease_button.pack(side=tk.LEFT)


        self.draw_axes()
        self.draw_grid()
        self.draw_segments()
        

        self.draw_perspective_projection()

    def draw_axes(self):

        self.canvas.create_line(0, CENTER_Y, WIDTH, CENTER_Y, fill="red")  # Горизонтальная ось
        self.canvas.create_line(CENTER_X, 0, CENTER_X, HEIGHT, fill="red")  # Вертикальная ось

    def draw_grid(self):

        for i in range(0, WIDTH // self.scale_factor):
            x = i * self.scale_factor
            self.canvas.create_line(x, 0, x, HEIGHT, fill="gray", dash=(2, 2))
        for j in range(0, HEIGHT // self.scale_factor):
            y = j * self.scale_factor
            self.canvas.create_line(0, y, WIDTH, y, fill="gray", dash=(2, 2))

    def draw_segments(self):
        for segment in self.segments:
            scaled_start = (segment.start[0] * self.scale_factor,
                            segment.start[1] * self.scale_factor)
            scaled_end = (segment.end[0] * self.scale_factor,
                          segment.end[1] * self.scale_factor)
            canvas_segment = Segment(*scaled_start, *scaled_end)
            canvas_segment.draw(self.canvas)

    def draw_perspective_projection(self):
        d = 500  
        
        for segment in self.segments:
            scaled_start = (segment.start[0] * self.scale_factor,
                            segment.start[1] * self.scale_factor)
            scaled_end = (segment.end[0] * self.scale_factor,
                          segment.end[1] * self.scale_factor)

            x1_perspective = (scaled_start[0] * d) / (d + scaled_start[1])
            y1_perspective = (scaled_start[1] * d) / (d + scaled_start[1])
            x2_perspective = (scaled_end[0] * d) / (d + scaled_end[1])
            y2_perspective = (scaled_end[1] * d) / (d + scaled_end[1])
            
            self.canvas.create_line(x1_perspective + CENTER_X / 2,
                                    HEIGHT - y1_perspective,
                                    x2_perspective + CENTER_X / 2,
                                    HEIGHT - y2_perspective,
                                    fill="yellow", width=2)

    def increase_scale(self):
        if self.scale_factor < 100:  
            self.scale_factor += 5
            self.redraw()

    def decrease_scale(self):
        if self.scale_factor > 5: 
            self.scale_factor -= 5
            self.redraw()

    def redraw(self):
        self.canvas.delete("all")  
        self.draw_axes()            
        self.draw_grid()            
        self.draw_segments()        
        self.draw_perspective_projection()  

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
