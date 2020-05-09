from PIL import Image, ImageSequence
import os
import sys
import time
import numpy
import getopt
import xprintidle
import rivaloled

VENDOR_ID = 0x1038
PRODUCT_ID = 0x1700
MAXX, MAXY = 36, 128


def isanimation(im):
    try:
        im.seek(1)
    except EOFError:
        return False
    else:
        return True


def processandsend(im):
    im = im.convert('1', dither=0)
    frame = rivaloled.imagetobits(im)
    canvas = rivaloled.bitstobytes(frame)
    rivaloled.sendframe(canvas)


def main(argv):
    filename = ""
    delay = 30000
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:d:")
    except getopt.GetoptError as err:
        print("ritooled.py -i <image> -d <bool>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("ritooled.py -i <image> -d <bool")
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
            processandsend(im)
        else:
            wait = 3
            while True:
                try:
                    bd = True
                    for frame in ImageSequence.Iterator(im):
                        if xprintidle.idle_time() < delay:
                            db = True
                            processandsend(im)
                            duration = 1 / frame.info["duration"]
                            time.sleep(duration*1.5)
                        else:
                            while db:
                                rivaloled.send_blank_frame()
                                db = False
                            time.sleep(1)
                except (KeyboardInterrupt, SystemExit):
                    mouse.send_oled_frame(blank)
                    sys.exit(1)
    except IOError:
        raise Exception("File: %s is not a valid image." % filename)


if __name__ == "__main__":
    main(sys.argv[1:])
