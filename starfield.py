#!/usr/bin/env python
 
"""A simple starfield example. Note you can move the 'center' of
the starfield by leftclicking in the window. This example show
the basics of creating a window, simple pixel plotting, and input
event management"""
 
 
import random, math
from Xlib import display
from rival_canvas import Canvas
import numpy

MAXX, MAXY = 36, 128

oled = Canvas(numpy.zeros((MAXX, MAXY), dtype=int, order='C'))
timeout = 60000

#constants
WINSIZE = [MAXX, MAXY]
WINCENTER = [MAXX/2, MAXY/2]
NUMSTARS = 60


def screensize():
    x = display.Display().screen().width_in_pixels
    y = display.Display().screen().height_in_pixels
    return x, y 


def mousepos():
    """mousepos() --> (x, y) get the mouse coordinates on the screen (linux, Xlib)."""
    data = display.Display().screen().root.query_pointer()._data
    return data["root_x"], data["root_y"]


def init_star():
    dir = random.randrange(100000)
    velmult = random.random()*.6+.4
    vel = [math.sin(dir) * velmult, math.cos(dir) * velmult]
    return vel, WINCENTER[:]
 
 
def initialize_stars():
    stars = []
    for x in range(NUMSTARS):
        star = init_star()
        vel, pos = star
        steps = random.randint(0, WINCENTER[0])
        pos[0] = pos[0] + (vel[0] * steps)
        pos[1] = pos[1] + (vel[1] * steps)
        vel[0] = vel[0] * (steps * .09)
        vel[1] = vel[1] * (steps * .09)
        stars.append(star)
    move_stars(stars)
    return stars
 

def draw_stars(stars):
    for vel, pos in stars:
        Canvas.setpixel(oled, int(pos[0]), int(pos[1]))
 
 
def move_stars(stars):
    for vel, pos in stars:
        pos[0] = pos[0] + vel[0]
        pos[1] = pos[1] + vel[1]
        if not 0 <= pos[0] <= WINSIZE[0] or not 0 <= pos[1] <= WINSIZE[1]:
            vel[:], pos[:] = init_star()
        else:
            vel[0] = vel[0] * 1.05
            vel[1] = vel[1] * 1.05
 
 
def main():
    x, y = screensize()
    xratio = x/MAXX
    yratio = y/MAXY

    "This is the starfield code"
    #create our starfield
    random.seed()
    stars = initialize_stars()

    #main game loop
    done = 0
    while not done:
        draw_stars(stars)
        move_stars(stars)
        Canvas.drawcanvas(oled, timeout)
        posx, posy = mousepos()
        posx = posx / xratio
        posy = posy / yratio
        WINCENTER[:] = (posx, posy)
        """
        for e in pygame.event.get():
            if e.type == MOUSEMOTION:
                print("mouse")
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = 1
                break
            elif e.type == MOUSEMOTION:
                print("mouse", pygame.mouse.get_pos())
                WINCENTER[:] = list(e.pos)
        """
        Canvas.tick(oled)
 
 
# if python says run, then we should run
if __name__ == '__main__':
    main() 