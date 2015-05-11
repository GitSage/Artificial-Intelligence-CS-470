import math
import Timer

class PDController:

    def __init__(self):
        self.goal_vec = [0,0]
        self.prev_vec = [0, 0]
        self.prev_dir_error = 0
        self.prev_speedx_error = 0
        self.prev_speedy_error = 0

    def get_next_action(self, tank, vec):
        self.prev_vec = list(self.goal_vec)
        self.goal_vec = vec
        return {'angvel': self.get_dir_to_goal(tank), 'speed': 1}

    def get_dir_to_goal(self, tank):
        # The direction I should be facing minus the direction that I am facing
        error = self.dir_error(tank)
        new_dir = 1 * error + 1 * (error - self.prev_dir_error) / Timer.Timer.TIME_PER_SLEEP
        self.prev_dir_error = error
        return new_dir

    def get_speed_to_goal(self, tank, vec):
        # The direction I should be facing minus the direction that I am facing
        errorx = self.speed_error(vec, self.prev_speedx_error)
        errory = self.speed_error(vec, self.prev_speedy_error)
        newspeedx = 1 * errorx + 1 * (errorx - self.prev_speedx_error) / Timer.Timer.TIME_PER_SLEEP
        newspeedy = 1 * errory + 1 * (errory - self.prev_speedy_error) / Timer.Timer.TIME_PER_SLEEP
        self.prev_speedx_error = errorx
        self.prev_speedy_error = errory
        print "errorx: ", errorx
        print "errory: ", errory
        print "newspeedx: ", newspeedx
        print "newspeedy: ", newspeedy

        print math.sqrt(newspeedx**2 + newspeedy**2)
        return math.sqrt(newspeedx**2 + newspeedy**2)

    def dir_error(self, tank):
        return self.ang() - tank.angle #ideal angle - actual angle

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
