import math
import Timer


class PDController:

    def __init__(self):
        self.goal_vec = [0,0]
        self.prev_vec = [0, 0]
        self.prev_dir_error = 0
        self.prev_speedx_error = 0
        self.prev_speedy_error = 0

    def get_next_action(self, tank, vec, speed=1):
        self.prev_vec = list(self.goal_vec)  # clone the old array into a new one
        self.goal_vec = vec
        next_action = {'angvel': self.get_dir_to_goal(tank), 'speed': speed}
        # print next_action
        return next_action

    def get_dir_to_goal(self, tank):
        error = self.dir_error(tank)  # The direction I should be facing minus the direction that I am facing
        new_dir = 1 * error + (0 * (error - self.prev_dir_error) / Timer.Timer.time_passed)
        self.prev_dir_error = error
        return new_dir

    def get_speed_to_goal(self, tank, vec):
        # The direction I should be facing minus the direction that I am facing
        errorx = self.speed_error(vec, self.prev_speedx_error)
        errory = self.speed_error(vec, self.prev_speedy_error)
        newspeedx = 1 * errorx + 1 * (errorx - self.prev_speedx_error) / Timer.Timer.time_passed
        newspeedy = 1 * errory + 1 * (errory - self.prev_speedy_error) / Timer.Timer.time_passed
        self.prev_speedx_error = errorx
        self.prev_speedy_error = errory
        return math.sqrt(newspeedx**2 + newspeedy**2)

    def dir_error(self, tank):
        return self.ang() - tank.angle  # ideal angle - actual angle

    def speed_error(self, vec, prev_v):
        return self.desired_speed(vec) - prev_v  # ideal speed - actual speed

    def desired_speed(self, vec):
        x = vec[0]
        y = vec[1]
        return math.sqrt(x**2 + y**2)

    def ang(self):
        angle = math.atan2(self.goal_vec[1], self.goal_vec[0])
        '''Make any angle be between +/- pi.'''
        angle -= 2 * math.pi * int(angle / (2 * math.pi))
        if angle <= -math.pi:
            angle += 2 * math.pi
        elif angle > math.pi:
            angle -= 2 * math.pi
        return angle
