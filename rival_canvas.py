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

    # drawrect(self, x, y, x1, y1)
    def drawrect(self, x, y, x1, y1):
        for px in range(x, x1):
            for py in range(y, y1):
                if py >= 0 and py < MAXY:
                    if px >= 0 and px < MAXX:
                        #print("Rec plot pos", x, y, x1, y1, px, py)
                        self.canvas[px, py] = 1

    # drawline() from point x,y to x1,y1
    def drawline(self, x, y, x1, y1):
        dy = y1-y
        dx = x1-x
        m = dy / dx
        py = y
        for px in range(x, x1):
            self.canvas[px, int(py)] = 1
            py = py + m


    # invert canvas
    def invertcanvas(self):
        self.canvas = numpy.logical_not(self.canvas).astype(int)

    # drawcanvas(self) display canvas, delay for screensaver in milliseconds
    def drawcanvas(self, delay):
        rivaloled.sendframe(self.canvas, delay)


    # tick(self) sleep for 1/10 sec ergo (10fps), and clears canvas
    def tick(self):
        time.sleep(.1)
        self.canvas = numpy.zeros((MAXX, MAXY), dtype=int, order='C')
