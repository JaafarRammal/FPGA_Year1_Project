from PIL import Image, ImageDraw
import time
import random
import sys
import cv2
import numpy
import keyboard

# **************** IMPORTANT NOTICE ****************
# 
# Game parameters to modify game difficulty are
# marked with "#PARAM"
#
# CV2 was used for the purpose of loading and
# visualizing the frames in real-time only and does
# not act on modifying the frames. Its use will be
# removed on the PYNQ board to run the game
#
# Lines of code to serve the testing purpose (saving
# and loading the frame) are marked with "#TEST"

# *******************************************************************************************
# **************** THE FOLLOWING ARE RAN ONCE ON THE PYNQ BOARD TO INITIALIZE ***************
# *******************************************************************************************


# **************** Initialize assets ****************

# RESIZE FACTOR IF ANY PROBLEMS: 135/64

# screen dimensions
SCREENWIDTH  = 960
SCREENHEIGHT = 1080

# base Y-axis position
BASEY = int(SCREENHEIGHT * 0.79)

# gap between upper and lower part of pipe
PIPEGAPSIZE  = 253 #PARAM

# image dictionnary
IMAGES = {}

# ditance between two pipes
PIPEOFFSET = SCREENWIDTH / 2 + SCREENWIDTH / 8 #PARAM

# bird x position
BIRDHORZ = 230

# list of birds assets
PLAYERS_LIST = (
    # red bird
    (
        'assets_1920_1080/sprites/redbird-upflap.png',
        'assets_1920_1080/sprites/redbird-midflap.png',
        'assets_1920_1080/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        'assets_1920_1080/sprites/bluebird-upflap.png',
        'assets_1920_1080/sprites/bluebird-midflap.png',
        'assets_1920_1080/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'assets_1920_1080/sprites/yellowbird-upflap.png',
        'assets_1920_1080/sprites/yellowbird-midflap.png',
        'assets_1920_1080/sprites/yellowbird-downflap.png',
    ),
)

# list of backgrounds assets
BACKGROUNDS_LIST = (
    'assets_1920_1080/sprites/background-day.png',
    'assets_1920_1080/sprites/background-night.png',
)

# list of pipes assets
PIPES_LIST = (
    'assets_1920_1080/sprites/pipe-green.png',
    'assets_1920_1080/sprites/pipe-red.png',
)

# numbers assets for score display
IMAGES['numbers'] = (
    'assets_1920_1080/sprites/0.png',
	'assets_1920_1080/sprites/1.png',
	'assets_1920_1080/sprites/2.png',
	'assets_1920_1080/sprites/3.png',
	'assets_1920_1080/sprites/4.png',
	'assets_1920_1080/sprites/5.png',
	'assets_1920_1080/sprites/6.png',
	'assets_1920_1080/sprites/7.png',
	'assets_1920_1080/sprites/8.png',
	'assets_1920_1080/sprites/9.png'
)

# game over asset
IMAGES['gameover'] = 'assets_1920_1080/sprites/gameover.png'

# message asset for welcome screen
IMAGES['message'] = 'assets_1920_1080/sprites/message.png'
# base (ground) asset
IMAGES['base'] = 'assets_1920_1080/sprites/base.png'

# pipe dimensions
PIPE_WIDTH, PIPEHEIGHT = Image.open(PIPES_LIST[0]).size

# bird dimensions
BIRD_WIDTH, BIRD_HEIGHT = Image.open(PLAYERS_LIST[0][1]).size

# pixel tracker for debugging
TRACKER = Image.new('RGBA', (10, 10), (0, 0, 0, 0))


# **************** Show score on screen ****************

def add_score(score, frame):

    # get score digits in an array
    score_digit = [int(x) for x in list(str(score))]
    
    # width of score display
    total_width = 0
    for digit in score_digit:
    	digit_image = Image.open(IMAGES['numbers'][digit])
    	total_width += digit_image.size[0]

    # score display offset to center on x-axis 
    Xoffset = (SCREENWIDTH - total_width) / 2

    # display the score on input frame (assuming the frame has correct dimensions)
    for digit in score_digit:
    	digit_image = Image.open(IMAGES['numbers'][digit])
    	frame.paste(digit_image, (int(Xoffset), int(SCREENHEIGHT * 0.1)), digit_image)
    	Xoffset += digit_image.size[0]

    return frame

# **************** Generate Pipe ****************

def get_pipe(gapY):

    # gap position on Y-axis
    gapY += int(BASEY * 0.2)
       
    # X offset
    pipeX = SCREENWIDTH + 10

    # build the pipe
    return [
        {'x': pipeX, 'y': gapY - PIPEHEIGHT},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]

# **************** Final Frame Function ****************

def get_frame(background_index, bird_index, bird_form, pipe_index, hole_1, hole_2, hole_3, bird_pos, pipe_pos, reached, score):
    
    # load background
    frame = Image.open(BACKGROUNDS_LIST[background_index])

    # not gameover
    gameover = False

    # load pipe assets
    IMAGES['pipe'] = (
        Image.open(PIPES_LIST[pipe_index]).rotate(180),
        Image.open(PIPES_LIST[pipe_index])
    )

    # build three pipes with the holes input
    pipe_1 = get_pipe(hole_1)
    pipe_2 = get_pipe(hole_2)
    pipe_3 = get_pipe(hole_3)
    
    # offset pipes at the beginning of game
    # so they are not created in front of the bird
    offset = PIPEOFFSET
    if not reached:
        offset = -1000

    # map upper pipes positions
    up_pipes = [
        {'x': SCREENWIDTH - pipe_pos, 'y': pipe_1[0]['y']},
        {'x': SCREENWIDTH - pipe_pos - offset, 'y': pipe_2[0]['y']},
        {'x': SCREENWIDTH - pipe_pos - 2*offset, 'y': pipe_3[0]['y']},
    ]

    # map lower pipes positions
    low_pipes = [
        {'x': SCREENWIDTH - pipe_pos, 'y': pipe_1[1]['y']},
        {'x': SCREENWIDTH - pipe_pos - offset, 'y': pipe_2[1]['y']},
        {'x': SCREENWIDTH - pipe_pos - 2*offset, 'y': pipe_3[1]['y']},
    ]

    # add pipes to the frame
    for u_p, l_p in zip(up_pipes, low_pipes):
        frame.paste(IMAGES['pipe'][0], (int(u_p['x']), int(u_p['y'])),IMAGES['pipe'][0])
        frame.paste(IMAGES['pipe'][1], (int(l_p['x']), int(l_p['y'])),IMAGES['pipe'][1])
        #frame.paste(TRACKER, (int(l_p['x']), int(l_p['y']) - PIPEGAPSIZE))
        #frame.paste(TRACKER, (int(l_p['x']), int(l_p['y'])))
        
    # check for gameover
    if bird_pos + BIRD_HEIGHT > int(low_pipes[1]['y']) and int(low_pipes[1]['x']) < BIRD_WIDTH + BIRDHORZ and int(low_pipes[1]['x']) + PIPE_WIDTH > BIRDHORZ:
        gameover = True
    if bird_pos < int(low_pipes[1]['y']) - PIPEGAPSIZE and int(low_pipes[1]['x']) < BIRD_WIDTH + BIRDHORZ and int(low_pipes[1]['x']) + PIPE_WIDTH > BIRDHORZ:
        gameover = True
    
    ## Enabling this makes a gameover when bird touches the ground 
    # if bird_pos == 802:
    #    gameover = True
    
    # load bird asset
    bird = Image.open(PLAYERS_LIST[bird_index][bird_form])
    
    # add bird to frame
    frame.paste(bird, (BIRDHORZ,bird_pos), bird)
    
    # add score to frame
    frame = add_score(score, frame)
    
    # add base to frame
    frame.paste(Image.open(IMAGES['base']), (0, BASEY),Image.open(IMAGES['base']))

    return frame, gameover

# ***************************************************************************
# **************** THE FOLLOWING IS TO RUN FOR EVERY NEW GAME ***************
# ***************************************************************************
  
# **************** Game ****************

# choose random background
BACKGROUND_IN = random.randrange(0,2)

# load waiting screen
frame = Image.open(BACKGROUNDS_LIST[BACKGROUND_IN])
message = Image.open(IMAGES['message'])
frame.paste(message, (int(SCREENWIDTH/2 - message.size[0]/2), int(SCREENHEIGHT/2 - message.size[1]/2)), message)

# TEST (START)
frame.save('frame_big.png')
imageSource = 'frame_big.png'
image = cv2.imread(imageSource)
if image is not None:
    cv2.imshow('image',image)
elif image is None:
    print ("Error loading image")
# TEST (END)

# wait for button
k = cv2.waitKey(0)

# initialize parameters

# not gameover
gameover = False 

# bird horizontal position
bird_pos = 400

# bird wings position (up, middle, down)
bird_form = 0.0

# pipe start position
# more negative -> more time for first appearance
pipe_pos = -1000

# score init to 0
score = 0

# pipe horizontal speed
pipe_inc = 30 #PARAM

# bird vertical speed
bird_inc = 17 #PARAM

# holes
hole_1 = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
hole_2 = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
hole_3 = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))

# randomize bird and pipe colors
BIRD_IN = random.randrange(0,3)
PIPE_IN = random.randrange(0,2)

# start regulators
reached = False
score_start = 0

# flap boolean
flap = False

while(not gameover):
  
    # TEST (START)
    if cv2.waitKey(1) == ord('c'):
        flap = True
    bird_form += 1
    frame, gameover = get_frame(BACKGROUND_IN, BIRD_IN, int(bird_form)%3,PIPE_IN,hole_1,hole_2,hole_3, bird_pos, pipe_pos, reached, score)
    # TEST (END)
    
    #frame.paste(TRACKER, (BIRDHORZ+BIRD_WIDTH,bird_pos))

    # update bird position
    bird_pos += bird_inc
    bird_pos = min(bird_pos,bird_pos%SCREENHEIGHT)
    bird_pos = min(802, bird_pos)
 
    #update pipe position
    pipe_pos += pipe_inc
    
	# display pipes
    if(pipe_pos > 0):
        a = pipe_pos%PIPEOFFSET
        if(a < pipe_pos):
			# swap holes when a pipe disapears and rewind (like on a wheel)
            temp = hole_1
            hole_1 = hole_3
            hole_3 = hole_2
            hole_2 = temp
			
			# replace the hole that disapeared with a new one
            hole_3 = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
			
			# there is a pipe. Gameover can be checked now in get_frame
            reached = True

		# update score
        if a > BIRDHORZ and a <= BIRDHORZ  + pipe_inc and score_start > 23:
            score += 1
        else:
			
			# ghost pipe position (non-present pipe) can cause faulty
			# score at start. Avoid by using a dummy variable
			# to store the score
            score_start += 1
			
		# update pipe position
        pipe_pos = a

	# TEST (START)
    frame.save('frame_big.png')
    imageSource = 'frame_big.png'
    image = cv2.imread(imageSource)
    if image is not None:
        cv2.imshow('image',image)
    elif image is None:
        print ("Error loading image")
	# TEST (END)
		
	# if flapped, push the bird up
    if flap:
        bird_pos -= 105
        flap = False

# gameover simulation, bird falling down
while(bird_pos < 802):
    cv2.waitKey(1)
    bird_pos += 20
    frame, gameover = get_frame(BACKGROUND_IN, BIRD_IN, int(bird_form)%3,PIPE_IN,hole_1,hole_2,hole_3, min(bird_pos, 802), pipe_pos, reached, score)
    
	# TEST (START)
	frame.save('frame_big.png')
    imageSource = 'frame_big.png'
    image = cv2.imread(imageSource)
    if image is not None:
        cv2.imshow('image',image)
    elif image is None:
        print ("Error loading image")
	# TEST (END)

# display gameover asset
gameover_img = Image.open(IMAGES['gameover'])
frame.paste(gameover_img, (int(SCREENWIDTH/2 - gameover_img.size[0]/2), int(SCREENHEIGHT/2 - gameover_img.size[1]/2)), gameover_img)

# TEST (START)
frame.save('frame_big.png')
imageSource = 'frame_big.png'
image = cv2.imread(imageSource)
if image is not None:
    cv2.imshow('image',image)
elif image is None:
    print ("Error loading image")
cv2.waitKey(0)
# TEST (END)

# **************** END OF CODE ****************


