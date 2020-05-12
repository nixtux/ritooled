import rivaloled
import numpy
import time

MAXX, MAXY = 36, 128


class Canvas:
    def __init__(self, canvas):
        self.canvas = canvas

    # setpixel(self, position x, position y)
    def setpixel(self, x, y):
        self.canvas[x, y] = 1

    # drawcanvas(self) display canvas, delay for screensaver in milliseconds
    def drawcanvas(self, delay):
        rivaloled.sendframe(self.canvas, delay)

    # tick(self) sleep for 1/10 sec ergo (10fps), and clears canvas
    def tick(self):
        time.sleep(.1)
        self.canvas = numpy.zeros((MAXX, MAXY), dtype=int, order='C')
