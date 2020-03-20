import os
from flask import url_for # DO WE NEED THIS?
from flask import Flask, render_template, request, redirect, send_file
from s3_operations import upload_file, download_file
from werkzeug.utils import secure_filename


app = Flask(__name__)

UPLOAD_FOLDER = '/Users/kevin/Desktop/New Classes/Cloud Computing/image_flask_app/uploads/'
BUCKET = 'project1testbucket'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"uploads/{f.filename}", BUCKET)

        return redirect("/storage")

@app.route("/storage")
def storage():
    contents = []# TODO
    return render_template("upload.html", contents=contents)

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
