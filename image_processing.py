from PIL import Image, ImageOps,ImageFilter
import constants
import s3_operations


def applyfilter(path, preset):
    f = path.split('.')
    outputfilename = f[0] + '-out-' + preset + '.' + f[1]
    
    im = Image.open(constants.UPLOAD_FOLDER + path)
    if preset == 'gray':
        im = ImageOps.gray

    if preset == 'edge':
        im = ImageOps.grayscale(im)
        im = im.filter(ImageFilter.FIND_EDGES)

    if preset == 'poster':
        im = ImageOps.posterize(im, 3)

    if preset == 'solar':
        im = ImageOps.solarize(im, threshold=80)

    if preset == 'blur':
        im = im.filter(ImageFilter.BLUR)
        
    if preset == 'sepia':
        sepia = []
        r, g, b = (239, 224, 185)
        for i in range(255):
            sepia.extend((r*i/255, g*i/255, b*i/255))
        im = im.convert("L")
        im.putpalette(sepia)
        im = im.convert("RGB")

    im.save(constants.UPLOAD_FOLDER + outputfilename)
    s3_operations.upload_file(outpufilename, constants.BUCKET)
    return outputfilename
