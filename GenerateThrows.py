import math
import time

import numpy as np
import pygame
import pygame.freetype
import pandas as pd
from Consts import Consts
C = Consts()

from RunGame import mainGame

def generate_throws_data():
    Velocity_range = [40, 110*1.5]
    Angle_range = [np.pi/2.5, np.pi/2.5]
    X_range = [0, C.HOOP_X]
    Y_range = [(C.HOOP_Y+C.SCREEN_HEIGHT)/2, (C.HOOP_Y+C.SCREEN_HEIGHT)/2]
    Nsamples = 10**6
    velocity_vec = np.random.uniform(Velocity_range[0],Velocity_range[1],Nsamples)
    angle_vec    = np.random.uniform(Angle_range[0],Angle_range[1],Nsamples)
    x_vec        = np.random.uniform(X_range[0],X_range[1],Nsamples)
    y_vec        = np.random.uniform(Y_range[0],Y_range[1],Nsamples)
    pos_vec      = [[x,y] for x,y in zip(x_vec,y_vec)]
    tic          = time.time()

    mainGame(pos_vec, velocity_vec, angle_vec, 10000)

    toc = time.time()
    # Get time of generate throws
    print('elapsed time of random thorws: %d seconds' % (toc-tic))



