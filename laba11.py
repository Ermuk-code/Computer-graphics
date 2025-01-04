import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tkinter import Tk, Frame, Button, Canvas, IntVar, Label, Entry

class BezierApp:
    def __init__(self, master):
        self.master = master
        master.title("Кривые и Поверхности Безье")

        self.frame = Frame(master)
        self.frame.pack()

        self.canvas = Canvas(master, width=800, height=600)
        self.canvas.pack()

        self.num_points_var = IntVar(value=4)
        self.divisions_var = IntVar(value=10)

        Label(self.frame, text="Количество контрольных точек:").pack()
        Entry(self.frame, textvariable=self.num_points_var).pack()

        Label(self.frame, text="Количество разбиений:").pack()
        Entry(self.frame, textvariable=self.divisions_var).pack()

        self.draw_curve_button = Button(self.frame, text="Нарисовать кривую Безье", command=self.draw_bezier_curve)
        self.draw_curve_button.pack()

        self.num_surface_points_var = IntVar(value=4)

        Label(self.frame, text="Количество контрольных точек поверхности:").pack()
        Entry(self.frame, textvariable=self.num_surface_points_var).pack()

        self.draw_surface_button = Button(self.frame, text="Нарисовать поверхность Безье", command=self.draw_bezier_surface)
        self.draw_surface_button.pack()

        self.num_du_sabin_points_var = IntVar(value=4)

        Label(self.frame, text="Количество контрольных точек Ду-Сабина:").pack()
        Entry(self.frame, textvariable=self.num_du_sabin_points_var).pack()

        self.draw_du_sabin_button = Button(self.frame, text="Нарисовать поверхность Ду-Сабина", command=self.du_sabin_surface)
        self.draw_du_sabin_button.pack()

    def binomial_coefficient(self, n, k):
        if k < 0 or k > n:
            return 0
        if k == 0 or k == n:
            return 1
        k = min(k, n - k)  
        c = 1
        for i in range(k):
            c = c * (n - i) // (i + 1)
        return c

    def clear_canvas(self):
        self.canvas.delete("all")

    def draw_bezier_curve(self):
        self.clear_canvas() 
        n = self.num_points_var.get()
        divisions = self.divisions_var.get()

        points = np.random.randint(50, 750, size=(n, 2))

        for i in range(n - 1):
            self.canvas.create_line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], fill='gray', dash=(2, 2))

        bezier_points = []
        
        for t in np.linspace(0, 1, divisions):
            b_t = np.zeros(2)
            for i in range(n):
                b_t += self.binomial_coefficient(n - 1, i) * (t ** i) * ((1 - t) ** (n - 1 - i)) * points[i]
            bezier_points.append(b_t)

            if t == 0 or t == 1:
                continue
            
            if len(bezier_points) > 1:
                self.canvas.create_line(bezier_points[-2][0], bezier_points[-2][1], bezier_points[-1][0], bezier_points[-1][1], fill='blue')

    def draw_bezier_surface(self):
        self.clear_canvas()  
        n = m = self.num_surface_points_var.get()
        
        points = np.random.randint(50, 750, size=(n, m, 2))

        for i in range(n):
            for j in range(m - 1):
                self.canvas.create_line(points[i][j][0], points[i][j][1], points[i][j + 1][0], points[i][j + 1][1], fill='gray', dash=(2, 2))
        
            if i < n - 1:
                for j in range(m):
                    self.canvas.create_line(points[i][j][0], points[i][j][1], points[i + 1][j][0], points[i + 1][j][1], fill='gray', dash=(2, 2))

        surface_points = []
        
        divisions = 10
        
        for u in np.linspace(0, 1, divisions):
            row = []
            for v in np.linspace(0, 1, divisions):
                b_u = np.zeros(2)
                for i in range(n):
                    for j in range(m):
                        b_u += (self.binomial_coefficient(n - 1, i) * (u ** i) * ((1 - u) ** (n - 1 - i)) *
                                  self.binomial_coefficient(m - 1, j) * (v ** j) * ((1 - v) ** (m - 1 - j)) * points[i][j])
                row.append(b_u)
            surface_points.append(row)

        for i in range(divisions):
            for j in range(divisions - 1):
                self.canvas.create_line(surface_points[i][j][0], surface_points[i][j][1],
                                        surface_points[i][j + 1][0], surface_points[i][j + 1][1], fill='blue')

            if i < divisions - 1:
                for j in range(divisions):
                    self.canvas.create_line(surface_points[i][j][0], surface_points[i][j][1],
                                            surface_points[i + 1][j][0], surface_points[i + 1][j][1], fill='blue')
    def du_sabin_surface(self):
        resolution = 100
        num_vertices = self.num_du_sabin_points_var.get()

        x = np.linspace(-5, 5, resolution)
        y = np.linspace(-5, 5, resolution)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        vertices = []
        for i in range(num_vertices):
            x = np.random.uniform(-5, 5)  
            y = np.random.uniform(-5, 5)  
            z = np.random.uniform(0, 2)  
            vertices.append((x, y, z))

        
        for i, vertex in enumerate(vertices):
            z_value = vertex[2]  # z-координата вершины
            Z += z_value * np.exp(-((X - vertex[0]) ** 2 + (Y - vertex[1]) ** 2))

            print(f'Этап {i + 1}: Добавлена вершина {vertex} (z = {z_value})')

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.set_title('Финальная поверхность Ду-Сабина')
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        plt.show()
        
if __name__ == "__main__":
    root = Tk()
    app = BezierApp(root)
    root.mainloop()
