from __future__ import print_function
import string
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys
import numpy as np
import rivalcfg
import time

VENDOR_ID = 0x1038
PRODUCT_ID = 0x1700
mouse = rivalcfg.get_mouse(VENDOR_ID, PRODUCT_ID)
MAXX, MAXY = 36, 128


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
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    arr = arr[(arr != 0).any(axis=1)]
    return arr


def displaytty(arr):
    result = np.where(arr, '#', ' ')
    print('\n'.join([''.join(row) for row in result]))


def bitstobytes(array):
    array = np.packbits(array,axis=-1)
    array = array.flatten("A")
    return array


def growarray(arr):
    x, y = arr.shape
    ypadt = 0
    ypadb = 0
    xpadt = 0
    xpadb = 0
    if y <= 128:
        ypad = (MAXY-y)/2
        if (ypad % 2) == 0:
            ypadt = int(ypad)
            ypadb = int(ypad)
        else:
            ypadt = int(ypad + 1)
            ypadb = int(ypad - 0.5)    
    if x <= 36:
        xpad = (MAXX-x)/2
        if (xpad % 2) == 0:
            xpadt = int(xpad)
            xpadb = int(xpad)
        else:
            xpadt = int(xpad + 1)
            xpadb = int(xpad - 0.5)
    arr = np.pad(arr, ((xpadt, xpadb) , (ypadt, ypadb)), mode = 'constant', constant_values=(0, 0))
    #todo just copy array into the size i need
    return arr


def main(argv):
    for c in argv:
        arr = char_to_pixels(
            c, 
            path='/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf', 
            fontsize=MAXX)
        #displaytty(arr)
        message = growarray(arr)
        x, y = message.shape
        if y == 128:
            frame=bitstobytes(message)
            mouse.send_oled_frame(frame)
        else: 
            position = 1
            flip = 1
            while True:
                x, y = message.shape
                frame = message[0:, position:position+MAXY]
                frame=bitstobytes(frame)
                mouse.send_oled_frame(frame)
                position = position + flip
                if position == y-MAXY:
                    flip = -1
                if position == 1:
                    flip = 1
                time.sleep(.05)

if __name__ == "__main__":
    main(sys.argv[1:])