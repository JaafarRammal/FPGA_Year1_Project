# Imperial College EIE-1: FPGA Flappy Bird

Demo: https://youtu.be/Gdy9L31zuA0

## Introduction

For our First Year Project in EIE at Imperial College, we are required to design a hardware system that performs real-time image processing on a video stream, implementing our proposed idea of an interactive game. Our system should perceive the real-world though a camera video stream and provide interactive output to the player via the HDMI monitor.

In response to the project requirements, we decided to build a replica of Flappy Bird. The classic game is a side-scroller where the player controls a bird by clicking on the screen to make the bird “flap up”, attempting to fly between columns of green pipes without hitting them. In our version, the only difference is that the player flaps their hands in front of the monitor to control the bird, feeding in an interactive and realistic experience for our flapping users.

Full Frame folders process the whole output frame. To add the game to the frame, we either use the vivado block (folders with in_game extension) or cv2 in the arm cpu (folders with \_cv2 extension)

## Directories:
- Full_Frame_CV2_720pi: This is the currently used version. FPGA detection on 720p. Game frame created and added by CPU with CV2. Includes final block design and schematic
- Full_Frame_CV2_1080pi: FPGA detection on 1080p. Game frame created and added by CPU with CV2
- Full_Frame_in_game_720pi: FPGA detection on 720p. Game frame added by FPGA after being shared by CPU through MMIO
- Green_Wrist_Detection: FPGA detection initial block test
- Jupyter_Notebooks: backups of Jupyter notebooks
- Python_Game: animating the Flappy Bird game with python. Contains a sprite-based version (import and assemble assets to form the frame) and a pixel-based version (draw all the elements pixel by pixel for every frame)
- Python_Tests: quick tests of our algorithms in python before implementing with Vivado
- Separate_Objects: 3 stages algorithm to distinghuish different bracelets of same color (a step to a multiplayer mode)
- Skin_Detection: FPGA block for HSV skin detection

## Using on your board:

### Setting up: 

- For the Jupyter Notebook use _./Jupyter_Notebooks/Game_v3.ipynb_
- For the overlay use _./Full_Frame_CV2_720pi/game.bit_ and _./Full_Frame_CV2_720pi/game.tcl_ (do NOT use v2)
- Print the green bracelets using the step file _/bracelets.step_ (best results with _ZIRO Fluo Green PLA_)
- In the same notebook folder create a text file named _highscores.txt_ and initialize it manually with 3 lines of 0 (as in 0/n0/n0/n)
- You are now ready to play!



### How to play:

- Run the notebook sections in order one by one. Allow for each section a reasonable runtime and check for any errors
- When the game starts running, there is no more need for the laptop ethernet connection: you can unplug your board and keep it running by itself on power!

The game has a play mode and a settings mode, toggled by switch 0

#### Play mode:

- Flap your hands to make the bird fly and avoid as many pipes as you can. That simple to use!
- When you score a highscore, it will save for the next game session
- You can check the detection on the bottom left screen. If the background presents white noise or your flap feels weird, jump to the settings mode to change the tresholds using switch 0
- To force exit a game to the main menu, press button 1
- To force exit the whole process, press button 0 (this will end the whole pynq board process)

#### Settings mode:

- Change difficulty with button 0 between easy, medium, and hard
- Select with switch 1 if which treshold to change (_Color treshold_ for hands detection and _Height treshold_ for flap detection)
- Use buttons 2/3 to increase/decrease the treshold value and button 1 to set it back to default
- For the color treshold, the best result is when the whole detection background is black and only your bracelets are white
- For the height treshold, you will be changing your "flap speed and range" (in other words how down you flap between two frames). A higher treshold means you have to flap stronger, faster, and on a large vertical distance to initiate the flap, and vice-versa. When changing the height treshold, you can test the flap by observing the 4 green LEDs on the board: these will blink when you flap
- You are now ready to play! Jump to _play mode_ using switch 0




