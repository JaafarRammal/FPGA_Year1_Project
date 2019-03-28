from PIL import Image
import time
import random

# **************** Initialize assets ****************

# screen dimensions
SCREENWIDTH  = 288
SCREENHEIGHT = 512

# amount by which base can maximum shift to left
PIPEGAPSIZE  = 100 # gap between upper and lower part of pipe
BASEY        = int(SCREENHEIGHT * 0.79)
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

# ditance between two pipes
PIPEOFFSET = SCREENWIDTH / 2

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        'assets/sprites/bluebird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    'assets/sprites/background-day.png',
    'assets/sprites/background-night.png',
)

# list of pipes
PIPES_LIST = (
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png',
)

# numbers sprites for score display
IMAGES['numbers'] = (
    'assets/sprites/0.png',
	'assets/sprites/1.png',
	'assets/sprites/2.png',
	'assets/sprites/3.png',
	'assets/sprites/4.png',
	'assets/sprites/5.png',
	'assets/sprites/6.png',
	'assets/sprites/7.png',
	'assets/sprites/8.png',
	'assets/sprites/9.png'
)

# game over sprite
IMAGES['gameover'] = 'assets/sprites/gameover.png'
# message sprite for welcome screen
IMAGES['message'] = 'assets/sprites/message.png'
# base (ground) sprite
IMAGES['base'] = 'assets/sprites/base.png'

# **************** Show score on screen ****************

def add_score(score, frame):

    score_digit = [int(x) for x in list(str(score))]
    total_width = 0 # total width of all numbers to be printed

    for digit in score_digit:
    	digit_image = Image.open(IMAGES['numbers'][digit])
    	total_width += digit_image.size[0]

    Xoffset = (SCREENWIDTH - total_width) / 2

    for digit in score_digit:
    	digit_image = Image.open(IMAGES['numbers'][digit])
    	frame.paste(digit_image, (int(Xoffset), int(SCREENHEIGHT * 0.1)), digit_image)
    	Xoffset += digit_image.size[0]

    return frame

# **************** Check for pixels collision ****************

def pixel_collision(rect1, rect2, hitmask1, hitmask2):
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

# **************** Generate Pipe ****************

def get_pipe(gapY):

    gapY += int(BASEY * 0.2)
    pipe_height = IMAGES['pipe'][0].size[1]
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipe_height},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]

# **************** Final Frame Function ****************

def get_frame(background_index, bird_index, pipe_index, hole_1, hole_2, base_offset, bird_pos, pipe_pos, score):
    frame = Image.open(BACKGROUNDS_LIST[background_index])
    bird = Image.open(PLAYERS_LIST[bird_index][2])
    frame.paste(bird, (50,bird_pos), bird)

    IMAGES['pipe'] = (
        Image.open(PIPES_LIST[pipe_index]).rotate(180),
        Image.open(PIPES_LIST[pipe_index])
    )

    pipe_1 = get_pipe(hole_1)
    pipe_2 = get_pipe(hole_2)
    
    up_pipes = [
        {'x': SCREENWIDTH - pipe_pos, 'y': pipe_1[0]['y']},
        {'x': SCREENWIDTH - pipe_pos - PIPEOFFSET, 'y': pipe_2[0]['y']},
    ]

    low_pipes = [
        {'x': SCREENWIDTH - pipe_pos, 'y': pipe_1[1]['y']},
        {'x': SCREENWIDTH - pipe_pos - PIPEOFFSET, 'y': pipe_2[1]['y']},
    ]

    for u_p, l_p in zip(up_pipes, low_pipes):
        frame.paste(IMAGES['pipe'][0], (int(u_p['x']), int(u_p['y'])),IMAGES['pipe'][0])
        frame.paste(IMAGES['pipe'][1], (int(l_p['x']), int(l_p['y'])),IMAGES['pipe'][1])

    frame = add_score(score, frame)
    frame.paste(Image.open(IMAGES['base']), (-10*base_offset, BASEY),Image.open(IMAGES['base']))

    return frame

# **************** Testing Frame Function ****************

frame = get_frame(0,2,0,120,90,2,240,120,239)
frame.show()

# **************** Main Game Scratch ****************

# **** Bird display test ****

# background_index = 0
# bird_index = 2

# background = Image.open(BACKGROUNDS_LIST[background_index])
# bird = Image.open(PLAYERS_LIST[bird_index][2])
# background.paste(bird, (50,int(SCREENHEIGHT/2)), bird)

# # **** Pipes display test ****

# pipe_index = 0

# IMAGES['pipe'] = (
#     Image.open(PIPES_LIST[pipe_index]).rotate(180),
# 	Image.open(PIPES_LIST[pipe_index])
# )

# # get 2 new pipes to add to upperPipes lowerPipes list
# # for third pipe its 2*PIPOFFSET
# hole = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
# newPipe1 = get_pipe(hole)

# hole = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
# newPipe2 = get_pipe(hole)

# position = 30

# # list of upper pipes
# upperPipes = [
#     {'x': SCREENWIDTH - position, 'y': newPipe1[0]['y']},
#     {'x': SCREENWIDTH - position - PIPEOFFSET, 'y': newPipe2[0]['y']},
# ]

# # list of lowerpipe
# lowerPipes = [
#     {'x': SCREENWIDTH - position, 'y': newPipe1[1]['y']},
#     {'x': SCREENWIDTH - position - PIPEOFFSET, 'y': newPipe2[1]['y']},
# ]

# for uPipe, lPipe in zip(upperPipes, lowerPipes):
#     background.paste(IMAGES['pipe'][0], (int(uPipe['x']), int(uPipe['y'])),IMAGES['pipe'][0])
#     background.paste(IMAGES['pipe'][1], (int(lPipe['x']), int(lPipe['y'])),IMAGES['pipe'][1])

# # **** Some animation ****

# pipeVelX = -4

# # player velocity, max velocity, downward accleration, accleration on flap
# playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
# playerMaxVelY =  10   # max vel along Y, max descend speed
# playerMinVelY =  -8   # min vel along Y, max ascend speed
# playerAccY    =   1   # players downward accleration
# playerRot     =  45   # player's rotation
# playerVelRot  =   3   # angular speed
# playerRotThr  =  20   # rotation threshold
# playerFlapAcc =  -9   # players speed on flapping
# playerFlapped = False # True when player flaps



# # **** Score and base display test ****

# start = time.time()
# showScore(101, background)
# background.paste(Image.open(IMAGES['base']), (-10*int((time.time()-start)%3), BASEY),Image.open(IMAGES['base']))

# background.show()
