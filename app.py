import os
from flask import url_for, flash
from flask import Flask, render_template, request, redirect, send_file, send_from_directory
import s3_operations
import image_processing
from werkzeug.utils import secure_filename
import constants


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = constants.UPLOAD_FOLDER
app.config['BASE_FOLDER'] = constants.BASE_FOLDER

####################
### Landing Page ###
####################

@app.route("/")
def route_to_landing():
    return redirect("/landing")
@app.route("/landing")
def landing():
    contents = s3_operations.list_files(constants.BUCKET)
    #contents = local_list_files() # TODO: NOT NEEDED FOR REMOTE
    return render_template("landing.html", contents=contents)

#######################
### Upload Page #######
#######################

# Upload to S3 (for remote use only)
@app.route("/upload_s3", methods=['POST'])
def upload():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)
        f.save(os.path.join(app.config['BASE_FOLDER'], app.config['UPLOAD_FOLDER'], f.filename))
        s3_operations.upload_file(f"{f.filename}", constants.BUCKET)

        return redirect("/filter/" + f.filename)

# Upload to local (not for remote)
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
        if file and constants.allowed_file(file.filename):
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

#################################
#### Image Filtering Pages ######
#################################

# Get taken to this page once the user submits
# an image upload request
@app.route("/filter/<filename>")
def render_filter(filename):
    return render_template("image_filtering.html", filepath=filename)

# apply_<preset> are the endpoints after the filter
# has been processed.
@app.route("/filter/<filename>/sepia", methods=['POST'])
def apply_sepia(filename):
    outputfilename = image_processing.applyfilter(filename, 'blur')
    return render_template("image_filtering_child.html", filepath=filename,
                               outputfilename=outputfilename)
@app.route("/filter/<filename>/blur", methods=['POST'])
def apply_blur(filename):
    outputfilename = image_processing.applyfilter(filename, 'blur')
    return render_template("image_filtering_child.html", filepath=filename,
                               outputfilename=outputfilename)
@app.route("/filter/<filename>/poster", methods=['POST'])
def apply_poster(filename):
    outputfilename = image_processing.applyfilter(filename, 'poster')
    return render_template("image_filtering_child.html", filepath=filename,
                               outputfilename=outputfilename)

##########################
### Download Pages #######
##########################

# I... forget exactly how this function is being used but i'll figure it out.
@app.route("/download_local/<filename>", methods=['GET'])
def send_file_to_kev(filename):
    return send_from_directory(os.path.join(app.config['BASE_FOLDER'], app.config['UPLOAD_FOLDER']), filename)
    
@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = s3_operations.download_file(filename, constants.BUCKET)

        return send_file(output, as_attachment=True)



    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
