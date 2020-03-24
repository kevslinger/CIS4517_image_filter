import os
from flask import url_for, flash # DO WE NEED THIS?
from flask import Flask, render_template, request, redirect, send_file, send_from_directory
import s3_operations
import image_processing
from werkzeug.utils import secure_filename
import constants


app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = constants.UPLOAD_FOLDER
app.config['BASE_FOLDER'] = constants.BASE_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in constants.ALLOWED_EXTENSIONS

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/landing")
def landing():
    #contents = []# TODO contents = list_files(constants.BUCKET)
    contents = local_list_files() # TODO: NOT NEEDED FOR REMOTE
    return render_template("landing.html", contents=contents)

@app.route("/filter/<filename>")
def render_filter(filename):
    return render_template("image_filtering.html", filename=filename)
                           #filename='http://127.0.0.1:5000/uploads/' + filename)

@app.route("/filter/<filename>/sepia", methods=['POST'])
def apply_sepia(filename):
    outputfilename = image_processing.applyfilter(filename, 'blur')
    return render_template("image_filtering_child.html", filename=filename,
                               outputfilename=outputfilename)
@app.route("/filter/<filename>/blur", methods=['POST'])
def apply_blur(filename):
    outputfilename = image_processing.applyfilter(filename, 'blur')
    return render_template("image_filtering_child.html", filename=filename,
                               outputfilename=outputfilename)
@app.route("/filter/<filename>/poster", methods=['POST'])
def apply_poster(filename):
    outputfilename = image_processing.applyfilter(filename, 'poster')
    return render_template("image_filtering_child.html", filename=filename,
                               outputfilename=outputfilename)

@app.route("/download_local/<filename>", methods=['GET'])
def send_file_to_kev(filename):
    return send_from_directory(os.path.join(app.config['BASE_FOLDER'], app.config['UPLOAD_FOLDER']), filename)
    
# TODO: NOT NEEDED FOR REMOTE
import glob
def local_list_files():
    file_list = []
    for filename in glob.glob('/Users/kevin/Desktop/New Classes/Cloud Computing/image_flask_app/uploads/*.jpg'):
        file_list.append({'key' : filename})
    return file_list
# END TODO

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = s3_operations.download_file(filename, constants.BUCKET)

        return send_file(output, as_attachment=True)

@app.route("/upload_s3", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(app.config['BASE_FOLDER'], app.config['UPLOAD_FOLDER'], f.filename))
        s3_operations.upload_file(f"uploads/{f.filename}", BUCKET)

        return redirect("/landing")
    
@app.route('/upload_local', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['BASE_FOLDER'], app.config['UPLOAD_FOLDER'], filename))
            return redirect("/filter/" + filename)
            #return redirect(url_for('/filter/' + filename,
                                    #filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

    
if __name__ == '__main__':
    app.run(debug=True)
