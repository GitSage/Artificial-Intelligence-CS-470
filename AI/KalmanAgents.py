__author__ = 'ben'

import Agents
import math
from Timer import Timer
import numpy as npy
# import matplotlib.pyplot as plt
from PDController import PDController
import time

class ClayPigeonAgent(Agents.Agent):
    pass

class StationaryClayPigeon(ClayPigeonAgent):
    pass


class ConstantVelocityClayPigeon(ClayPigeonAgent):
    def __init__(self, tank_index, state):
        self.state = state
        self.state.mytanks['0'].speed(0.2)

class NonConformingClayPigeon(ClayPigeonAgent):
    def __init__(self, tank_index, state):
        self.state = state
        self.state.mytanks['0'].speed(1)
        self.state.mytanks['0'].set_angvel(0.7)

class KalmanAgent(Agents.Agent):

    def __init__(self, tank_index, target_color, state):
        self.state = state
        self.target_color = target_color
        self.tank_index = tank_index
        self.pdc = PDController()
        self.timer_id = Timer.add_task(self.update)

    def update(self):
        angvel = self.getAngvelToTarget()
        self.state.mytanks['0'].set_angvel(angvel)

    def getAngvelToTarget(self):
        """
        Calculates the vector that we should be facing to kill the target, then uses the PDController to find the
        angular velocity required to face the target.
        This calculation is performed like this:
        1. Use the Kalman Filter to get the predicted next location of the target.
        2. Add to that vector the distance that the target will travel while the bullet fires.
        3. Pass the vector into the PDController to find the direction that we should face.
        :return float: the angular velocity that we need in order to correctly face the target.
        """
        self.state.update_mytanks()
        self.state.update_othertanks()
        enemy_tank = self.state.othertanks[self.target_color][0]
        ang = self.ang(enemy_tank.x, enemy_tank.y)
        target_vec = [-math.cos(ang), -math.sin(ang)]

        # step 1

        # step 3
        next_action = self.pdc.get_next_action(self.state.mytanks[self.tank_index], target_vec)
        return next_action['angvel']

    def ang(self, x, y):
        tank = self.state.mytanks['0']
        angle = math.atan2(tank.y - y, tank.x - x)
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
