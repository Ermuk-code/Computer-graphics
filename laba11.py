import numpy as np
import matplotlib.pyplot as plt
import math  # Импортируем стандартный модуль math

class BezierCurve:
    def __init__(self, control_points):
        self.control_points = np.array(control_points)

    def bernstein_poly(self, n, i, t):
        return (math.factorial(n) / (math.factorial(i) * math.factorial(n - i))) * (t ** i) * ((1 - t) ** (n - i))

    def calculate_point(self, t):
        n = len(self.control_points) - 1
        point = np.zeros(2)
        for i in range(n + 1):
            point += self.bernstein_poly(n, i, t) * self.control_points[i]
        return point

    def draw_curve(self, num_points=100):
        t_values = np.linspace(0, 1, num_points)
        curve_points = np.array([self.calculate_point(t) for t in t_values])
        plt.plot(curve_points[:, 0], curve_points[:, 1], label='Bezier Curve')
        plt.scatter(self.control_points[:, 0], self.control_points[:, 1], color='red', label='Control Points')
        plt.legend()
        plt.title('Cubic Bezier Curve')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.grid(True)
        plt.show()

class BezierSurface:
    def __init__(self, control_grid):
        self.control_grid = np.array(control_grid)

    def bernstein_poly_2d(self, n, i, m, j, u, v):
        return self.bernstein_poly(n, i, u) * self.bernstein_poly(m, j, v)

    def calculate_surface_point(self, u, v):
        n = self.control_grid.shape[0] - 1
        m = self.control_grid.shape[1] - 1
        point = np.zeros(2)
        for i in range(n + 1):
            for j in range(m + 1):
                point += self.bernstein_poly_2d(n, i, m, j, u, v) * self.control_grid[i][j]
        return point

    def draw_surface(self, num_points=10):
        u_values = np.linspace(0, 1, num_points)
        v_values = np.linspace(0, 1, num_points)
        surface_points = np.array([[self.calculate_surface_point(u, v) for u in u_values] for v in v_values])
        
        # Plotting the surface
        ax = plt.axes(projection='3d')
        ax.plot_surface(surface_points[:, :, 0], surface_points[:, :, 1], surface_points[:, :, 2], alpha=0.5)
        
        # Plotting control points
        control_x = self.control_grid[:, :, 0].flatten()
        control_y = self.control_grid[:, :, 1].flatten()
        control_z = np.zeros_like(control_x)
        
        ax.scatter(control_x, control_y, control_z, color='red', label='Control Points')
        
        ax.set_title('Bezier Surface')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_zlabel('Z-axis')
        
        plt.show()

# Example usage:
# Cubic Bezier Curve
bezier_curve = BezierCurve(control_points=[[0, 0], [1, 2], [2, -1], [3, 3]])
bezier_curve.draw_curve()

# Bezier Surface
bezier_surface = BezierSurface(control_grid=[
    [[0, 0], [1, 2]],
    [[2, -1], [3, 3]]
])
bezier_surface.draw_surface()
