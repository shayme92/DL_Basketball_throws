from Consts import Consts
C = Consts()

class Ball:
    """
    Class to keep track of a ball's location.
    """
    def __init__(self):
        self.isTouchedBoardFlag = False
        self.x = 0
        self.y = 0
        self.prev_y = 0
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = -9.8 #gravity

    def updateVx(self, dt):
        self.vx = self.vx + self.ax * dt
        return self.vx

    def updateVy(self, dt):
        self.vy = self.vy + self.ay * dt
        return self.vy

    def updateX(self, dt):
        self.x = int(self.x + 0.5*(self.vx + self.updateVx(dt))*dt)
        return self.x

    def updateY(self, dt):
        self.prev_y = self.y
        self.y = int(self.y - 0.5*(self.vy + self.updateVy(dt))*dt)
        return self.y

    def isTouchedBoard(self):
        if (self.x+C.BALL_RADIUS)>=(C.BOARD_X) and \
                (self.y<C.BOARD_Y_BOTTOM and self.y>C.BOARD_Y):
            return True
        return False

    def touchBoardProccess(self):
        if self.isTouchedBoard():
            self.vx *=-1
            self.isTouchedBoardFlag = True

    def isScore(self):
        x_bool = ((self.x+C.BALL_RADIUS)<=(C.HOOP_X+2*C.HOOP_RADIUS)) and ((self.x-C.BALL_RADIUS)>=C.HOOP_X)
        y_bool = (self.prev_y<=C.HOOP_Y) and (self.y>=C.HOOP_Y)
        if (x_bool) and (y_bool):
            return True
        return False

    def isStartMoving(self):
        return self.vx or self.vy