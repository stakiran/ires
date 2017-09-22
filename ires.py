# -*- coding: utf-8 -*-

import os

from PIL import Image
from PIL import ImageFile

def p(msg):
    print msg

def abort(msg):
    p('Error: {:}'.format(msg))
    exit(1)

def get_directory(path):
    return os.path.dirname(path)

def get_filename(path):
    return os.path.basename(path)

def get_basename(path):
    return os.path.splitext(get_filename(path))[0]

def get_extension(path):
    return os.path.splitext(get_filename(path))[1]

def calc_new_size(size_int, resize_rate_int):
    return int(size_int*(resize_rate_int/100.0))

def save_to_png(imageinst, filename):
    imageinst.save(filename)

def save_to_jpg(imageinst, filename):
    # バッファが小さくて
    # IOError: encoder error -2 when writing image file
    # が起きるので, テキトーにでかいバッファサイズを設定しとく.
    # from: https://stackoverflow.com/questions/6788398/how-to-save-progressive-jpeg-using-python-pil-1-1-7
    #
    # [以下調べてない]
    # - 単に最大 w, h の乗算でいい? それともさらに n 倍が必要?
    ImageFile.MAXBLOCK = max_width*max_height

    imageinst.save(filename, 'JPEG',
        quality=100,
        optimize=True,
        progressive=True
    )

def save_judgeman(imageinst, infilepath, resize_rate):
    directory = get_directory(infilepath)
    base = get_basename(infilepath).lower()
    ext  = get_extension(infilepath).lower()
    outfilename = '{:}_{:}{:}'.format(base, resize_rate, ext)
    outfilepath = os.path.join(directory, outfilename)

    if ext=='.png':
        save_to_png(imageinst, outfilepath)
    elif ext=='.jpg' or ext=='.jpeg':
        save_to_jpg(imageinst, outfilepath)
    else:
        abort('Not supported format: {:}'.format(ext))

def resize_a_image(infilepath, resize_rate):
    img = Image.open(infilepath, 'r')
    w, h = img.size
    rate = resize_rate
    new_w, new_h = calc_new_size(w, rate), calc_new_size(h, rate)
    new_size = (new_w, new_h)
    resized_img = img.resize(new_size)
    save_judgeman(resized_img, infilepath, rate)

def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-r', '--rate', default=100, required=True, type=int,
        help='resize Rate[%%].')
    parser.add_argument('infiles', nargs='*',
        help='target image files. MUST BE FILENAME, NOT FULLPATH.')

    parser.add_argument('--max-width', default=4096, type=int,
        help='Max buffer width size for jpeg.')
    parser.add_argument('--max-height', default=4096, type=int,
        help='Max buffer height size for jpeg.')

    args = parser.parse_args()
    return args

selfdir = os.path.abspath(os.path.dirname(__file__))

args = parse_arguments()

resize_rate = args.rate
max_width   = args.max_width
max_height  = args.max_height
infiles     = [os.path.join(selfdir,infilename) for infilename in args.infiles]

if len(infiles)==0:
    abort('No filename given.')

for i,infilepath in enumerate(infiles):
    p('{:}/{:} {:}...'.format(i+1, len(infiles), get_filename(infilepath)))
    resize_a_image(infilepath, resize_rate)
