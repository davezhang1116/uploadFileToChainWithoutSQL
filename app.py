from flask import Flask, render_template,flash, url_for, request, redirect, session, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
import hashlib, os, io
from werkzeug.utils import secure_filename
from send import upload_file, download_file
import web3


app = Flask(__name__)

UPLOAD_FOLDER = './files'

@app.route('/', methods=['GET', 'POST'])
def index():
    base_html = '''
    <!doctype html>
    <title>Upload new files that is less than 10MB </title>
    <h1>Upload a file</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
    if request.method == 'POST':
        for i in os.listdir("./process"):
            os.remove("./process/"+i)
        for i in os.listdir("./downloaded_files"):
            os.remove("./downloaded_files/"+i)
        for i in os.listdir("./files"):
            os.remove("./files/"+i)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            hash = upload_file(filename)
            return """<h2> Your download hash is {}</h2>
            <p><a href="/download/{}">download link</a></p>
            """.format(hash,hash)
    return base_html
@app.route('/download/<hash>')
def download(hash):

    filename = download_file(hash)

    file_path = "./downloaded_files/"+ filename
    return_data = io.BytesIO()
    with open(file_path, 'rb') as fo:
        return_data.write(fo.read())
    return_data.seek(0)
    os.remove(file_path)
    return send_file(return_data, attachment_filename=filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
