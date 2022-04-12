import main as STEG
from PIL import Image, GifImagePlugin
from flask import Flask, request, flash, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER       =   f'{os.path.dirname(os.path.realpath(__file__))}/static/images/'
ALLOWED_EXTENSIONS  =   set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def log(arg = None):
    print(f'🚀🚀🚀\n{arg}\n🚀🚀🚀')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['POST','GET'])
@app.route('/index', methods = ['POST','GET'])
def index(filename = None):
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            imagepath = f'{UPLOAD_FOLDER}{filename}'
            file.save(imagepath)
            image = Image.open(imagepath)
            nframes = STEG.GetNFrames(image)
            if nframes > 0:
                for i in range(0,nframes):
                    image.seek(i)
                    image.save(f'{UPLOAD_FOLDER}frame{i}{filename}')
            return redirect(url_for('info', image = imagepath.split('/')[-1],))
    return render_template("upload.html")

@app.route('/index/info', methods = ['POST','GET'])
def info(i = 0):
    path = request.args['image']
    image = Image.open(f'{UPLOAD_FOLDER}{path}')
    nframes = STEG.GetNFrames(image)
    ExifList = STEG.GetExif(image)
    if request.method == 'POST':
        if 'FRAME' not in request.form:
            return redirect(request.url)
        i = request.form['FRAME']
        if i == '':
            return redirect(request.url)
        if int(i) > nframes-1 or int(i) < 0: i = '0'
        try:
            if request.form['switch'] == 'continue':
                frameimage = f'frame{i}{path}'
                return redirect(url_for('switch', image = frameimage))
        except:
            log(request.form)
    frameimage = f'frame{i}{path}'
    return render_template("info.html", img = f'/../static/images/{frameimage}', Exif = ExifList, Frames = nframes-1, Frame = i, path=path)

@app.route('/index/check', methods = ['POST','GET'])
def switch():
    path = request.args['image']
    RenderImage = f'/../static/images/{path}'
    if request.method == 'POST':
        image = Image.open(f'{UPLOAD_FOLDER}{path}')
        image = STEG.Convert(image)
        if 'method' not in request.form:
            return redirect(request.url)
        NewImage = Image.new(image.mode, image.size, color='white')
        case = request.form['method']
        # Nice code
        if case == 'Negative':
            ResultImage = STEG.Negative(image,NewImage)
            ResultImage.save(f'{UPLOAD_FOLDER}{case}{path}')
            RenderImage = f'/../static/images/{case}{path}'
        elif case == 'OnlyRed':
            ResultImage = STEG.OnlyRed(image,NewImage)
            ResultImage.save(f'{UPLOAD_FOLDER}{case}{path}')
            RenderImage = f'/../static/images/{case}{path}'
        elif case == 'OnlyGreen':
            ResultImage = STEG.OnlyGreen(image,NewImage)
            ResultImage.save(f'{UPLOAD_FOLDER}{case}{path}')
            RenderImage = f'/../static/images/{case}{path}'
        elif case == 'OnlyBlue':
            ResultImage = STEG.OnlyBlue(image,NewImage)
            ResultImage.save(f'{UPLOAD_FOLDER}{case}{path}')
            RenderImage = f'/../static/images/{case}{path}'
        else:
            bit = int(request.form['bit'])
            if case == 'RedBitPlane':
                ResultImage = STEG.RedBitPlane(image,NewImage,bit)
                ResultImage.save(f'{UPLOAD_FOLDER}{case}{bit}{path}')
                RenderImage = f'/../static/images/{case}{bit}{path}'
            elif case == 'GreenBitPlane':
                ResultImage = STEG.GreenBitPlane(image,NewImage,bit)
                ResultImage.save(f'{UPLOAD_FOLDER}{case}{bit}{path}')
                RenderImage = f'/../static/images/{case}{bit}{path}'
            elif case == 'BlueBitPlane':
                ResultImage = STEG.BlueBitPlane(image,NewImage,bit)
                ResultImage.save(f'{UPLOAD_FOLDER}{case}{bit}{path}')
                RenderImage = f'/../static/images/{case}{bit}{path}'
            elif case == 'AlphaBitPlane':
                ResultImage = STEG.AlphaBitPlane(image,NewImage,bit)
                ResultImage.save(f'{UPLOAD_FOLDER}{case}{bit}{path}')
                RenderImage = f'/../static/images/{case}{bit}{path}'
            elif case == 'SignificantBit':
                color = request.form['color']
                startpoint = request.form['startpoint']
                row_order = request.form['row_order']
                f = open("static/result.txt", "w")
                log('SignificantBit')
                message = STEG.SignificantBit(image,color,row_order,startpoint,bit)
                f.write(message)
                log('END')
                f.close()
    return render_template("switch.html", img = RenderImage)

if __name__ == '__main__': ## https://redirect.is/hztkea9
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()