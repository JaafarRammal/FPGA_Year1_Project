# FPGA_Year1_Project

For our First Year Project in EIE at Imperial College, we are required to design a hardware system that performs real-time image processing on a video stream, implementing our proposed idea of an interactive game. Our system should perceive the real-world though a camera video stream and provide interactive output to the player via the HDMI monitor.

In response to the project requirements, we decided to build a replica of Flappy Bird. The classic game is a side-scroller where the player controls a bird by clicking on the screen to make the bird “flap up”, attempting to fly between columns of green pipes without hitting them. In our version, the only difference is that the player flaps their hands in front of the monitor to control the bird, feeding in an interactive and realistic experience for our flapping users.

Full Frame folders process the whole output frame. To add the game to the frame, we either use the vivado block (folders with in_game extension) or cv2 in the arm cpu (folders with \_cv2 extension)

## Directories:
- Full_Frame_CV2_1080pi: FPGA detection on 1080p. Game frame created and added by CPU with CV2
- Full_Frame_CV2_720pi: FPGA detection on 720p. Game frame created and added by CPU with CV2 (USED VERSION). Includes final block design and schematic
- Full_Frame_in_game_720pi: FPGA detection on 720p. Game frame added by FPGA after being shared by CPU through MMIO
- Green_Wrist_Detection: FPGA detection initial block test
- Jupyter_Notebooks: backups of Jupyter notebooks
- Python_Game: animating the Flappy Bird game with python. Contains a sprite-based version (import and assemble assets to form the frame) and a pixel-based version (draw all the elements pixel by pixel for every frame)
- Python_Tests: quick tests of our algorithms in python before implementing with Vivado
- Separate_Objects: 3 stages algorithm to distinghuish different bracelets of same color (a step to a multiplayer mode)
- Skin_Detection: FPGA block for HSV skin detection

