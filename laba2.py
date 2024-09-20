def drawpixel(x, y, image): 
    if 0 <= int(x) < len(image) and 0 <= int(y) < len(image[0]):
        image[int(y)][int(x)] = (255, 255, 255)
        
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
    
    pixel_data = bytearray()
    for row in reversed(image):  
        for r, g, b in row:
            pixel_data.append(b)  
            pixel_data.append(g) 
            pixel_data.append(r)  

        
        padding = (4 - (width * 3) % 4) % 4
        pixel_data.extend(b'\x00' * padding)

  
    file_size = 54 + len(pixel_data)
    bmp_header[2:6] = file_size.to_bytes(4, 'little')
    
   
    bmp_header[34:38] = len(pixel_data).to_bytes(4, 'little')
    print('Файл сохранен')

    with open(filename, 'wb') as f:
        f.write(bmp_header)
        f.write(pixel_data)
def circle_Bresenham(x1, y1, r, image):
    x = 0
    y = r
    delta = 1 - 2 * r
    err = 0
    while(y >= x):
        drawpixel(x1 + x, y1 + y, image)
        drawpixel(x1 + x, y1 - y, image)
        drawpixel(x1 - x, y1 + y, image)
        drawpixel(x1 - x, y1 - y, image)
        drawpixel(x1 + y, y1 + x, image)
        drawpixel(x1 + y, y1 - x, image)
        drawpixel(x1 - y, y1 + x, image)
        drawpixel(x1 - y, y1 - x, image)
        err = 2 * (delta + y) - 1
        if((delta < 0) and (err <= 0)):
            x += 1
            delta += 2 * x + 1
            continue
        if ((delta > 0) and (err > 0)):
            y -= 1
            delta -= 2 * y + 1
            continue
        x += 1
        y -= 1
        delta += 2 * (x - y)
image_size = (256, 256)
image = [[(0, 0, 0) for i in range(image_size[1])] for j in range(image_size[0])]
center_x, center_y, radius = map(int, input('Координаты не должны превышать 256. Введите координаты центра окружности (x, y, R): ').split())
circle_Bresenham(center_x, center_y, radius, image)
save_bmp('circle.bmp', image)

    