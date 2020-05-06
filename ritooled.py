from PIL import Image, ImageSequence
import os
import sys
import time
import getopt
import rivalcfg
import xprintidle

VENDOR_ID = 0x1038
PRODUCT_ID = 0x1700
mouse = rivalcfg.get_mouse(VENDOR_ID, PRODUCT_ID)
MAXX, MAXY = 36, 128


blank = []
for e in range(576):
    blank.append(0x00)


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
    im = im.convert('1', dither=0)
    array = processpixelcolor(x, y, im)
    array = converttoinit(stringsplit(array, 8))
    return array


def main(argv):
    filename = ""
    delay = 30000
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:d:")
    except getopt.GetoptError as err:
        print("riloader.py -i <image> -d <bool>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("riloader.py -i <image> -d <bool")
            sys.exit()
        elif opt in "-i":
            filename = arg
        elif opt in "-d":
            d = int(arg)
            if d >= 1500 and d <= 600000:
                delay = int(arg)
            else:
                print("delay must be greater than 1500 and less than 600000")
    if not os.path.exists(filename):
        raise Exception("File: %s does not exist." % filename)
    try:
        im = Image.open(filename, "r")
        y, x = im.size
        imf = im.format
        if imf != "GIF":
            raise Exception("File: %s needs to be in gif format." % filename)
        if y > MAXY or x > MAXX:
            raise Exception("Image must be 128x36 pixel")
        if not isanimation(im):
            array = processframe(x, y, im)
            mouse.send_oled_frame(array)
        else:
            while True:
                try:
                    for frame in ImageSequence.Iterator(im):
                        if xprintidle.idle_time() < delay:
                            array = processframe(x, y, frame)
                            mouse.send_oled_frame(array)
                            duration = 1 / frame.info["duration"]
                            #print(duration,xprintidle.idle_time())
                            time.sleep(duration)
                        else:
                            #print(time.time(), xprintidle.idle_time())
                            mouse.send_oled_frame(blank)
                            break
                except (KeyboardInterrupt, SystemExit):
                    mouse.send_oled_frame(blank)
                    sys.exit(1)
    except IOError:
        raise Exception("File: %s is not a valid image." % filename)


if __name__ == "__main__":
    main(sys.argv[1:])
