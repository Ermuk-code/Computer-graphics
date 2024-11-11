import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def draw_cube(ax):

    r = 1  
    vertices = np.array([[ r,  r,  r],
                         [ r, -r,  r],
                         [-r, -r,  r],
                         [-r,  r,  r],
                         [ r,  r, -r],
                         [ r, -r, -r],
                         [-r, -r, -r],
                         [-r,  r, -r]])
    
    # Ребра куба
    edges = [
        [vertices[0], vertices[1]],
        [vertices[1], vertices[2]],
        [vertices[2], vertices[3]],
        [vertices[3], vertices[0]],
        [vertices[4], vertices[5]],
        [vertices[5], vertices[6]],
        [vertices[6], vertices[7]],
        [vertices[7], vertices[4]],
        [vertices[0], vertices[4]],
        [vertices[1], vertices[5]],
        [vertices[2], vertices[6]],
        [vertices[3], vertices[7]],
    ]
    
    # Отображение рёбер
    for edge in edges:
        ax.plot3D(*zip(*edge), color='b')

def draw_dodecahedron(ax):
    phi = (1 + np.sqrt(5)) / 2  # Golden ratio
    a = 1 / phi
    b = 1

    vertices = np.array([
        [b, b, b], [b, b, -b], [b, -b, b], [b, -b, -b],
        [-b, b, b], [-b, b, -b], [-b, -b, b], [-b, -b, -b],
        [0, a, phi], [0, a, -phi], [0, -a, phi], [0, -a, -phi],
        [a, phi, 0], [a, -phi, 0], [-a, phi, 0], [-a, -phi, 0],
        [phi, 0, a], [phi, 0, -a], [-phi, 0, a], [-phi, 0, -a]
    ])

    edges = [
        [vertices[0], vertices[8]], [vertices[0], vertices[12]], [vertices[0], vertices[16]],
        [vertices[1], vertices[9]], [vertices[1], vertices[12]], [vertices[1], vertices[17]],
        [vertices[2], vertices[10]], [vertices[2], vertices[13]], [vertices[2], vertices[16]],
        [vertices[3], vertices[11]], [vertices[3], vertices[13]], [vertices[3], vertices[17]],
        [vertices[4], vertices[8]], [vertices[4], vertices[14]], [vertices[4], vertices[18]],
        [vertices[5], vertices[9]], [vertices[5], vertices[14]], [vertices[5], vertices[19]],
        [vertices[6], vertices[10]], [vertices[6], vertices[15]], [vertices[6], vertices[18]],
        [vertices[7], vertices[11]], [vertices[7], vertices[15]], [vertices[7], vertices[19]],
        [vertices[8], vertices[10]], [vertices[12], vertices[14]], [vertices[9], vertices[11]],
        [vertices[19], vertices[18]], 
        [vertices[17], vertices[16]], 
        [vertices[13], vertices[15]],
    ]


    for edge in edges:
        ax.plot3D(*zip(*edge), color='r')

def main():
    fig = plt.figure(figsize=(10, 10))
    
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.set_title('Гексаэдр (Куб)')
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_zticks([])
    draw_cube(ax1)

    ax2 = fig.add_subplot(122, projection='3d')
    ax2.set_title('Додекаэдр')
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_zticks([])
    draw_dodecahedron(ax2)

    plt.show()

if __name__ == "__main__":
    main()
