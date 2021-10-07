from flask import Flask, render_template, request
from os import path
app = Flask(__name__)

@app.route('/multiupload', methods=['GET','POST'])
def upload():
    if request.method == "POST":
        files = request.files.getlist("file")
        for file in files:
            file.save(path.join(app.config['UPLOAD_FOLDER'], file.filename))


@app.route('/upload')
def screen_upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save("uploads/" + f.filename)
        return 'file uploaded successfully'

if __name__ == '__main__':
    app.run(debug = True)