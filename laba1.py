def sign(num):
    if(num > 0):
        return 1
    if(num == 0):
        return 0
    if(num < 0):
        return -1

#Цда
def CDA(x0, y0, x1, y1, image):
    if(x1 == x0) and (y0 == y1):
        print("Отрезок является выражденным")
        return 0
    else:
        L = int(max(abs(x1 - x0), abs(y1 - y0)))
        dx = (x1 - x0) / L
        dy = (y1 - y0) / L
    
        x = x0 + sign(dx) * 0.5
        y = y0 + sign(dy) * 0.5
        for i in range(L + 1):
            if 0 <= int(x) < len(image) and 0 <= int(y) < len(image[0]):
                image[int(y)][int(x)] = (255, 255, 255)  # белый
            x += dx
            y += dy


def float_Bresenham(x0, y0, x1, y1, image):
    if(x1 == x0) and (y0 == y1):
        print("Отрезок является выражденным")
        return 0
    else:
        dx = x1 - x0
        dy = y1 - y0
        
        sx = sign(dx)
        sy = sign(dy)
        
        dx = abs(dx)
        dy = abs(dy)
        
        if dx > dy:
            err = dx // 2
            while x0 != x1:
                if 0 <= x0 < len(image) and 0 <= y0 < len(image[0]):
                    image[y0][x0] = (255, 255, 255)  # белый
                err -= dy
                if err < 0:
                    y0 += sy
                    err += dx
                x0 += sx
            if 0 <= x1 < len(image) and 0 <= y1 < len(image[0]):
                image[y1][x1] = (255, 255, 255)  # белый
        else:
            err = dy // 2
            while y0 != y1:
                if 0 <= x0 < len(image) and 0 <= y0 < len(image[0]):
                    image[y0][x0] = (255, 255, 255)  # белый
                err -= dx
                if err < 0:
                    x0 += sx
                    err += dy
                y0 += sy
            if 0 <= x1 < len(image) and 0 <= y1 < len(image[0]):
                image[y1][x1] = (255, 255, 255)  
                    
            else:
                flag = 0
                while y0 != y1:
                    if 0 <= x0 < len(image) and 0 <= y0 < len(image[0]):
                        image[y0][x0] = (255, 255, 255)  # белый
                    err -= dx
                    if err < 0:
                        x0 += sx
                        err += dy
                    y0 += sy
                if 0 <= x1 < len(image) and 0 <= y1 < len(image[0]):
                    image[y1][x1] = (255, 255, 255)

def int_Bresenham(x0, y0, x1, y1, image):
    dx = x1 - x0
    dy = y1 - y0
    dx1 = abs(dx)
    dy1 = abs(dy)
    px = 2 * dy1 - dx1

    if dy1 <= dx1:
        if dx >= 0:
            x = x0
            y = y0
            x_end = x1
        else:
            x = x1
            y = y1
            x_end = x0
        image[y][x] = (255, 255, 255)  # белый
        
        while x < x_end:
            x += 1
            if px < 0:
                px += 2 * dy1
            else:
                if dy >= 0:
                    y += 1
                else:
                    y -= 1
                px += 2 * (dy1 - dx1)
            if 0 <= x < len(image) and 0 <= y < len(image[0]):
                image[y][x] = (255, 255, 255)  # белый
    else:
        if dy >= 0:
            x = x0
            y = y0
            y_end = y1
        else:
            x = x1
            y = y1
            y_end = y0
        image[y][x] = (255, 255, 255)  # белый
        
        while (dy >= 0 and y < y_end) or (dy < 0 and y > y_end):
            y += 1 if dy >= 0 else -1
            if px <= 0:
                px += 2 * dx1
            else:
                if dx >= 0:
                    x += 1
                else:
                    x -= 1
                px += 2 * (dx1 - dy1)
            if 0 <= x < len(image) and 0 <= y < len(image[0]):
                image[y][x] = (255, 255, 255)  

def save_bmp(filename, image):
    height = len(image)
    width = len(image[0])
    
    bmp_header = bytearray([
        0x42, 0x4D,           
        0, 0, 0, 0,          
        0, 0, 0, 0,         
        54, 0, 0, 0,         
        40, 0, 0, 0,         
        width & 0xFF, (width >> 8) & 0xFF, (width >> 16) & 0xFF, (width >> 24) & 0xFF,  
        height & 0xFF, (height >> 8) & 0xFF, (height >> 16) & 0xFF, (height >> 24) & 0xFF,  
        1, 0,               
        24, 0,               
        0, 0, 0, 0,          
        0, 0, 0, 0,         
        0x13, 0x0B, 0, 0,    
        0x13, 0x0B, 0, 0,    
        0, 0, 0, 0,          
        0, 0, 0, 0           
    ])
    
    # Pixel data
    pixel_data = bytearray()
    for row in reversed(image):  # BMP format stores pixels bottom-to-top
        for r, g, b in row:
            pixel_data.append(b)  # Blue
            pixel_data.append(g)  # Green
            pixel_data.append(r)  # Red

        # Add padding to ensure row size is a multiple of 4 bytes
        padding = (4 - (width * 3) % 4) % 4
        pixel_data.extend(b'\x00' * padding)

    # Set file size
    file_size = 54 + len(pixel_data)
    bmp_header[2:6] = file_size.to_bytes(4, 'little')
    
    # Set size of bitmap data
    bmp_header[34:38] = len(pixel_data).to_bytes(4, 'little')
    
    # Write to file
    with open(filename, 'wb') as f:
        f.write(bmp_header)
        f.write(pixel_data)

if __name__ == "__main__":
    image_size = (256, 256) 
    image = [[(0, 0, 0) for i in range(image_size[1])] for j in range(image_size[0])]  
    x0, y0 = map(int, input("Координаты не должны превышать 256. Введите координаты первой точки (x0, y0): ").split())
    x1, y1 = map(int, input("Координаты не должны превышать 256. Введите координаты второй точки (x1, y1): ").split())
    if(x0 > 256 or y0 > 256 or y1 > 256 or x1 > 256):
        print("Ошибка. Координаты превышают 256")
    method_index = int(input("Введите номер метода\n 1. алгоритм Цда \n 2. Веществвенный алгоритм Брезенхема \n 3. Целочисленный алгоритм Брезенхема \n"))
    match method_index:
        case 1:
            CDA(x0, y0, x1, y1, image)
            save_bmp("CDA_line.bmp", image)
            print("Изображение сохранено как CDA_line.bmp")
        case 2:
            float_Bresenham(x0, y0, x1, y1, image)
            save_bmp("float_Bresenham_line.bmp", image)
            print("Изображение сохранено как float_Bresenham_line.bmp")
        case 3:
            int_Bresenham(x0, y0, x1, y1, image)
            save_bmp("int_Bresenham_line.bmp", image)
            print("Изображение сохранено как int_Bresenham_line.bmp")
        
    