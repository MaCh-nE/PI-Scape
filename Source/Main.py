import pygame as pg
import numpy as np
import random as RND
import sys
from time import sleep

## Parent directory 
sys.path.append("C:\\Users\\PI-Scape\\")
# -------------------------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------------------------#

from To_include.Bezier_Local_Import import *
from To_include.Class_Local_Import import *

# -------------------------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------------------------#

pg.init()

# Display objects :

size = (1600 , 950)
# Surface screen : 
screen = pg.display.set_mode(size)
pg.display.set_caption("3.14SCAPE")


# Basic colors dict. (RGB):
colors = {
    "BLACK" : (0,0,0) ,
    "WHITE" : (255,255,255) ,
    "RED" : (255,0,0) ,
    "GREEN" : (0,255,0) ,
    "BLUE" : (0,0,255)
}

# -------------------------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------------------------#

# Key Locks dictionnary :
keylocks = {
    pg.K_UP : False,
    pg.K_DOWN : False,
    pg.K_LEFT : False,
    pg.K_RIGHT : False,
    pg.K_0 : False,
    pg.K_1 : False,
    pg.K_2 : False,
    pg.K_3 : False,
    pg.K_4 : False,
    pg.K_5 : False,
    pg.K_6 : False,
    pg.K_7 : False,
    pg.K_8 : False,
    pg.K_9 : False,
    pg.K_RETURN : False,
    pg.K_ESCAPE : False,
    pg.K_TAB: False,
    pg.K_CLEAR: False,
    pg.K_SPACE : False,
    pg.K_BACKSPACE : False,
    pg.MOUSEBUTTONDOWN : False,
    pg.MOUSEBUTTONUP : False,
    pg.MOUSEWHEEL : False
}

# Images (surfaces) :
img_b1 = pg.transform.scale(pg.image.load("Assets\\Background\\Frames\\bgrd1.jpg"),(size))
screen.blit(img_b1 , (0,0))
pg.display.flip()

img_b2 = pg.transform.scale(pg.image.load("Assets\\Background\\Frames\\bgrd17.jpg"),(size))

font_main = pg.font.Font('C:\\Users\Lenovo\\AppData\\Local\\Microsoft\\Windows\\Fonts\\pixel.ttf',110)
font_sub = pg.font.Font('C:\\Users\Lenovo\\AppData\\Local\\Microsoft\\Windows\\Fonts\\pixel.ttf',75)

img_f_1 = font_main.render("Welcome to PI-scape !",True,colors["WHITE"])
img_f_2 = font_sub.render("Press ENTER to start",True,colors["WHITE"])
r_f_1 = img_f_1.get_rect()
r_f_2 = img_f_2.get_rect()

lights = pg.transform.scale(pg.image.load("Assets\\Lights\\lights.png"),(size))
light = False

enter_button = Button(size[0]/2,
                2*size[1]/3,
                400,
                200,
                ["Assets\\Buttons\\enter_UNPRESSED.png", "Assets\\Buttons\\\enter_PRESSED.png"])

scoreboard = Button(size[0]/2,
                    70,
                    280,
                    140,
                    ["Assets\\Scoreboard\\Main Frames\\frame 1 no BG.png", "Assets\\Scoreboard\\Main Frames\\frame 2 no BG.png"])

score = 0
stateNull = pg.transform.scale(pg.image.load("Assets\\Scoreboard\\Score bits\\full neutral.png"), (scoreboard.size))
scoreSurfaces = [[pg.transform.scale(pg.image.load("Assets\\Scoreboard\\Score bits\\score\\" + str(j) + "\\" + str(i) +".png"), (scoreboard.size)) for i in range(10)]
                for j in [1, 10 ,100]]

# -------------------------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------------------------#

sprites = pg.sprite.Group()
intro_PI_sprite = SpriteSheet(pg.image.load("Assets\\Characters\\Pi\\Intro_PI\\Intro_Sprite(503 x 496).png"),
                     75,
                     93,
                     503,
                     496,
                     0.277,
                     17)
sprites.add(intro_PI_sprite)


intro_scoreboard = largeSprite(280,
                               140,
                               topleft_center((size[0]/2,70), (280, 140)),
                               48,
                               0,
                               "Assets\\Scoreboard\\Intro Animation\\sB",
                               ".png")

board_swipe = largeSprite(size[0],
                          size[1],
                          (0,0),
                          64,
                          1,
                          "Assets\\Background\\Swipe_Sprite\\Swipe_Sprite (",
                          ").png")


# Waves object list (default Wave constructor) (initialized with 1 wave at 1st) :
waves = [Wave(*Wave.params_gen(size[0], size[1]))]

# Technical block :
# jumpWay flag indicating wich arrow the jump follows (1: Clockwise / -1: Anti-Clockwise)
# run flag / Game status  (1: Welcome state / 2: Game wipe / 3: Game reset wipe / 4: Game start animation / 5: Game loop)
jumpWay = 1
run, wlc = True, 1
clock, FPS = pg.time.Clock(), 60


# -------------------------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------------------------#

# Game Loop :
while run :

# -------------------------------------------------------------------------------------------------------------------------------------#
    
    ## Event handler :
    for event in pg.event.get() :
        if event.type == pg.QUIT :
            run = False
        if event.type == pg.KEYDOWN :
            if event.key == pg.K_LEFT and keylocks[pg.K_LEFT] == False:
                ## !!->     Change of key press on each <- -> key press     <-!! 
                ## !!->     Main Sprite's x, y following that    <-!!
                jumpWay = -1
                main_PI_sprite.resetJump()

                UPDRAFT_sprite.mainFollow(main_PI_sprite)
                UPDRAFT_sprite.new_RNDxy(15)
                UPDRAFT_sprite.reset()

                if main_PI_sprite.inStatic == True :
                    main_PI_sprite.reset()
            
            if event.key == pg.K_RIGHT and keylocks[pg.K_RIGHT] == False:
                ## !!->     Change of key press on each <- -> key press     <-!! 
                ## !!->     Main Sprite's x, y following that    <-!!
                jumpWay = 1
                main_PI_sprite.resetJump()

                UPDRAFT_sprite.mainFollow(main_PI_sprite)
                UPDRAFT_sprite.new_RNDxy(15)
                UPDRAFT_sprite.reset()

                if main_PI_sprite.inStatic == True :
                    main_PI_sprite.reset()

            if event.key == pg.K_RETURN :
                waves = [Wave(*Wave.params_gen(size[0], size[1]))]
                score = 0
                
                keylocks[pg.MOUSEBUTTONDOWN] = False
                keylocks[pg.MOUSEBUTTONUP] = False
                wlc = 3

        if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
            if keylocks[pg.MOUSEBUTTONDOWN] == False and keylocks[pg.MOUSEBUTTONUP] == False :
                if enter_button.check_collision() :
                    enter_button.switch_image()
                    if enter_button.pressed == True :
                        wlc = 2
                        enter_button.press()
                        keylocks[pg.MOUSEBUTTONDOWN] = True
                        keylocks[pg.MOUSEBUTTONUP] = True
                    else :
                        enter_button.press()

# -------------------------------------------------------------------------------------------------------------------------------------#

    ## Welcome Block :
    if wlc == 1 :
        if RND.randint(0,4) == 3 :
            if light == False :
                screen.blit(lights,(0,0))
                light = True
            else :
                screen.blit(img_b1 , (0,0))
                light = False
            if RND.randint(1,3) == 3 :
                screen.blit(img_b1 , (0,0))
        
        screen.blit(img_f_1,(size[0]/2 - abs(r_f_1.right-r_f_1.left)/2 , size[1]/4))
        screen.blit(img_f_2,(size[0]/2 - abs(r_f_2.right-r_f_2.left)/2 , size[1]/2))
        enter_button.draw(screen)


    # Welcome wipe :
    elif wlc == 2 :
        if board_swipe.frame < board_swipe.total :
            board_swipe.draw(screen, 0.8, 1)
        else :
            board_swipe.frameLock()
            wlc = 4


    ## End wipe :
    elif wlc == 3 :
        if board_swipe.frame >= board_swipe.fstIndex :
            board_swipe.draw(screen, 1, -1)
        else :
            board_swipe.reset()
            wlc = 1
            keylocks[pg.K_LEFT] = True
            keylocks[pg.K_RIGHT] = True


    ## Start animation :
    elif wlc == 4 :
        if sprites.has(intro_PI_sprite) :
            screen.blit(img_b2 , (0,0))
            sprites.draw(screen)
            sprites.update(0.2, False)
            if intro_PI_sprite.inStatic == True :
                if intro_scoreboard.frame < intro_scoreboard.total :
                    intro_scoreboard.draw(screen, 0.36, 1)
                else :
                    intro_scoreboard.reset()

                    wlc = 5
                    intro_PI_sprite.reset()
                    sprites.remove(intro_PI_sprite)

                    main_PI_sprite = SpriteSheet(pg.image.load("Assets\\Characters\\Pi\\Main_PI_Rotation\\Main_Sprite(538 x 464).png"),
                            100,
                            100,
                            538,
                            464,
                            0.3,
                            63)
                    sprites.add(main_PI_sprite)

                    UPDRAFT_sprite = SpriteSheet(pg.image.load("Assets\\Transformations\\UPDRAFT\\Updraft_Sprite(454 x 550).png"),
                            170,
                            150,
                            454,
                            550,
                            0.17,
                            59)
                    sprites.add(UPDRAFT_sprite)
                    keylocks[pg.K_LEFT] = False
                    keylocks[pg.K_RIGHT] = False
        else :
            sprites.remove(main_PI_sprite)
            sprites.remove(UPDRAFT_sprite)
            sprites.add(intro_PI_sprite)


    ## Game Block :
    else :
        screen.blit(img_b2 , (0,0))
        sprites.draw(screen)
           
        # Main Sprite Rectangle for HIT-BOX adjustements : 
        # pg.draw.rect(screen, colors["GREEN"], main_PI_sprite.rect, width=2)
        # pg.draw.rect(screen, colors["GREEN"], UPDRAFT_sprite.rect, width=2)
        sprites.update(2, False)

        main_PI_sprite.jump(140, 0.15, 2.6, jumpWay)

        # Random new wave f screen (proportional to game diff further) :
        if RND.randint(1,500) == 5 :
            waves.append(Wave(*Wave.params_gen(size[0], size[1])))

        for wave in waves :
            if wave.fin>0 or wave.deb>0 :
                for center in wave.support() :
                    pg.draw.circle(screen,colors["WHITE"],center,RND.uniform(3,15),2)
            else :
                score+= 10
                scoreboard.press()
                del waves[waves.index(wave)]
                continue
            
            wave.sin_update(5, size[0])

        ## Scoreboard management :
        if scoreboard.pressed == True :
            scoreboard.switch_image()
            scoreboard.press()
        # 30 frames for green doted scoreboard
        if scoreboard.draws[1] == 30:
            scoreboard.switch_image()
            scoreboard.draws[1] = 0

        scoreboard.draw(screen)
        screen.blit(stateNull, topleft_center(scoreboard.coord, scoreboard.size))
        for i in range(3) :
            screen.blit(scoreSurfaces[i][digitilizer(score, 3)[i]], topleft_center(scoreboard.coord, scoreboard.size))
    
    pg.display.flip()
    clock.tick(FPS)


pg.quit()
