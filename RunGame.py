import math
import time

import numpy as np
import pygame
import pygame.freetype
import pandas as pd

from Ball import Ball
from Consts import Consts
C = Consts()
from Events import My_events
my_events = My_events()

def draw_hoop(screen):
    pygame.draw.line(screen, C.RED, [C.HOOP_X,C.HOOP_Y], [C.HOOP_X+2*C.HOOP_RADIUS,C.HOOP_Y], C.HOOP_WIDTH)
    for line in range(0,C.Nlines+1):
        if line<=C.Nlines/2:
            pygame.draw.line(screen, C.WHITE, [C.HOOP_X+2*C.HOOP_RADIUS*line/C.Nlines,C.HOOP_Y+C.HOOP_WIDTH/2], [C.HOOP_X+2*C.HOOP_RADIUS*(line+1)/C.Nlines,C.HOOP_Y+C.HOOP_WIDTH/2+60],4)
        if line>=C.Nlines/2:
            pygame.draw.line(screen, C.WHITE, [C.HOOP_X+2*C.HOOP_RADIUS*line/C.Nlines,C.HOOP_Y+C.HOOP_WIDTH/2], [C.HOOP_X+2*C.HOOP_RADIUS*(line-1)/C.Nlines,C.HOOP_Y+C.HOOP_WIDTH/2+60],4)

def draw_board(screen):
    pygame.draw.rect(screen,C.BLACK,(C.BOARD_X,C.BOARD_Y,8,C.BOARD_HEIGHT))
    pygame.draw.rect(screen,C.BLACK,(C.BOARD_X+10,C.BOARD_Y+20,8,C.SCREEN_HEIGHT-C.BOARD_Y-20))

def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    if (x1 == x2):
        y_coords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        x_coords = [x1] * len(y_coords)
    elif (y1 == y2):
        x_coords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        y_coords = [y1] * len(x_coords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        x_coords = [x for x in np.arange(x1, x2, dx if x1 < x2 else -dx)]
        y_coords = [y for y in np.arange(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(x_coords[1::2], y_coords[1::2]))
    last_coords = list(zip(x_coords[0::2], y_coords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)

def draw_static_shapes(screen,img,score,N_shots,GAME_FONT):
    screen.blit(img, [0, 0])
    draw_hoop(screen)
    draw_board(screen)
    if N_shots==0:
        text = ["SCORE: %d " % (score),
                "Num of throws: %d" % (N_shots),
                "RATIO: %0.2f" % (0.0)]
    else:
        text = ["SCORE: %d " % (score),
                "Num of throws: %d" % (N_shots),
                "RATIO: %0.2f" % (np.minimum(1.0,(score/N_shots)))]
    for i,line in enumerate(text):
        textsurface = GAME_FONT.render(line, False, C.WHITE)
        screen.blit(textsurface, (int(C.SCREEN_WIDTH / 3), 100+i*40))

def create_ball(x, y):
    """
    Function to make a new ball on screen.
    """
    ball = Ball()
    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.
    ball.x = int(x)
    ball.y = int(y)

    return ball

def get_axes_velocity(velocity,angle):
    vx = (velocity * math.cos((angle)))
    vy = (velocity * math.sin((angle)))
    return  vx,vy

def mainGame(pos_vec=[None], velocity_vec=[None], angle_vec=[None], score_target=np.inf):
    """
    This is our main game running code.
    """
    df = pd.DataFrame(data={'x':[],'y':[],'velocity':[],'angle':[],'isTouchBoard':[]})
    t = 0
    score = 0
    previous_score = 0
    ball_count = 0
    my_events = My_events()
    pygame.init()
    # Set the height and width of the screen
    size = [C.SCREEN_WIDTH, C.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("ThrowToBasket-DL")
    pygame.font.init()
    GAME_FONT  = pygame.font.SysFont('Comic Sans MS', 30)
    # Set the screen background
    BckImage = pygame.image.load('./assets/court.jpg').convert()
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # -------- Main Program Loop -----------
    # Loop until the user clicks the close button.
    pos = pos_vec[ball_count]
    velocity = velocity_vec[ball_count]
    angle = angle_vec[ball_count]
    while not my_events.done and score<score_target:
        if pos and 'ball' not in locals():
            ball = create_ball(pos[0], pos[1])
            isScored_flag = False
        if velocity and angle and not ball.isStartMoving():
            ball.vx, ball.vy = get_axes_velocity(velocity, angle)
            my_events.start_throw = True
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if my_events.draw_dash_line:
                    draw_static_shapes(screen, BckImage, score, ball_count, GAME_FONT)
                    x,y = pygame.mouse.get_pos()
                    draw_dashed_line(screen, C.WHITE, [ball.x,ball.y],[x,y])
            if event.type == pygame.MOUSEBUTTONUP:
                if 'ball' not in locals():
                    pos = pygame.mouse.get_pos()
                    isScored_flag = False
                    my_events.draw_dash_line = True
                elif (not angle) and (not velocity):
                    x,y = pygame.mouse.get_pos()
                    x = float(x)
                    y = float(y)
                    angle = np.arctan((y-float(ball.y))/(float(ball.x)-x))
                    velocity = 450*math.hypot((float(ball.x)-x),(y-float(ball.y)))/C.SCREEN_SIZE
                    if x>=ball.x:
                        velocity*=-1
                    print("velocity: %f, angle: %f " % (velocity,angle))
                    my_events.draw_dash_line = False


            elif event.type == pygame.QUIT:
                my_events.done = True
        # --- Drawing
        # Draw the ball
        if not my_events.draw_dash_line:
            draw_static_shapes(screen, BckImage, score, ball_count, GAME_FONT)
        if 'ball' in locals():
            # Draw the ball
            pygame.draw.circle(screen, C.BORANGE, [ball.x, ball.y], C.BALL_RADIUS)
            if ball.isStartMoving():
                ball.touchBoardProccess()
                if ball.isScore() and not isScored_flag:
                    score+=1
                    isScored_flag = True
                ball.updateX(0.12) #0.15
                ball.updateY(0.12) #0.15
            if ball.y>C.SCREEN_HEIGHT or ball.x>C.SCREEN_WIDTH:
                isTouchBoard = ball.isTouchedBoardFlag
                del ball

                ball_count+=1
                prev_pos = pos
                prev_velocity = velocity
                prev_angle = angle
                pos = pos_vec[ball_count]
                velocity = velocity_vec[ball_count]
                angle = angle_vec[ball_count]
                if previous_score < score:
                    df = df.append(
                        {'x': prev_pos[0], 'y': prev_pos[1], 'velocity': prev_velocity, 'angle': prev_angle,
                            'isTouchBoard': isTouchBoard}, ignore_index=True)
                    previous_score = score

        # Limit to 90 frames per second
        clock.tick(300)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # drop scored data set
    df.to_csv('dataset_%d.csv' % time.time())
    # Close everything down
    pygame.quit()


df = pd.read_csv('throwData.csv')
pos_vec = np.array([df['x'], df['y']]).T
angle_vec = np.array([df['angle']]).T
velocity_vec = np.array([df['velocity']]).T
# mainGame(pos_vec.tolist(), velocity_vec, angle_vec, 10000)