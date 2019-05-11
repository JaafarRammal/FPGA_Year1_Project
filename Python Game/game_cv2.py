import cv2
import random
import time

def draw_pipe(frame, pipe_x, hole_1, hole_2, gap, pipe_off):
    
    # upper pipe 1
    cv2.rectangle(frame,(pipe_x+5,hole_1),(pipe_x,-1),(0,0,0),-1)
    cv2.rectangle(frame,(pipe_x+10,hole_1),(pipe_x+5,-1),(133,170,69),-1)
    cv2.rectangle(frame,(pipe_x+15,hole_1),(pipe_x+10,-1),(149,183,81),-1)
    cv2.rectangle(frame,(pipe_x+20,hole_1),(pipe_x+15,-1),(164,198,72),-1)
    cv2.rectangle(frame,(pipe_x+25,hole_1),(pipe_x+20,-1),(181,212,104),-1)
    cv2.rectangle(frame,(pipe_x+30,hole_1),(pipe_x+25,-1),(189,230,112),-1)
    cv2.rectangle(frame,(pipe_x+35,hole_1),(pipe_x+30,-1),(200,220,130),-1)
    cv2.rectangle(frame,(pipe_x+40,hole_1),(pipe_x+35,-1),(189,230,112),-1)
    cv2.rectangle(frame,(pipe_x+45,hole_1),(pipe_x+40,-1),(181,212,104),-1)
    cv2.rectangle(frame,(pipe_x+50,hole_1),(pipe_x+45,-1),(117,156,88),-1)
    cv2.rectangle(frame,(pipe_x+55,hole_1),(pipe_x+50,-1),(84,128,34),-1)
    cv2.rectangle(frame,(pipe_x+60,hole_1),(pipe_x+55,-1),(84,128,34),-1)
    cv2.rectangle(frame,(pipe_x+65,hole_1),(pipe_x+60,-1),(84,128,34),-1)
    cv2.rectangle(frame,(pipe_x+70,hole_1),(pipe_x+65,-1),(0,0,0),-1)
    cv2.rectangle(frame,(pipe_x+5,hole_1),(pipe_x+65,hole_1-5),(0,0,0),-1)

    # lower pipe 1
    cv2.rectangle(frame,(pipe_x+5,hole_1+gap),(pipe_x,721),(0,0,0),-1)
    cv2.rectangle(frame,(pipe_x+10,hole_1+gap),(pipe_x+5,721),(133,170,69),-1)
    cv2.rectangle(frame,(pipe_x+15,hole_1+gap),(pipe_x+10,721),(149,183,81),-1)
    cv2.rectangle(frame,(pipe_x+20,hole_1+gap),(pipe_x+15,721),(164,198,72),-1)
    cv2.rectangle(frame,(pipe_x+25,hole_1+gap),(pipe_x+20,721),(181,212,104),-1)
    cv2.rectangle(frame,(pipe_x+30,hole_1+gap),(pipe_x+25,721),(189,230,112),-1)
    cv2.rectangle(frame,(pipe_x+35,hole_1+gap),(pipe_x+30,721),(200,220,130),-1)
    cv2.rectangle(frame,(pipe_x+40,hole_1+gap),(pipe_x+35,721),(189,230,112),-1)
    cv2.rectangle(frame,(pipe_x+45,hole_1+gap),(pipe_x+40,721),(181,212,104),-1)
    cv2.rectangle(frame,(pipe_x+50,hole_1+gap),(pipe_x+45,721),(117,156,88),-1)
    cv2.rectangle(frame,(pipe_x+55,hole_1+gap),(pipe_x+50,721),(84,128,34),-1)
    cv2.rectangle(frame,(pipe_x+60,hole_1+gap),(pipe_x+55,721),(84,128,34),-1)
    cv2.rectangle(frame,(pipe_x+65,hole_1+gap),(pipe_x+60,721),(84,128,34),-1)
    cv2.rectangle(frame,(pipe_x+70,hole_1+gap),(pipe_x+65,721),(0,0,0),-1)
    cv2.rectangle(frame,(pipe_x,hole_1+gap),(pipe_x+70,hole_1-5+gap),(0,0,0),-1)

    # upper pipe 2
    cv2.rectangle(frame,(pipe_x+5+pipe_off,hole_2),(pipe_x+pipe_off,-1),(0,0,0),-1)
    cv2.rectangle(frame,(pipe_x+10+pipe_off,hole_2),(pipe_x+5+pipe_off,-1),(133,170,69),-1)
    cv2.rectangle(frame,(pipe_x+15+pipe_off,hole_2),(pipe_x+10+pipe_off,-1),(149,183,81),-1)
    cv2.rectangle(frame,(pipe_x+20+pipe_off,hole_2),(pipe_x+15+pipe_off,-1),(164,198,72),-1)
    cv2.rectangle(frame,(pipe_x+25+pipe_off,hole_2),(pipe_x+20+pipe_off,-1),(181,212,104),-1)
    cv2.rectangle(frame,(pipe_x+30+pipe_off,hole_2),(pipe_x+25+pipe_off,-1),(189,230,112),-1)
    cv2.rectangle(frame,(pipe_x+35+pipe_off,hole_2),(pipe_x+30+pipe_off,-1),(200,220,130),-1)
    cv2.rectangle(frame,(pipe_x+40+pipe_off,hole_2),(pipe_x+35+pipe_off,-1),(189,230,112),-1)
    cv2.rectangle(frame,(pipe_x+45+pipe_off,hole_2),(pipe_x+40+pipe_off,-1),(181,212,104),-1)
    cv2.rectangle(frame,(pipe_x+50+pipe_off,hole_2),(pipe_x+45+pipe_off,-1),(117,156,88),-1)
    cv2.rectangle(frame,(pipe_x+55+pipe_off,hole_2),(pipe_x+50+pipe_off,-1),(84,128,34),-1)
    cv2.rectangle(frame,(pipe_x+60+pipe_off,hole_2),(pipe_x+55+pipe_off,-1),(84,128,34),-1)
    cv2.rectangle(frame,(pipe_x+65+pipe_off,hole_2),(pipe_x+60+pipe_off,-1),(84,128,34),-1)
    cv2.rectangle(frame,(pipe_x+70+pipe_off,hole_2),(pipe_x+65+pipe_off,-1),(0,0,0),-1)
    cv2.rectangle(frame,(pipe_x+5+pipe_off,hole_2),(pipe_x+65+pipe_off,hole_2-5),(0,0,0),-1)

    # lower pipe 2
    cv2.rectangle(frame,(pipe_x+5+pipe_off,hole_2+gap),(pipe_x+pipe_off,721),(0,0,0),-1)
    cv2.rectangle(frame,(pipe_x+10+pipe_off,hole_2+gap),(pipe_x+5+pipe_off,721),(133,170,69),-1)
    cv2.rectangle(frame,(pipe_x+15+pipe_off,hole_2+gap),(pipe_x+10+pipe_off,721),(149,183,81),-1)
    cv2.rectangle(frame,(pipe_x+20+pipe_off,hole_2+gap),(pipe_x+15+pipe_off,721),(164,198,72),-1)
    cv2.rectangle(frame,(pipe_x+25+pipe_off,hole_2+gap),(pipe_x+20+pipe_off,721),(181,212,104),-1)
    cv2.rectangle(frame,(pipe_x+30+pipe_off,hole_2+gap),(pipe_x+25+pipe_off,721),(189,230,112),-1)
    cv2.rectangle(frame,(pipe_x+35+pipe_off,hole_2+gap),(pipe_x+30+pipe_off,721),(200,220,130),-1)
    cv2.rectangle(frame,(pipe_x+40+pipe_off,hole_2+gap),(pipe_x+35+pipe_off,721),(189,230,112),-1)
    cv2.rectangle(frame,(pipe_x+45+pipe_off,hole_2+gap),(pipe_x+40+pipe_off,721),(181,212,104),-1)
    cv2.rectangle(frame,(pipe_x+50+pipe_off,hole_2+gap),(pipe_x+45+pipe_off,721),(117,156,88),-1)
    cv2.rectangle(frame,(pipe_x+55+pipe_off,hole_2+gap),(pipe_x+50+pipe_off,721),(84,128,34),-1)
    cv2.rectangle(frame,(pipe_x+60+pipe_off,hole_2+gap),(pipe_x+55+pipe_off,721),(84,128,34),-1)
    cv2.rectangle(frame,(pipe_x+65+pipe_off,hole_2+gap),(pipe_x+60+pipe_off,721),(84,128,34),-1)
    cv2.rectangle(frame,(pipe_x+70+pipe_off,hole_2+gap),(pipe_x+65+pipe_off,721),(0,0,0),-1)
    cv2.rectangle(frame,(pipe_x+pipe_off,hole_2+gap),(pipe_x+70+pipe_off,hole_2-5+gap),(0,0,0),-1)

def draw_bird(frame, bird_x, bird_y, wing):

    # body
    cv2.rectangle(frame,(bird_x,bird_y),(bird_x+30,bird_y+30),(0,0,0),2)
    cv2.rectangle(frame,(bird_x+2,bird_y+2),(bird_x+28,bird_y+10),(253,218,141),-1)
    cv2.rectangle(frame,(bird_x+2,bird_y+10),(bird_x+28,bird_y+19),(249,184,51),-1)
    cv2.rectangle(frame,(bird_x+2,bird_y+19),(bird_x+28,bird_y+28),(211,121,41),-1)

    # eye
    cv2.rectangle(frame,(bird_x+16,bird_y+2),(bird_x+28,bird_y+12),(255,255,255),-1)
    cv2.rectangle(frame,(bird_x+16,bird_y),(bird_x+30,bird_y+14),(0,0,0),2)
    cv2.rectangle(frame,(bird_x+23,bird_y+5),(bird_x+27,bird_y+9),(0,0,0),-1)

    # mouth
    cv2.rectangle(frame,(bird_x+16,bird_y+18),(bird_x+28,bird_y+26),(255,0,0),-1)
    cv2.rectangle(frame,(bird_x+16,bird_y+18),(bird_x+30,bird_y+26),(0,0,0),2)
    cv2.rectangle(frame,(bird_x+20,bird_y+21),(bird_x+28,bird_y+23),(0,0,0),-1)

    #wings
    cv2.rectangle(frame,(bird_x+4,bird_y+12+5*(wing-1)),(bird_x+10,bird_y+17+5*(wing-1)),(255,255,255),-1)
    cv2.rectangle(frame,(bird_x+4,bird_y+12+5*(wing-1)),(bird_x+10,bird_y+17+5*(wing-1)),(0,0,0),2)



def game():
    while True:
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 2
        fontColor = (255,255,255)
        lineType = 2
        pos = 940

        flap = False
        rise = False

        height = 1
        previous_height = height

        color_tresh = 27
        heigth_tresh = 10

        bird = 400
        wing = -1
        speed = 30

        pipe = 1300
        hole_1 = random.randint(1,20)*10
        hole_2 = random.randint(1,20)*10

        gap = 300
        pipe_h = 70

        score = 0

        gameover = False

        start = time.time()

        while not gameover:

            wing += 1
            wing = wing%21

            in_frame = cv2.imread('out.jpg')

            speed -= 3
            if cv2.waitKey(1) == ord('c'):
                speed = 23
                flap = False

            bird -= speed
            bird = min(bird, 590)

            pipe = pipe - 10

            if pipe < 640 + pipe_h:
                pipe = 1020
                hole_1 = hole_2
                hole_2 = random.randint(1,20)*10
                score += 1
                pos = 940 - (len(str(score))-2)*21



            draw_pipe(in_frame, pipe, hole_1, hole_2, gap, 320)
            cv2.rectangle(in_frame,(1280,721),(640, 650),(222,216,149),-1)
            cv2.rectangle(in_frame,(1280,650),(640, 625),(156,230,89),-1)
            cv2.rectangle(in_frame,(1280,625),(640, 622),(0,0,0),-1)
            draw_bird(in_frame, 800, bird, (int)(wing/7))

            if (bird < hole_1 or bird > hole_1 + gap + 30) and (pipe < 830 and pipe > 800 - pipe_h):
                gameover = True
                cv2.putText(in_frame,'Game Over', (800, 300), font, fontScale, fontColor,lineType)

            cv2.putText(in_frame,f"{score}", (pos,100), font, fontScale, fontColor,lineType)

            cv2.imshow('Game', in_frame)

    cv2.destroyAllWindows()


def main():
    game()


if __name__ == '__main__':
    main()
