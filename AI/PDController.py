__author__ = 'ben'
import math

class PDController:

    def __init__(self, time):
        self.time = time
        self.goal_vec = None

    def get_next_action(self, tank, vec):
        self.goal_vec = vec
        return {'angvel': self.get_dir_to_goal(tank), 'speed': .5}

    def get_dir_to_goal(self, tank):
        # The direction I should be facing minus the direction that I am facing
        return .2 * (self.ang() - tank.angle)

    def ang(self):
        angle = math.atan2(self.goal_vec[1], self.goal_vec[0])
        '''Make any angle be between +/- pi.'''
        angle -= 2 * math.pi * int(angle / (2 * math.pi))
        if angle <= -math.pi:
            angle += 2 * math.pi
        elif angle > math.pi:
            angle -= 2 * math.pi
        return angle
