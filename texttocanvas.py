from __future__ import print_function
import string
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys
import numpy
import rivaloled
import time

MAXX, MAXY = 36, 128
timeout = 60000

def char_to_pixels(text, path, fontsize):
    """
    Based on https://stackoverflow.com/a/27753869/190597 (jsheperd)
    """
    font = ImageFont.truetype(path, fontsize) 
    w, h = font.getsize(text)  
    h *= 2
    image = Image.new('L', (w, h), 1)  
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font) 
    arr = numpy.asarray(image)
    arr = numpy.where(arr, 0, 1)
    arr = arr[(arr != 0).any(axis=1)]
    return arr


def imagetoarray(filename):
    filename="cpu.png"
    im = Image.open(filename, "r")
    array = rivaloled.imagetobits(im)
    return array
    

def stitcharray(a, b, axis):
    return numpy.concatenate((a, b), axis=axis, out=None)


def padarray(arr, xsize, ysize):
    x, y = arr.shape
    print("grow array", x, y, xsize, ysize)
    ypadt = 0
    ypadb = 0
    xpadt = 0
    xpadb = 0
    if y < ysize:
        ypad = (ysize-y)/2
        print("y, ysize ",y, ysize)

        if (ypad % 2) == 0:
            ypadt = int(ypad)
            ypadb = int(ypad)
        else:
            ypadt = int(ypad + 1)
            ypadb = int(ypad - 0.5)
    if x < xsize:
        print("x, xsize ",x, xsize)
        xpad = (xsize-x)/2
        if (xpad % 2) == 0:
            xpadt = int(xpad)
            xpadb = int(xpad)
        else:
            xpadt = int(xpad + 1)
            xpadb = int(xpad - 0.5)
    print(xpadt, xpadb, ypadt, ypadb)
    arr = numpy.pad(arr, ((xpadt, xpadb) , (ypadt, ypadb)), mode = 'constant', constant_values=(0, 0))
    return arr


def texttoarray(argv, fontsize):
    print("argv", argv)
    for c in argv:
        arr = char_to_pixels(
            c, 
            #path='/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf', 
            #path='/home/nixtux/.local/share/fonts/adip1.ttf', 
            path='/home/nixtux/.local/share/fonts/YummyCupcakes.ttf', 
            fontsize=fontsize)
    return arr


def showmessage(array):
    x, y = array.shape
    print(array.shape)
    if y == 128:
        rivaloled.sendframe(array, timeout)
    else:
        seq = []
        position = 1
        flip = 1
        x, y = array.shape
        l = y * 2
        for index in range(l):
            frame = array[0:, position:position+MAXY]
            seq.append(frame)
            position = position + flip
            if position == y-MAXY:
                flip = -1
            if position == 1:
                flip = 1
        frames = numpy.dstack(seq)
        rivaloled.sendsquenece(frames, timeout)


def texttooled(text, fontsize):
    message = texttoarray(text, fontsize)
    x, y = message.shape
    if y > 128:
        message = padarray(message, 36, y)
    else:
        message = padarray(message, 36, 128)
    showmessage(message)



def main(argv):
    icon = imagetoarray("hdehe")
    x, y = icon.shape
    icon = padarray(icon, 36, y)
    message = texttoarray(argv, 38)
    x, y = message.shape
    message = padarray(message, 36, y)
    x, y = message.shape
    message = stitcharray(icon, message, 1)
    x, y = message.shape
    x, y = message.shape
    if y > 128:
        message = padarray(message, 36, y)
    else:
        message = padarray(message, 36, 128)
    x, y = message.shape
    showmessage(message)

    

if __name__ == "__main__":
    main(sys.argv[1:])