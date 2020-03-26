from PIL import Image, ImageOps,ImageFilter
import constants
import s3_operations


def applyfilter(path, preset):
    f = path.split('.')
    outputfilename = f[0] + '-out-' + preset + '.' + f[1]
    
    im = Image.open(constants.UPLOAD_FOLDER + path)
    if preset == 'gray':
        im = ImageOps.grayscale(im)

    if preset == 'edge':
        im = ImageOps.grayscale(im)
        im = im.filter(ImageFilter.FIND_EDGES)

    if preset == 'poster':
        im = ImageOps.posterize(im, 3)

    if preset == 'solar':
        im = ImageOps.solarize(im, threshold=80)

    if preset == 'blur':
        im = im.filter(ImageFilter.BLUR)

    im.save(constants.UPLOAD_FOLDER + outputfilename)
    #s3_operations.upload_file(outputfilename, constants.BUCKET)
    return outputfilename
