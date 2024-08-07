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
        self.head = (self.fin , (self.h) + self.amp*(np.sin(self.freq*self.fin)))

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
    
    def __init__(self, sheet, x, y, wid, hei, coeff, total, randomAssets=0) :
        super().__init__()
        self.sheet = sheet
        self.wid = wid
        self.hei = hei
        self.coeff = coeff
        self.total = total

        ####  For SpriteSheets with random static values to be re-rendered (Digitilazied PI for exemple), it's the totl number
        #     of these values, concatenated on the top of the actual Sprite frames;
        self.rndAssets = randomAssets
        if self.rndAssets!=0 :
            self.RNDframes = []
            self.getframes(self.RNDframes, self.rndAssets, 0)

        self.frames = []
        self.getframes(self.frames, self.total, randomAssets)
        self.current = 0

        self.inStatic = False
        self.image = self.frames[self.current]
        self.rect = self.image.get_rect()

        self.coord = [x,y]
        self.x = self.coord[0]

        self.hitBox = pg.Rect((self.rect.topleft[0] - 20, self.rect.topleft[1] - 20), (90, 85))
        self.rect.center = self.coord



    ## Frame by Frame method into the frames list :
    def getframes(self, list, total, initialized) :
        for frame in range(initialized, total + initialized) :
            image = pg.Surface((self.wid, self.hei)).convert_alpha()

            ## 3rd .blit() param -> rect of the sheet
            image.blit(self.sheet, (0,0), (0,frame*self.hei,self.wid,self.hei))

            ## scale
            image = pg.transform.scale(image, (self.wid*self.coeff, self.hei*self.coeff))

            ## transparency of the background (ignore black)
            image.set_colorkey((0, 0, 0))
            list.append(image)
    
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
        self.hitBox.center = self.rect.center
        self.x = self.x + sign*pace

    def reset(self) :
        self.current = 0
        self.image = self.frames[self.current]
        self.inStatic = True

    ## INHERITED !! --> to RE-ASSIGN
    def update(self, pace) :
        if self.rndAssets == 0:
            if self.current >= self.total - 1 :
                self.inStatic = True
                self.current = self.total - 1
            else :
                self.inStatic = False
                self.current+= pace
            self.image = self.frames[int(self.current)]
        else :
            if self.current >= self.total - 1 :
                self.inStatic = True
                ## 0.25 so each frame can be rendered 4 times in 60FPS, equivalent to the design wich upholds each digit for 2 frames in 30FPS
                self.current+= 0.25
                self.image = self.RNDframes[int(self.current) % self.rndAssets]
            else :
                self.inStatic = False
                self.current+= pace
                self.image = self.frames[int(self.current)]


    ## ONLY FOR THE MAIN SPRITE
    def getmainhitBox(self) :
        return self.hitBox

    def collisionCheck(self, rect):
        return self.getmainhitBox().colliderect(rect)


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

    def checkFinish(self) :
        return int(self.frame) >= self.total + self.fstIndex - 1
    
class movingSprite :
    def __init__(self, screenSize, width, height, total, fstIndex, folderPath, extension) :
        self.size = (width, height)
        self.screenSize = screenSize
        self.path = folderPath
        self.ext = extension
        self.total = total
        self.fstIndex = fstIndex
        self.frame = fstIndex
        self.coord = [screenSize[0],
                      RND.uniform(3/10,3/5)*screenSize[1]]
        self.rect = pg.transform.scale(pg.image.load(self.path + str(int(self.frame)) + self.ext), self.size).get_rect()

        self.shakeY = 1
        self.hitBox = pg.Rect((self.rect.topleft[0] + 50, self.rect.topleft[1]), (420, 430))
        self.rect.center = self.coord
    
    def move_n_draw(self, surface, transformPace, movePace, shakeCoeff, sign) :
        if int(self.frame) >= self.total + self.fstIndex - 1 :
            self.frame = self.fstIndex
        surface.blit(pg.transform.scale(pg.image.load(self.path + str(int(self.frame)) + self.ext), self.size), topleft_center(self.coord, self.size))
        self.frame = self.frame + sign*transformPace
        self.coord = [self.coord[0] - sign*movePace, self.coord[1] + self.shakeY*shakeCoeff]
        self.rect.center = self.coord
        self.hitBox.center = self.coord
        self.shakeY = self.shakeY*(-1)
        
    def reset(self):
        self.coord = [self.screenSize[0],
                      RND.uniform(2/10,9/10)*self.screenSize[1]]
        self.frame = self.fstIndex
        self.rect.center = self.coord

    def finished(self):
        return self.rect.right <= 0
    
    def getmainhitBox(self):
        return self.hitBox
    
# -------------------------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------------------------#

## Altered Sprite Group Class (for the PI's vertical teleport effect)
class customSpriteGroup(pg.sprite.Group):
    def __init__(self, screenSize) :
        super().__init__()
        self.screenWidth = screenSize[0]
        self.screenHeight = screenSize[1]

    def draw(self, surface):
        for sprite in self.sprites():
            self.draw_wrapped_sprite(sprite, surface)

    def draw_wrapped_sprite(self, sprite, surface):
        surface.blit(sprite.image, sprite.rect)
        

        ## Frame rendering
        if sprite.rect.bottom > self.screenHeight:
            surface.blit(sprite.image, (sprite.rect.x, sprite.rect.bottom - self.screenHeight - 50))
        elif sprite.rect.top < 0:
            surface.blit(sprite.image, (sprite.rect.x, sprite.rect.top + self.screenHeight + 50))

        ## Actual HitBox re-orienting (Rect moving, to not duplicate entities after teleport)      
        if sprite.rect.top > self.screenHeight:
            sprite.rect.top-= self.screenHeight
        elif sprite.rect.bottom < 0:
            sprite.rect.bottom+= self.screenHeight

    ## Screen Width Offset check, done apart fom the draw method due to hierarchia lcall (the PI's jump method is called BEFORE the draw())
    def widthOffsetCheck(self) :
        for sprite in self.sprites():
            if sprite.rect.left < 0 :
                sprite.rect.left = 0
            elif sprite.rect.right >= self.screenWidth :
                sprite.rect.right = self.screenWidth