from PIL import Image, ImageOps, ExifTags

def Convert(image):
    if image.mode != 'RGB':
        image_result = image.convert('RGB')
    else:
        image_result = image
    return image_result

def GetNFrames(image):
    try:
        return image.n_frames
    except AttributeError:
        count = 0
        try:
            while True:
                image.seek(count)
                count = count + 1
        except EOFError:
            return count

def GetExif(image): # строка
    img_exif = image.getexif()
    exiflist = []
    if img_exif is None:
        return 'None'
    else:
        for key, val in img_exif.items():
            if key in ExifTags.TAGS:
                exiflist.append(f'{ExifTags.TAGS[key]}:{val}')
        return exiflist

def Negative(image, result_image):
    result_image = ImageOps.invert(image)
    return result_image

def OnlyRed(image,result_image):
    x, y = image.size
    for i in range(x):
        for j in range(y):
            r, g, b = image.getpixel((i,j))
            g = 0
            b = 0
            result_image.putpixel((i,j),(r,g,b))
    return result_image

def OnlyGreen(image,result_image):
    x, y = image.size
    for i in range(x):
        for j in range(y):
            r, g, b = image.getpixel((i,j))
            r = 0
            b = 0
            result_image.putpixel((i,j),(r,g,b))
    return result_image

def OnlyBlue(image,result_image):
    x, y = image.size
    for i in range(x):
        for j in range(y):
            r, g, b = image.getpixel((i,j))
            r = 0
            g = 0
            result_image.putpixel((i,j),(r,g,b))
    return result_image

def RedBitPlane(image ,result_image , plane = 0):
    x, y = image.size
    for i in range(x):
        for j in range(y):
            color = image.getpixel((i,j))[0]
            color = int(format(color, '08b')[7-plane]) * 255
            result_image.putpixel((i,j),(color,color,color))
    return result_image

def GreenBitPlane(image ,result_image , plane = 0):
    x, y = image.size
    for i in range(x):
        for j in range(y):
            color = image.getpixel((i,j))[1]
            color = int(format(color, '08b')[7-plane]) * 255
            result_image.putpixel((i,j),(color,color,color))
    return result_image

def BlueBitPlane(image ,result_image , plane = 0):
    x, y = image.size
    for i in range(x):
        for j in range(y):
            color = image.getpixel((i,j))[2]
            color = int(format(color, '08b')[7-plane]) * 255
            result_image.putpixel((i,j),(color,color,color))
    return result_image

def AlphaBitPlane(image, result_image, plane = 0):
    x, y = image.size
    for i in range(x):
        for j in range(y):
            color = image.getpixel((i,j))[3]
            color = int(format(color, '08b')[7-plane]) * 255
            result_image.putpixel((i,j),(color,color,color))

def StereogramSolver(image, result_image, shift = 0):
    x, y = image.size
    clone = image.copy()
    for i in range(x):
        for j in range(y):
            r, g, b = image.getpixel((i,j))
            if i + shift >= x:
                rs, gs, bs = clone.getpixel((x - (i + shift),j))
            else:
                rs, gs, bs = clone.getpixel((i + shift,j))
            result_image.putpixel((i,j),(abs(rs - r), abs(gs - g), abs(bs - b)))
    return result_image

def SignificantBit(image, color_order = 'RGB', row_order = True, startpoint = 0, bit = 0):
    color_order = color_order.upper()
    x, y = image.size
    r ,g ,b = 0, 1, 2
    bit = 7 - int(bit) + 2
    message = ''

    color_orders = {
        'RGB': [r ,g ,b],
        'RBG': [r ,b ,g],
        'BRG': [b ,r ,g],
        'BGR': [b ,g ,r],
        'GRB': [g ,r ,b],
        'GBR': [g ,b ,r]
    }

    x = range(x)
    y = range(y)
    if startpoint == '1':
        x = reversed(x)
    elif startpoint == '2':
        y = reversed(y)
    elif startpoint == '3':
        x = reversed(x)
        y = reversed(y)

    order = color_orders[color_order]
    message = ''

    if row_order == 'True':
        for i in x:
            for j in y:
                colors = image.getpixel((i,j))
                f = format(colors[order[0]], '#010b')[bit]
                s = format(colors[order[1]], '#010b')[bit]
                t = format(colors[order[2]], '#010b')[bit]
                message = message+f+s+t
    else:
        for i in y:
            for j in x:
                colors = image.getpixel((j,i))
                f = format(colors[order[0]], '#010b')[bit]
                s = format(colors[order[1]], '#010b')[bit]
                t = format(colors[order[2]], '#010b')[bit]
                message = message+f+s+t

    return message

def Messages():
    print('Какую операцию хотите провести?\n')
    print('Negative')
    print('OnlyRed, OnlyGreen, OnlyBlue')
    print('RedBitPlane, GreenBitPlane, BlueBitPlane')
    print('StereogramSolver')
    print('SignificantBit')
    print('exit - чтобы выйти из программы\n')

if __name__ == "__main__":
    while True:
        try:
            file = input('Введите названия файла:\n$ ')
            if file == 'exit':
                exit()
            else:
                Original_Image = Image.open(file)
                break
        except FileNotFoundError:
                print('файл не найден')
    Result_Image = Image.new(Original_Image.mode, Original_Image.size, color = 'white')

    Messages()
    PlaneMessage = 'Введите просматриваемый бит (0 - 7): '
    StereogramMessage = 'Введите смещенеие: '
    SignificantBitMessages = [
            'Введите порядок цвета: ',
            'Чтение по рядам? (True, False): ',
            'Точка старта? (0,1,2,3): ',
            'Введите просматриваемый бит (0 - 7): ']
    
    # Честно.. Реализация через словарь была бы тут к месту, но по какой-то причине.
    # Когда я объявляю словарь, перед запуском программы, он проходится по всем функциями внутри объявленным
    # Следовательно, довольствуемся чем есть
    while True:
        enter = input('Выберите операцию.\n$ ')
        if enter == 'Negative':
            Negative(Original_Image, Result_Image).show()
        elif enter == 'OnlyRed':
            OnlyRed(Original_Image, Result_Image).show()
        elif enter == 'OnlyGreen':
            OnlyGreen(Original_Image, Result_Image).show()
        elif enter == 'OnlyBlue':
            OnlyBlue(Original_Image, Result_Image).show()
        elif enter == 'RedBitPlane':
            RedBitPlane(Original_Image, Result_Image, PlaneMessage).show()
        elif enter == 'GreenBitPlane':
            GreenBitPlane(Original_Image, Result_Image, PlaneMessage).show()
        elif enter == 'BlueBitPlane':
            BlueBitPlane(Original_Image, Result_Image, PlaneMessage).show()
        elif enter == 'StereogramSolver':
            StereogramSolver(Original_Image, Result_Image, StereogramMessage).show()
        elif enter == 'SignificantBit':
            a = SignificantBit(Original_Image, input(SignificantBitMessages[0]), input(SignificantBitMessages[1]), input(SignificantBitMessages[2]), input(SignificantBitMessages[3]))
            f = open("result.txt", "x")
            f.write(a)
            f.close()
        elif enter == 'exit':
            exit()
        else:
            print('Такой операции нету')