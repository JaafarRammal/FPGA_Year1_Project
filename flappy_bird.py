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

def showScore(score, SCREEN):

    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
    	digit_image = Image.open(IMAGES['numbers'][digit])
    	totalWidth += digit_image.size[0]

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
    	digit_image = Image.open(IMAGES['numbers'][digit])
    	SCREEN.paste(digit_image, (int(Xoffset), int(SCREENHEIGHT * 0.1)), digit_image)
    	Xoffset += digit_image.size[0]

    return SCREEN

# **************** Check for pixels collision ****************

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
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

# **************** Generate Random Pipe ****************

def getRandomPipe():
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].size[1]
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]

# **************** Main Game ****************

# **** Bird display test ****

background = Image.open(BACKGROUNDS_LIST[1])
bird = Image.open(PLAYERS_LIST[2][2])
background.paste(bird, (50,int(SCREENHEIGHT/2)), bird)

# **** Pipes display test ****

IMAGES['pipe'] = (
    Image.open(PIPES_LIST[1]).rotate(180),
	Image.open(PIPES_LIST[1])
)

# get 2 new pipes to add to upperPipes lowerPipes list
# for third pipe its 2*PIPOFFSET
newPipe1 = getRandomPipe()
newPipe2 = getRandomPipe()

position = 10

# list of upper pipes
upperPipes = [
    {'x': SCREENWIDTH - position, 'y': newPipe1[0]['y']},
    {'x': SCREENWIDTH - position - PIPEOFFSET, 'y': newPipe2[0]['y']},
]

# list of lowerpipe
lowerPipes = [
    {'x': SCREENWIDTH - position, 'y': newPipe1[1]['y']},
    {'x': SCREENWIDTH - position - PIPEOFFSET, 'y': newPipe2[1]['y']},
]

for uPipe, lPipe in zip(upperPipes, lowerPipes):
    background.paste(IMAGES['pipe'][0], (int(uPipe['x']), int(uPipe['y'])),IMAGES['pipe'][0])
    background.paste(IMAGES['pipe'][1], (int(lPipe['x']), int(lPipe['y'])),IMAGES['pipe'][1])

# **** Some animation ****

pipeVelX = -4

# player velocity, max velocity, downward accleration, accleration on flap
playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
playerMaxVelY =  10   # max vel along Y, max descend speed
playerMinVelY =  -8   # min vel along Y, max ascend speed
playerAccY    =   1   # players downward accleration
playerRot     =  45   # player's rotation
playerVelRot  =   3   # angular speed
playerRotThr  =  20   # rotation threshold
playerFlapAcc =  -9   # players speed on flapping
playerFlapped = False # True when player flaps



# **** Score and base display test ****

start = time.time()
showScore(101, background)
background.paste(Image.open(IMAGES['base']), (-10*int((time.time()-start)%3), BASEY),Image.open(IMAGES['base']))

background.show()

