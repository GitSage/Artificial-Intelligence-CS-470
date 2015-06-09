__author__ = 'ben'

import Agents
import math
from Timer import Timer
import numpy as npy
# import matplotlib.pyplot as plt
import PDController
import time

class ClayPigeonAgent(Agents.Agent):
    pass

class StationaryClayPigeon(ClayPigeonAgent):
    pass

class ConstantVelocityClayPigeon(ClayPigeonAgent):
    pass

class NonConformingClayPigeon(ClayPigeonAgent):
    pass

class KalmanAgent(Agents.Agent):

    def __init__(self, tank_index, target_color, state):
        self.state = state
        self.target_color = target_color
        self.tank_index = tank_index
        self.pdc = PDController

        self.xt = [self.state.mytanks[self.tank_index].x,  # x position
                     0,  # x velocity
                     0,  # x acceleration
                     self.state.mytanks[self.tank_index].y,  # y position
                     0,  # y velocity
                     0]  # y acceleration

        self.sigt = npy.array([[100.0, 0.0, 0.0, 0.0,   0.0, 0.0],  # initial covariance matrix. We don't think it's moving
                          [0.0,   0.1, 0.0, 0.0,   0.0, 0.0],  # but we're uncertain where it is.
                          [0.0,   0.0, 0.1, 0.0,   0.0, 0.0],
                          [0.0,   0.0, 0.0, 100.0, 0.0, 0.0],
                          [0.0,   0.0, 0.0, 0.0,   0.1, 0.0],
                          [0.0,   0.0, 0.0, 0.0,   0.0, 0.1]])

        dt = Timer.TIME_PER_TICK  # delta t
        c = 0  # represents friction. The server has no friction, so this is usually 0.

        self.F = npy.array([[1, dt, dt**2/2, 0, 0, 0],
                       [0, 1,  dt,      0, 0, 0],
                       [0, -c, 1,       0, 0, 0],
                       [0, 0,  0,       1, dt, dt**2/2],
                       [0, 0,  0,       0, 1, dt],
                       [0, 0,  0,       0, -c, 1]])
        self.F_trans = self.F.transpose()

        self.H = npy.array([[1, 0, 0, 0, 0, 0],
                       [0, 0, 0, 1, 0, 0]])
        self.H_trans = self.H.transpose()

        self.sigx = npy.array([[0.1, 0.0, 0.0,   0.0,   0.0, 0.0],  # Variance of the predicted state noise. Constant.
                          [0.0, 0.1, 0.0,   0.0,   0.0, 0.0],  #
                          [0.0, 0.0, 100.0, 0.0,   0.0, 0.0],
                          [0.0, 0.0, 0.0,   0.1,   0.0, 0.0],
                          [0.0, 0.0, 0.0,   0.0,   0.1, 0.0],
                          [0.0, 0.0, 0.0,   0.0,   0.0, 100.0]])

        self.sigz = npy.array([[25, 0],  # this is the noise of the x and y locations
                         [0, 25]])

    def update(self):
        next_action = self.pdcontroller.get_next_action(self.state., pf_vec)
        FSFTsigx = self.F.dot(self.sig0).dot(self.F_trans) + self.sigx
        HTBlahInverse = npy.inv(self.H.dot(FSFTsigx).dot(self.H_trans) + self.sigz)
        kalman_gain = FSFTsigx.dot(self.H_trans).dot(HTBlahInverse)


        # self.xt = self.F.dot(self.xt + kalman_gain).dot


    def dist(self, x, y):
        return math.sqrt((x - self.x)**2 + (y - self.y)**2)

    def ang(self, x, y):
        angle = math.atan2(self.y - y, self.x - x)
        '''Make any angle be between +/- pi.'''
        angle -= 2 * math.pi * int(angle / (2 * math.pi))
        if angle <= -math.pi:
            angle += 2 * math.pi
        elif angle > math.pi:
            angle -= 2 * math.pi
        return angle


# class KalmanVisualizer:
#     def __init__(self, width, height):
#         plt.ion()
#         self.x = 0
#         self.y = 0
#         self.r = 100
#         self.circle = plt.Circle((self.x, self.y), self.r, color='b')
#         plt.axis([-width/2, width/2, -height/2, height/2])
#
#         plt.gca().add_patch(self.circle)
#         plt.show()
#
#     def update(self, x, y, r):
#         self.circle.center = x, y
#         self.circle.radius = r
#         plt.draw()
#
# if __name__ == "__main__":
#     vis = KalmanVisualizer(800, 800)
#     vis.update(0, 0, 10)
#     time.sleep(1)
#     vis.update(100, 100, 100)
#     time.sleep(1)
#     vis.update(-100, -100, 150)
#     while 1:
#         pass
