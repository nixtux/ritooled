import xprintidle
import rivalcfg
import numpy
import time
import sys 


#Set config for Rival 700
VENDOR_ID = 0x1038
PRODUCT_ID = 0x1700
mouse = rivalcfg.get_mouse(VENDOR_ID, PRODUCT_ID)

#Set Old Screen Dims
MAXX, MAXY = 36, 128
blankframe = numpy.zeros((MAXX, MAXY), dtype=int, order='C')
oldframes = numpy.zeros((MAXX, MAXY, 2), dtype=int, order='C')
oldframe = blankframe


def imagetobits(im):
    #convert pil image to numpy array
    frame = numpy.asarray(im, dtype=int)
    return frame


def _bitstobytes_(array):
    #flatten array befire sending to rivalcfg
    array = numpy.packbits(array,axis=-1)
    array = array.flatten("A")
    return array


def sendframe(frame):
    global oldframe
    if not numpy.array_equal(frame, oldframe):
        frame = _bitstobytes_(frame)
        mouse.send_oled_frame(frame)
        oldframe = frame


def sendsquenece(frames, delay):
    global oldframes
    while not numpy.array_equal(frames, oldframes):
        depth = frames.shape[2]
        for d in range(depth):
            if xprintidle.idle_time() < delay:
                frame = frames[:,:,d]
                sendframe(frame)
            else:
                sendblankframe()
            time.sleep(.1) #10 fps


def sendblankframe():
    sendframe(blankframe)


def main(frame):
    if len(frame) != 4608:
        raise ValueError("Please provide 4608 bytes data.")


if __name__ == '__main__':
    main(sys.argv[1:])