import math
import numpy as np

class Consts:
    """
    Consts for animation.
    """
    def __init__(self):

        #Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255,69,0)
        self.BORANGE = (250,131,32)
        self.GREY = (169,169,169)

        #Define some metrics
        self.SCREEN_WIDTH = 700
        self.SCREEN_HEIGHT = 500
        self.SCREEN_SIZE = math.sqrt((self.SCREEN_WIDTH**2)+(self.SCREEN_HEIGHT**2))
        self.BALL_RADIUS = int(22)
        self.HOOP_RADIUS = int(self.BALL_RADIUS*np.sqrt(100/27))
        self.BOARD_HEIGHT = 120
        self.BOARD_WIDTH = 72
        self.HOOP_Y = 120
        self.HOOP_X = self.SCREEN_WIDTH-130
        self.HOOP_X_R_EDGE = self.HOOP_X+2*self.HOOP_RADIUS
        self.HOOP_X_CENTER = self.HOOP_X+self.HOOP_RADIUS
        self.HOOP_CENTER_POINT = np.array([self.HOOP_X_CENTER, self.HOOP_Y])
        self.HOOP_WIDTH = 10

        self.BOARD_X = self.HOOP_X+2*self.HOOP_RADIUS
        self.BOARD_Y = self.HOOP_Y-self.BOARD_HEIGHT+(self.BOARD_HEIGHT*12/42)
        self.BOARD_Y_BOTTOM = self.BOARD_Y+self.BOARD_HEIGHT
        self.Nlines = 4