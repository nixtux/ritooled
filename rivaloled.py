import rivalcfg
import numpy
import sys 


VENDOR_ID = 0x1038
PRODUCT_ID = 0x1700
MAXX, MAXY = 36, 128

mouse = rivalcfg.get_mouse(VENDOR_ID, PRODUCT_ID)
blankframe = numpy.zeros((576, MAXY), dtype=int, order='C')


def imagetobits(im):
    frame = numpy.asarray(im, dtype=int)
    return frame


def bitstobytes(array):
    array = numpy.packbits(array,axis=-1)
    array = array.flatten("A")
    return array


def sendframe(frame):
    mouse.send_oled_frame(frame)


def sendblankframe(frame):
    mouse.send_oled_frame(blankframe)


def main(frame):
    if len(frame) != 4608:
        raise ValueError("Please provide 4608 bytes data.")


if __name__ == '__main__':
    main(sys.argv[1:])