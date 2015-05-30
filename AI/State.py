import logging
import math


class State:

    def __init__(self, messenger, me):
        self.messenger = messenger
        self.mytanks = {}
        self.obstacles = []
        self.flags = {}
        self.bases = {}
        self.me = Me
        self.me.color = me

        logging.debug("Initializing state.")
        self.update_mytanks()
        self.update_obstacles()
        self.update_flags()
        self.update_bases()

    def update_mytanks(self):
        # mytank [index] [callsign] [status] [shots available] [time to reload] [flag] [x] [y] [angle] [vx] [vy]
        # [angvel]
        data = self.messenger.mytanks()
        for mytank in data.split("\n"):
            t = mytank.split(" ")
            self.mytanks[t[1]] = Tank(t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10], t[11], t[12],
                                      self.messenger)

    def update_obstacles(self):
        # obstacle [x1] [y1] [x2] [y2] ...
        self.obstacles = []
        data = self.messenger.obstacles()
        for obstacle in data.split("\n"):
            o = obstacle.split(" ")
            points = []
            for i in xrange(1, len(o), 2):
                points.append([float(o[i]), float(o[i+1])])
            self.obstacles.append(Obstacle(points))

    def update_flags(self):
        # flag [team color] [possessing team color] [x] [y]
        data = self.messenger.flags()
        for flag in data.split("\n"):
            f = flag.split(" ")
            newflag = Flag(f[1], f[2], float(f[3]), float(f[4]))
            self.flags[f[1]] = newflag
            if f[1] == self.me.color:
                self.me.flag = newflag

    def update_bases(self):
        data = self.messenger.bases()
        for base in data.split("\n"):
            b = base.split(" ")
            points = []
            for i in xrange(2, len(b), 2):
                points.append([float(b[i]), float(b[i+1])])
            newbase = Base(b[1], points)
            self.bases[newbase.team_color] = newbase
            if newbase.team_color == self.me.color:
                self.me.base = newbase

    def update_occgrid(self, tank_index):
        x, y, grid = self.messenger.occgrid(tank_index)
        return x, y, self.parse_occgrid_from_list(grid)

    def parse_occgrid_from_list(self, str_list):
        """
        The messenger will give the following:
        at 20,20
        size 5x4
        0110
        0111
        0111
        0001
        0100

        We will convert that into an array like this:
        [[00000]
         [11101]
         [11100]
         [01110]]

        :return array: an array like the one described above
        """
        result = []
        for line in str_list.split('\n'):
            result.append(list(line))
        # reflect on the tl-br diagonal
        rotated = [[0 for x in range(len(result))] for x in range(len(result[0]))]
        for row in range(0, len(result)):
            for col in range(0, len(result[0])):
                rotated[col][row] = float(result[row][col])

        return rotated

class Me:

    def __init__(self):
        pass


class Tank:

    def __init__(self, index, callsign, status, shots_available, time_to_reload, flag, x, y, angle, vx, vy, angvel,
                 messenger):
        self.index = int(index)
        self.callsign = callsign
        self.status = status
        self.shots_available = int(shots_available)
        self.time_to_reload = float(time_to_reload)
        self.flag = flag
        self.x = int(x)
        self.y = int(y)
        self.angle = float(angle)
        self.vx = float(vx)
        self.vy = float(vy)
        self.angvel = float(angvel)
        self.messenger = messenger

    def update(self, index, callsign, status, shots_available, time_to_reload, flag, x, y, angle, vx, vy, angvel):
        self.__init__(index, callsign, status, shots_available, time_to_reload, flag, x, y, angle, vx, vy, angvel)

    def shoot(self):
        self.messenger.shoot(self.index)

    def speed(self, speed):
        self.messenger.speed(self.index, speed)

    def set_angvel(self, angvel):
        self.messenger.angvel(self.index, angvel)

    def __repr__(self):
        return "tank %d, x %f, y %f, angle %f, angvel %f" % (self.index, self.x, self.y, self.angle, self.angvel)


class Obstacle:

    def __init__(self, points):
        self.points = points

    def get_radius(self):
        x = math.fabs((self.points[0][0] - self.points[1][0]) / 2)
        y = math.fabs((self.points[0][1] - self.points[1][1]) / 2)
        return math.sqrt(x**2 + y**2)

    def get_centerpoint(self):
        """For now, assumes that the base is a rectangle.
        """
        x = (self.points[0][0] + self.points[1][0]) / 2
        y = (self.points[0][1] + self.points[1][1]) / 2
        return {'x': x, 'y': y}


class Flag:
    def __init__(self, team_color, possessing_team_color, x, y):
        self.team_color = team_color
        self.possessing_team_color = possessing_team_color
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "Flag team color: %s, possessing_team_color: %s, x: %f, y:  %f" % (self.team_color,
                                                                                  self.possessing_team_color, self.x,
                                                                                  self.y)


class Base:

    def __init__(self, team_color, points):
        self.team_color = team_color
        self.points = points


    def get_centerpoint(self):
        """For now, assumes that the base is a rectangle.
        """
        x = (self.points[0][0] + self.points[1][0] + self.points[2][0] + self.points[3][0]) / 4
        y = (self.points[0][1] + self.points[1][1] + self.points[2][1] + self.points[3][1]) / 4
        return {'x': x, 'y': y}