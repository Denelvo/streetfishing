import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from google.cloud import storage

app=Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'tiff', 'eps', 'raw'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/') # First visit, show form
def upload_form():
    return render_template('mupload.html')

@app.route('/', methods=['POST'])   # Pics being uploaded
def upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('Geen foto\'s geselecteerd. Toch niet geblankt? ')
            return redirect(request.url)

        client = storage.Client()
        files = request.files.getlist('files[]')
        num = len(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                localfilename = os.path.join(app.config['UPLOAD_FOLDER'], request.form.get('team_number') + '_' + request.form.get('team_name') + '_' + filename)
                file.save(localfilename)

                bucket = client.get_bucket('streetfishing.appspot.com')
                blob2 = bucket.blob(request.form.get('team_number') + '_' + request.form.get('team_name') + '/' + filename)
                blob2.upload_from_filename(filename=localfilename)
                blob2.make_public()
                blobfilename = blob2.public_url
                os.remove(localfilename)
                #flash('URL: '+blobfilename)

        flash(str(num) + ' foto\'s zijn opgeladen! Bedankt ' + request.form.get('team_name') + '.')
        return redirect('/')

@app.route('/gallery') # Results: pic gallery
def display_gallery():
    urls=[]
    client = storage.Client()
    bucket = client.get_bucket('streetfishing.appspot.com')
    blobs = list(client.list_blobs(bucket))
    for blob in client.list_blobs('streetfishing.appspot.com'):
        st = str(blob)
        st = st.split(',')[1].strip()
        url = 'https://storage.googleapis.com/streetfishing.appspot.com/' + st
        urls.append(url)
    urls.sort()

    return render_template('gallery.html', urls = urls)


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=False,threaded=True)