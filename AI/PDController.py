__author__ = 'ben'
import math
from Timer import Timer


class PDController:

    def __init__(self):
        self.goal_vec = [0, 0]
        self.prev_vec = [0, .01]  # this avoids being "stuck" right away
        self.stuck_counter = 0
        self.max_stuck_counter = 5 / Timer.TIME_PER_SLEEP  # 5 seconds

    def get_next_action(self, tank, vec):
        self.prev_vec = list(self.goal_vec)
        self.goal_vec = vec
        return {'angvel': self.get_dir_to_goal(tank), 'speed': 1}

    def get_dir_to_goal(self, tank):
        # The direction I should be facing minus the direction that I am facing
        ang = self.ang()
        if self.is_stuck():
            # turn around and hope
            ang = ang * -1
            self.stuck_counter += 1
            if self.stuck_counter == self.max_stuck_counter:
                self.stuck_counter = 0

        return 1 * (ang - tank.angle)

    def is_stuck(self):
        return False
        # return self.goal_vec == self.prev_vec or self.stuck_counter != 0


    def ang(self):
        angle = math.atan2(self.goal_vec[1], self.goal_vec[0])
        '''Make any angle be between +/- pi.'''
        angle -= 2 * math.pi * int(angle / (2 * math.pi))
        if angle <= -math.pi:
            angle += 2 * math.pi
        elif angle > math.pi:
            angle -= 2 * math.pi
        return angle
