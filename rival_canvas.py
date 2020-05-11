import rivaloled
import numpy
import time

MAXX, MAXY = 36, 128


class Canvas:
    def __init__(self, canvas):
        self.canvas = canvas


    def setpixel(self, x, y):
        self.canvas[x, y] = 1


    def drawcanvas(self):
        rivaloled.sendframe(self.canvas)


    def tick(self):
        time.sleep(.1)
        self.canvas = numpy.zeros((MAXX, MAXY), dtype=int, order='C')
