import xprintidle
import threading
import rivalcfg
import numpy
import time
import sys


# Set config for Rival 700
VENDOR_ID = 0x1038
PRODUCT_ID = 0x1700
mouse = rivalcfg.get_mouse(VENDOR_ID, PRODUCT_ID)

# Set Old Screen Dims
MAXX, MAXY = 36, 128
blankframe = numpy.zeros((MAXX, MAXY), dtype=int, order='C')
oldframes = numpy.zeros((MAXX, MAXY, 2), dtype=int, order='C')
oldframe = []
screendisabled = False
timeout = 200000
shuttingdown = False


def screensaver(delay):
    global screendisabled, timeout, shuttingdown, oldframe
    timeout = delay
    while True:
        if xprintidle.idle_time() < timeout:
            if screendisabled:
                screendisabled = False
                mouse.send_oled_frame(oldframe)
            screendisabled = False
        else:
            sendblankframe(timeout)
            screendisabled = True
        if shuttingdown:
            break
        time.sleep(2)


# Start screensaver thread
screensaver = threading.Thread(target=screensaver, args=(timeout,))
screensaver.start()


# convert pil image to a binary numpy array
def imagetobits(im):
    frame = numpy.asarray(im, dtype=int)
    return frame


# flatten array before sending to rivalcfg
def _bitstobytes_(array):
    array = numpy.packbits(array, axis=-1)
    array = array.flatten("A")
    return array


# sendframe(numpy array of (36x128), delay for screensaver in milliseconds)
def sendframe(frame, delay):
    global oldframe, timeout
    timeout = delay
    if not numpy.array_equal(frame, oldframe):
        if not screendisabled:
            frame = _bitstobytes_(frame)
            mouse.send_oled_frame(frame)
            if not numpy.array_equal(frame, _bitstobytes_(blankframe)):
                oldframe = frame


# sendsquenece(numpy array (36x128, frames in squenece), delay for screensaver in milliseconds)
def sendsquenece(frames, delay):
    global oldframes, timeout, shuttingdown
    while not numpy.array_equal(frames, oldframes):
        depth = frames.shape[2]
        for d in range(depth):
            try:
                frame = frames[:, :, d]
                sendframe(frame, delay)
                time.sleep(.1)  # 1th sec ergo 10 fps
            except (KeyboardInterrupt, SystemExit):
                print(" ---- Ctrl+c Detected Closing Down Please Wait.")
                shuttingdown = True
                sendblankframe(delay)
                sys.exit(1)


# sendblankframe(delay for screensaver in milliseconds)
def sendblankframe(delay):
    global timeout
    sendframe(blankframe, timeout)


def main(frame):
    pass
