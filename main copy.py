import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask import send_from_directory
from werkzeug.utils import secure_filename
from logic import find_text
from googletrans import Translator

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])

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
    
if __name__ == "__main__":
	app.run(debug=True)