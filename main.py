from PIL import Image, ImageOps, ExifTags
import re

def Convert(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    return image

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
    img_exif, exiflist = image.getexif(), []
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
        for ii in range(y):
            r = image.getpixel((i,ii))[0]
            result_image.putpixel((i,ii),(r,0,0))
    return result_image

def OnlyGreen(image,result_image):
    x, y = image.size
    for i in range(x):
        for ii in range(y):
            g = image.getpixel((i,ii))[1]
            result_image.putpixel((i,ii),(0,g,0))
    return result_image

def OnlyBlue(image,result_image):
    x, y = image.size
    for i in range(x):
        for ii in range(y):
            b = image.getpixel((i,ii))[2]
            result_image.putpixel((i,ii),(0,0,b))
    return result_image

def RedBitPlane(image,result_image,plane=0):
    x, y = image.size
    for i in range(x):
        for ii in range(y):
            color = image.getpixel((i,ii))[0]
            color = int(format(color, '08b')[plane]) * 255
            result_image.putpixel((i,ii),(color,color,color))
    return result_image

def GreenBitPlane(image,result_image,plane=0):
    x, y = image.size
    for i in range(x):
        for ii in range(y):
            color = image.getpixel((i,ii))[1]
            color = int(format(color, '08b')[plane]) * 255
            result_image.putpixel((i,ii),(color,color,color))
    return result_image

def BlueBitPlane(image,result_image,plane=0):
    x, y = image.size
    for i in range(x):
        for ii in range(y):
            color = image.getpixel((i,ii))[2]
            color = int(format(color, '08b')[plane]) * 255
            result_image.putpixel((i,ii),(color,color,color))
    return result_image

def AlphaBitPlane(image,result_image,plane=0):
    if image.mode == 'RGBA':
        x, y = image.size
        for i in range(x):
            for ii in range(y):
                color = image.getpixel((i,ii))[3]
                color = int(format(color, '08b')[plane]) * 255
                result_image.putpixel((i,ii),(color,color,color))
    return result_image

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
    x, y = range(x), range(y)
    r,g,b = 0,1,2

    try:
        if int(bit) > 7 or int(bit) < 0: bit = 0
    except ValueError: bit = 0

    if startpoint == 1: x = reversed(x)
    elif startpoint == 2: y = reversed(y)
    elif startpoint == 3: x, y = reversed(x), reversed(y)
    
    color_orders = {
        'RGB': [r ,g ,b],'RBG': [r ,b ,g],
        'BRG': [b ,r ,g],'BGR': [b ,g ,r],
        'GRB': [g ,r ,b],'GBR': [g ,b ,r]
    }

    order = color_orders[color_order]
    message = ''
    if row_order == 'True':
        for i in y:
            for ii in x:
                colors = image.getpixel((ii,i))
                f = format(colors[order[0]], '#010b')[2:][bit]
                s = format(colors[order[1]], '#010b')[2:][bit]
                t = format(colors[order[2]], '#010b')[2:][bit]
                message = message+f+s+t
    else:
        for i in x:
            for ii in y:
                colors = image.getpixel((i,ii))
                f = format(colors[order[0]], '#010b')[2:][bit]
                s = format(colors[order[1]], '#010b')[2:][bit]
                t = format(colors[order[2]], '#010b')[2:][bit]
                message = message+f+s+t
    return message

def OddEvenAnalyze(image, result_image, o=255, e=0):
    x, y = image.size
    for i in range(x):
        for ii in range(y):
            r, g, b = image.getpixel((i,j))[:2]
            if r % 2 == 0:  r = o
            else: r = e
            if g % 2 == 0:  g = o
            else: g = e
            if b % 2 == 0:  b = o
            else: b = e
            result_image.putpixel((i,ii),(r,g,b))
    return result_image

def Strings(F):
    result = ''
    for _ in F:
        _ = chr(int(_))
        if _.isascii():
            result += f'{_}'
    result = re.sub(r"\s+", "", result)
    return result

def Generate(image,sav,name):
    ### create
    x, y = image.size
    redp, greenp, bluep = [], [], []
    neg = Image.new('RGB', (x,y))
    red = Image.new('RGB', (x,y))
    green = Image.new('RGB', (x,y))
    blue = Image.new('RGB', (x,y))
    oddeven = Image.new('RGB', (x,y))
    for i in range(0,8):
        redp.append(Image.new('RGB', (x,y)))
        greenp.append(Image.new('RGB', (x,y)))
        bluep.append(Image.new('RGB', (x,y)))

    ### process
    for i in range(x):
        for ii in range(y):
            r, g, b = image.getpixel((i,ii))
            red.putpixel((i,ii),(r,0,0))
            green.putpixel((i,ii),(0,g,0))
            blue.putpixel((i,ii),(0,0,b))
            ro, go, bo = 255,255,255
            if r % 2 == 0:  ro = 0
            if g % 2 == 0:  go = 0
            if b % 2 == 0:  bo = 0
            oddeven.putpixel((i,ii),(ro,go,bo))
            for iii in range(0,8):
                rb = int(format(r, '08b')[iii]) * 255
                gb = int(format(g, '08b')[iii]) * 255
                bb = int(format(b, '08b')[iii]) * 255
                redp[iii].putpixel((i,ii),(rb,rb,rb))
                greenp[iii].putpixel((i,ii),(gb,gb,gb))
                bluep[iii].putpixel((i,ii),(bb,bb,bb))

    ### save
    Negative(image, neg).save(f'{sav}N{name}')
    red.save(f'{sav}R{name}')
    green.save(f'{sav}G{name}')
    blue.save(f'{sav}B{name}')
    oddeven.save(f'{sav}OE{name}')
    for i in range(0,8):
        redp[i].save(f'{sav}R{i}{name}')
        greenp[i].save(f'{sav}G{i}{name}')
        bluep[i].save(f'{sav}B{i}{name}')

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