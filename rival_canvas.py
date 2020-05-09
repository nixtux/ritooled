import rivaloled
import numpy
import time

MAXX, MAXY = 36, 128
blankcanvas = numpy.zeros((MAXX, MAXY), dtype=int, order='C')
blankscreen = rivaloled.bitstobytes(blankcanvas)

class Canvas:
    def __init__(self, canvas):
        self.canvas = canvas


    def setpixel(self, x, y):
        self.canvas[x, y] = 1


    def drawcanvas(self):
        rivaloled.sendframe(rivaloled.bitstobytes(self.canvas))


    def tick(self):
        time.sleep(.05)
        self.canvas = numpy.zeros((MAXX, MAXY), dtype=int, order='C')
        #rivaloled.sendframe(blankscreen)

