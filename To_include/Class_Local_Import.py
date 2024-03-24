import numpy as np
import random as RND
import pygame as pg
import sys
from To_include.Bezier_Local_Import import *


# -------------------------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------------------------#

class Wave :

    def __init__(self, h, freq, amp, deb, fin, length) :
        self.h = h
        self.freq = freq
        self.amp = amp
        self.deb = deb
        self.fin = fin
        self.length = length

    ## Wave updater : -pix_rate pixels from start to finish :
    def sin_update(self, pix_rate, s0) :
        if self.fin > (s0 - self.length) :
            self.fin-= pix_rate
        else :
            if self.fin > 0 :
                self.fin-= pix_rate
            if self.deb > 0 :
                self.deb-= pix_rate

    ## Random param generator :
    @classmethod
    def params_gen(cls, s0 , s1) : # RND h, RND freq, RND amp, RND (start,finish), RND len
        return [RND.uniform(5*s1/20, 15*s1/20),
                RND.uniform(0.001,0.02),
                RND.uniform(40, 300),
                s0, s0,
                RND.uniform(s0/8, 7*s0/8)]
    
    ## sin waves support method :
    def support(self) :
        X = np.linspace(self.fin,self.deb,int(abs(self.deb - self.fin)/4))
        return [(x , (self.h) + self.amp*(np.sin(self.freq*x))) for x in X]

# -------------------------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------------------------#

class SpriteSheet(pg.sprite.Sprite) :
    
    def __init__(self, sheet, x, y, wid, hei, coeff, total) :
        super().__init__()
        self.sheet = sheet
        self.wid = wid
        self.hei = hei
        self.coeff = coeff
        self.total = total
        self.animated = True

        self.frames = []
        self.getframes()
        self.current = 0

        self.inStatic = False
        self.image = self.frames[self.current]
        self.rect = self.image.get_rect()

        self.coord = [x,y]
        self.x = self.coord[0]
        self.rect.center = self.coord

    ## Frame by Frame method into the frames list :
    def getframes(self) :
        for frame in range(self.total) :
            image = pg.Surface((self.wid, self.hei)).convert_alpha()

            ## 3rd .blit() param -> rect of the sheet
            image.blit(self.sheet, (0,0), (0,frame*self.hei,self.wid,self.hei))

            ## scale
            image = pg.transform.scale(image, (self.wid*self.coeff, self.hei*self.coeff))

            ## transparency of the background (ignore black)
            image.set_colorkey((0, 0, 0))
            self.frames.append(image)

    
    def new_RNDxy(self, eps) :
        self.rect.center = [RND.uniform(self.coord[0]-eps, self.coord[0]+eps), RND.uniform(self.coord[1]-eps, self.coord[1]+eps)]

    def resetJump(self) :
        self.coord = self.rect.center
        self.x = self.coord[0]

    def mainFollow(self, obj) :
        self.coord = obj.coord

    def jump(self, amp, width, pace, sign) :
        self.rect.center = [self.x, PI_Trajectory(self.x,
                                           amp,
                                           width,
                                           sign,
                                           self.coord[0],
                                           self.coord[1])]
        self.x = self.x + sign*pace

    def reset(self) :
        self.current = 0
        self.image = self.frames[self.current]
        self.inStatic = True

    ## INHERITED !! --> to RE-ASSIGN
    def update(self, pace, switch_pos) :
        if self.animated == True :
            if self.current >= self.total - 1 :
                self.inStatic = True
                self.current = self.total - 1
            else :
                self.inStatic = False
                self.current+= pace

            self.image = self.frames[int(self.current)]

            if switch_pos == True :
                self.rect.center = [self.coord[0],
                                    self.coord[1] + PI_Trajectory(self.coord[0],
                                                                  self.eps, 
                                                                  1,
                                                                  self.coord[0],
                                                                  self.coord[1])]
                
                if self.currentcoord < 10000 - 1 :
                    self.currentcoord+= 1

    

# -------------------------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------------------------#

class Button :
    def __init__(self, x, y, width, height, paths) :
        self.size = (width, height)
        self.states = [pg.transform.scale(pg.image.load(paths[0]), self.size),
                       pg.transform.scale(pg.image.load(paths[1]), self.size)]
        
        self.image = self.states[0]

        self.coord = [x,y]
        self.rect = self.image.get_rect()
        self.rect.center = self.coord
        self.pressed = False
        
        self.draws = [0,0]

    def switch_image(self) :
        self.image = self.states[1 - self.states.index(self.image)]

    def draw(self, surface) :
        surface.blit(self.image, topleft_center(self.coord, self.size))
        self.draws[self.states.index(self.image)]+= 1

    def check_collision(self) :
        return self.rect.collidepoint(pg.mouse.get_pos()) 
    
    def press(self) :
        self.pressed = not self.pressed

# -------------------------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------------------------#
        
## Sprite class fro large sprites (no sprite sheet) :
class largeSprite :
    def __init__(self, width, height, coord, total, fstIndex, folderPath, extension) :
        self.size = (width, height)
        self.coord = coord

        self.path = folderPath
        self.ext = extension

        self.total = total


        self.fstIndex = fstIndex
        self.frame = fstIndex

    def draw(self, surface, pace, sign) :
        surface.blit(pg.transform.scale(pg.image.load(self.path + str(int(self.frame)) + self.ext), self.size), self.coord)
        self.frame = self.frame + sign*pace

    def reset(self) :
        self.frame = self.fstIndex
    
    def frameLock(self) :
        self.frame = self.total - 1