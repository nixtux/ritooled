from PIL import Image, ImageSequence
import sys
import os
import time
import rivalcfg

filename = sys.argv[1]
mouse = rivalcfg.get_first_mouse()
MAXX, MAXY = 36, 128


def isanimation(im):
    try:
        im.seek(1)
    except EOFError:
        return False
    else:
        return True


def stringsplit(string, length):
    split_strings = []
    for index in range(0, len(string), length):
        split_strings.append(string[index : index + length])
    return split_strings


def converttoinit(table):
    output = []
    for l in range(len(table)):
        output.append(int(table[l], 2))
    return output


def processpixelcolor(x, y, im):
    index = 1
    array = ""
    for px in range(x):
        for py in range(y):
            pxl = im.getpixel((py, px))
            if pxl == 255:
                pxl = "1"
            else:
                pxl = "0"
            array = array + pxl
            index = index + 1
    return array


def processframe(x, y, im):
    array = processpixelcolor(x, y, im)
    array = converttoinit(stringsplit(array, 8))
    return array


def main():
    if not os.path.exists(filename):
        raise Exception("File: %s does not exist." % filename)
    im = Image.open(filename, "r")
    y, x = im.size
    imf = im.format
    if imf != "GIF":
        raise Exception("File: %s needs to be in gif format." % filename)
    if y > MAXY or x > MAXX:
        raise Exception("Image must be 128x36 pixel")
    if not isanimation(im):
        im = im.convert('1', dither=1)
        array = processframe(x, y, im)
        mouse.set_oled_image(array)
    else:
        while True:
            for frame in ImageSequence.Iterator(im):
                frame = frame.convert('1', dither=1)
                array = processframe(x, y, frame)
                mouse.set_oled_image(array)
                duration = 1 / frame.info['duration']
                #print (duration)
                time.sleep(duration)


if __name__ == "__main__":
    main()