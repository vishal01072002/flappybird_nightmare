import pygame
from pygame.locals import *
import random
import sys  # for exit from game through cross(X) button

# global variable
FPS = 32
SCREENWIDTH = 386
SCREENHEIGHT = 660
SCREEN = pygame.display.set_mode(
    (SCREENWIDTH, SCREENHEIGHT))  # for game screen
GROUND_Y = 575  # 80% OF HEIGHT
GAME_SPRITES = {}  # FOR SCORE NUMBER IMAGES
GAME_SOUNDS = {}
PLAYER = 'flappy game/images/mini_ghost bird.png'  # BIRD IMAGE FULL PATH
BACKGROUND = 'flappy game/images/background.png'
PIPE = 'flappy game/images/pipe2.png'


def welcome_screen():
    playerx = int(SCREENWIDTH/3)
    playery = int(SCREENHEIGHT/2.2)
    basex = 0

    while True:
        for event in pygame.event.get():
            # print(event,"\n")
            # event means user press any key and event.get return the key which is pressed by user
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                print("escape")
                print(event, "\n")
                # QUIT for (cross sign) and KEYDOWN (means any key is pressed) K_ESCAPE (Esc key)
                pygame.quit()  # exit from game
                sys.exit()  # exit from program

            # space or up key means start game and go out from this function
            if event.type == KEYDOWN and (event.type == K_SPACE or event.key == K_UP):
                print(event, "elseif\n")
                return

            # blit means show on screen
            else:
                print(event, "else\n")
                # it takaes 2 values 1st image and 2nd cordinates
                SCREEN.blit(GAME_SPRITES['message'], (0, 0))
                # SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUND_Y))

                # untill below function not call screen will no be change and always show above blits
                pygame.display.update()

                # control FPS it will not be above from given FPS
                FPSCLOCK.tick(FPS)


def main_game():
    score = 0
    playerx = int(SCREENWIDTH/3)
    playery = int(SCREENHEIGHT/2.2)
    basex = 0

    # create 2 random pipes
    newpipe1 = getrandompipe()
    newpipe2 = getrandompipe()

    # list of upper pipe
    upperpipe = [
        {'x': SCREENWIDTH+350, 'y': newpipe1[0]['y']},
        {'x': SCREENWIDTH+350 + (SCREENWIDTH/2), 'y': newpipe2[0]['y']}
    ]

    # list of lower pipe
    lowerpipe = [
        {'x': SCREENWIDTH+350, 'y': newpipe1[1]['y']},
        {'x': SCREENWIDTH+350 + (SCREENWIDTH/2), 'y': newpipe2[1]['y']}
    ]

    pipe_vel_x = -4  # pipe moves in negative direction

    player_vel_y = -9  # go down with velocity
    player_max_vel_y = 10  # max velocity
    player_min_vel_y = -8
    player_acc_y = 1   # accelaration

    player_flap_vel = -8  # velocity while flapping
    player_flapped = False  # It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            # event means user press any key and event.get return the key which is pressed by user
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # QUIT for (cross sign) and KEYDOWN (means any key is pressed) K_ESCAPE (Esc key)
                pygame.quit()  # exit from game
                sys.exit()  # exit from program

            # space or up key means start game and go out from this function
            if event.type == KEYDOWN and (event.type == K_SPACE or event.key == K_UP):
                if playery > 0:
                    player_vel_y = player_flap_vel
                    player_flapped = True
                    GAME_SOUNDS['wing'].play()

        crash_test = isCollide(playerx, playery, upperpipe, lowerpipe)
        # it return true if player is crased
        if crash_test:
            return

        # check for score
        playermid = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipe:
            pipemid = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipemid <= playermid < pipemid + 4:
                score += 1
                print(f"your score is {score}")
            GAME_SOUNDS['point'].play()

        # increase accleration after press key
        if player_vel_y < player_max_vel_y and not player_flapped:
            player_vel_y += player_acc_y

        if player_flapped:
            player_flapped = False

        player_height = GAME_SPRITES['player'].get_height()

        # increase height in y axis after press key
        # take minimum coz if bird at ground we dont want to more down (it wiil hinde behind base image)
        playery = playery + min(player_vel_y, GROUND_Y -
                                playery - player_height)

        # ---------------- moves pipes to the left
        # zip a=[1,2,3] b=[1,4,9]   ---> c = zip(a,b) ===> [(1,1), (2,4), (3,9)]

        for uppipe, lowpipe in zip(upperpipe, lowerpipe):
            # pipe_vel_x is negative so pipe moves in left direction
            uppipe['x'] += pipe_vel_x
            lowpipe['x'] += pipe_vel_x

        # add a new pipe when 1st pipe is about to go and then remove 1st
        if 0 < upperpipe[0]['x'] < 5:
            newpipe = getrandompipe()
            upperpipe.append(newpipe[0])
            lowerpipe.append(newpipe[1])

        # if pipe is out of the screen then remove
        # if pipe screen width - pipe width == pipe position means its out of the screen

        if upperpipe[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperpipe.pop(0)
            lowerpipe.pop(0)

        # blit our sprits on screen
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for uppipe1, lowpipe1 in zip(upperpipe, lowerpipe):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (uppipe1['x'], uppipe1['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],
                        (lowpipe1['x'], lowpipe1['y']))

        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUND_Y))

        # print number (score)
        mydigit = [int(x) for x in list(str(score))]
        width = 0
        for digit in mydigit:
            width += GAME_SPRITES['number'][digit].get_width()

        Xoffset = (SCREENWIDTH - width)/2

        for digit in mydigit:
            SCREEN.blit(GAME_SPRITES['number'][digit],
                        (Xoffset, SCREENHEIGHT*0.05))
            Xoffset += GAME_SPRITES['number'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperpipe, lowerpipe):
    plyrhight = GAME_SPRITES['player'].get_height()
    if playery > GROUND_Y - plyrhight or playery < 0:
        GAME_SOUNDS['die'].play()
        return True

    for pipe in upperpipe:
        pipeheight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeheight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['die'].play()
            return True

    for pipe in lowerpipe:
        if(playery + plyrhight > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['die'].play()
            return True 

    return False


def getrandompipe():
    """
    we make a get random pipe func which return list of dictonary both side pipe
    like {'x': value ,'y': value}, --> upper pipe
    {'x': value ,'y': value}  --> lower pipe  
    every x distance will be generated 10 px distance
    for we take min value taht mean pipe minimum height will be min
    generate random number between min and screen height - base_y
        ------- ofset, scren_hei - base_Y -1.2*ofset ------
    """

    pipe_height = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT*0.3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT -
                                   GAME_SPRITES['base'].get_height() - 1.6*offset))
    pipe_x = SCREENWIDTH + 25
    y1 = pipe_height - y2 + offset
    print(pipe_x, y1, y2)
    pipe = [
        {'x': pipe_x, 'y': -y1},  # for upper pipe
        {'x': pipe_x, 'y': y2}  # for lower pipe
    ]
    return pipe


if __name__ == "__main__":

    pygame.init()  # initilize all pygame modules

    # our program will not work more than 40 fps
    # it helps to control fps of our game
    FPSCLOCK = pygame.time.Clock()

    # give caption (heading on top of game scren)
    pygame.display.set_caption('flappy bird by lucifer')

    # it is a dictonary which key(number) have tuple(images) value
    GAME_SPRITES["number"] = (
        # convert alpha is used to render image on screen
        pygame.image.load('flappy game/numbers/0.png').convert_alpha(),
        pygame.image.load('flappy game/numbers/1.png').convert_alpha(),
        pygame.image.load('flappy game/numbers/2.png').convert_alpha(),
        pygame.image.load('flappy game/numbers/3.png').convert_alpha(),
        pygame.image.load('flappy game/numbers/4.png').convert_alpha(),
        pygame.image.load('flappy game/numbers/5.png').convert_alpha(),
        pygame.image.load('flappy game/numbers/6.png').convert_alpha(),
        pygame.image.load('flappy game/numbers/7.png').convert_alpha(),
        pygame.image.load('flappy game/numbers/8.png').convert_alpha(),
        pygame.image.load('flappy game/numbers/9.png').convert_alpha()
    )

    # --------- home screen it for test
    GAME_SPRITES["message"] = pygame.image.load(
        'flappy game/images/homescreen1.png').convert_alpha()

    GAME_SPRITES["base"] = pygame.image.load(
        'flappy game/images/ground2.png').convert_alpha()

    GAME_SPRITES["pipe"] = (
        pygame.image.load(PIPE).convert_alpha(),
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180)
        # it rotate image in give angle
    )

    # gamae sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('flappy game/sounds/die.wav')
    # == hit coz hit means end
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('flappy game/sounds/die.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('flappy game/sounds/swoosh.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('flappy game/sounds/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('flappy game/sounds/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcome_screen()  # show welcome screen untill usr press any key
        main_game()
