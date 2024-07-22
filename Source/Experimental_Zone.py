import pygame as pg
import sys
import numpy as np
from Function_Plotting_Pool import xSqr

sys.path.append("F:\\PI-Scape\\")

## ------------------------------------------------------------------------------------------------------ ##
## ------------------------------------------------------------------------------------------------------ ##

pg.init()
size, clock = (1600 , 950), pg.time.Clock()

## Frames per sec, Data Pixel-Inch
FPS, DPI = 60, 43

# Surface screen : 
screen = pg.display.set_mode(size)

back = pg.transform.scale(pg.image.load("Assets\\Background\\Frames\\bgrd17.jpg"),(size))
plane = pg.image.load("Assets\\Background\\matplotlib_XY_axis.png")

coord, recCoord = (100, 100), (100, 100)
run = True


## Quadratics :
xSqr_Px = [(X[0]*43 + (size[0]/2) + 2 , -X[1]*52 + (size[1]/2)) for X in xSqr]

while run :
    for event in pg.event.get() :
        if event.type == pg.QUIT :
            run = False
    screen.blit(back, (0,0))
    screen.blit(plane, (0,0))


    pg.draw.lines(screen, (255, 255, 255), False, xSqr_Px, 3)

    mouse_x, mouse_y = pg.mouse.get_pos()

    # Print the mouse coordinates
    print(f"Mouse position: ({mouse_x}, {mouse_y})")
    pg.display.flip()
    clock.tick(FPS)

print(xSqr_Px)
pg.quit()