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
    return render_template("landing.html", contents=contents)

#######################
### Upload Page #######
#######################

# Upload to S3
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
@app.route("/filter/<filename>/<preset>", methods=['POST'])
def apply_preset(filename, preset):
    outputfilename = image_processing.applyfilter(filename, preset)
    return render_template("image_filtering_child.html", filepath=filename,
                                 outputfilename=outputfilename)

##########################
### Download Page ########
##########################

# Download from S3
@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = s3_operations.dow*nload_file(filename, constants.BUCKET)

        return send_file(output, as_attachment=True)



    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
