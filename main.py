import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask import send_from_directory
from werkzeug.utils import secure_filename
from logic import find_text
from googletrans import Translator
import os
from flask import Flask, render_template, send_from_directory, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import cv2
import easyocr
import PIL
from PIL import Image
import numpy as np

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['SECRET_KEY'] = 'ccdcdccdcd'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads/'


translator = Translator()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def Home():
    return render_template('Home.html')

@app.route('/Extract_Text')
def index():
    return render_template('Text_Extr.html')

@app.route('/Extract_Text', methods=['GET','POST'])
def upload():
    uploaded_files = request.files.getlist("file[]")
    if not any(f for f in uploaded_files):
      return redirect(url_for('index'))
    file_details = []
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            text = find_text(filepath)
            file_details.append([filename, text])

    return render_template('Text_Extr.html', files=file_details)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/SpeechREC', methods=['GET','POST'])
def speech():
    return render_template('speech.html')

@app.route("/Translate", methods=['POST', 'GET'])
def Text_Translator():
    if request.method == 'POST':
        try:
            text_to_translate = request.form["text-to-translate"].lower()
            selected_language = request.form["select-language"]
            translated_text = translator.translate(
                text_to_translate, dest=selected_language)
            text = translated_text.text
            
        except:
            text = "{ERROR: We are not able to handle your request right now}"
        return render_template('Translate.html', translation_result=text)
    return render_template("Translate.html")


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

class UploadForm(FlaskForm):
    photo = FileField(
        validators = [
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('Upload')

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/Detect', methods = ['GET', 'POST'])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        file_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], 'image.jpg')
        if os.path.exists(file_path):
            os.remove(file_path)
        filename = photos.save(form.photo.data, name='image.jpg')
        print(filename)
        
        file_url = url_for('get_file', filename=filename)
        
        
        image = cv2.imread("static/uploads/" + str(filename))
        #print(image)
        cv2.imwrite("static/uploads/images.jpg",image)
        images = cv2.imread("static/uploads/images.jpg")
        if (image is not None):
            grey = cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)

            reader = easyocr.Reader(['en'])
            result = reader.readtext(grey)
            font = cv2.FONT_HERSHEY_SIMPLEX


            for detection in result:
                
                top_left = tuple(detection[0][0])
                bottom_right = tuple(detection[0][2])
                text = detection[1]
                images = cv2.rectangle(images, top_left, bottom_right, (0, 255, 0), 3)
                images = cv2.putText(images, text, top_left, font, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
            
              



            config_file = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
            frozen_model = 'frozen_inference_graph.pb'
            model = cv2.dnn_DetectionModel(frozen_model,config_file)

            model.setInputSize(320,320)
            model.setInputScale(1.0/127.5)
            model.setInputMean((127.5,127.5,127.5))
            model.setInputSwapRB(True)

            classLabels = []
            file_name = 'Labels.txt'
            with open(file_name,'rt') as fpt:
                classLabels = fpt.read().rstrip('\n').split('\n')
            #print(classLabels)
            
            ClassIndex, confidece, bbox = model.detect(images,confThreshold=0.5)
            font_scale = 2
            
            ClassIndex = np.array(ClassIndex)
            confidece = np.array(confidece)
            bbox = np.array(bbox)
            
            for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidece.flatten(), bbox):
                cv2.rectangle(images,boxes,(255,0,0),2)
                cv2.putText(images,classLabels[ClassInd-1],(boxes[0]+10,boxes[1]+40),font,fontScale=font_scale,color =(0,255,0),thickness=3)
            
            # image = Image.fromarray(images, 'RGB')
            cv2.imwrite("static/uploads/detect.jpg",images)
            
            detext=find_text(file_path)
            print("detext: ", detext)

        else:
            print('Wrong')
            
        detect_file_url = url_for('get_file', filename='detect.jpg')
    else:
        file_url = None
        detect_file_url = None
        detext = None
        
    return render_template('Detect.html', form=form, file_url = file_url, detext=detext, detect_file_url = detect_file_url)







    
if __name__ == "__main__":
	app.run(debug=True)