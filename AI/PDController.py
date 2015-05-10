import math


class PDController:

    def __init__(self):
        self.goal_vec = [0, 0]
        self.prev_vec = [0, .01]  # this avoids being "stuck" right away

    def get_next_action(self, tank, vec):
        self.prev_vec = list(self.goal_vec)
        self.goal_vec = vec
        return {'angvel': self.get_dir_to_goal(tank), 'speed': 1}

    def get_dir_to_goal(self, tank):
        # The direction I should be facing minus the direction that I am facing
        return 1 * (self.ang() - tank.angle)

    def ang(self):
        angle = math.atan2(self.goal_vec[1], self.goal_vec[0])
        '''Make any angle be between +/- pi.'''
        angle -= 2 * math.pi * int(angle / (2 * math.pi))
        if angle <= -math.pi:
            angle += 2 * math.pi
        elif angle > math.pi:
            angle -= 2 * math.pi
        return angle
