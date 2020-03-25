BASE_FOLDER = '/home/ubuntu/CIS4517_image_filter'
#BASE_FOLDER = '/Users/kevin/Desktop/New Classes/Cloud Computing/image_flask_app'
UPLOAD_FOLDER = 'static/'
DOWNLOAD_FOLDER = 'downloads/'
BUCKET = 'project1testbucket'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# TODO: NOT NEEDED FOR REMOTE
import glob
def local_list_files():
    file_list = []
    for filename in glob.glob('/Users/kevin/Desktop/New Classes/Cloud Computing/image_flask_app/uploads/*.jpg'):
        file_list.append({'Key' : filename})
    return file_list
# END TODO
