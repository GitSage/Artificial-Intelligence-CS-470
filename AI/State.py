import logging

__author__ = 'ben'


class State:

    def __init__(self, messenger, me):
        self.messenger = messenger
        self.mytanks = {}
        self.obstacles = []
        self.flags = {}
        self.me = Me
        self.me.color = me

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
                points.append([o[i], o[i+1]])
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
        self.flag = (flag != "-")  # true if holding the flag, false if not
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


class Flag:
    def __init__(self, team_color, possessing_team_color, x, y):
        self.team_color = team_color
        self.possessing_team_color = possessing_team_color
        self.x = x
        self.y = y

    def __repr__(self):
        return "Flag team color: %s, possessing_team_color: %s, x: %f, y:  %f" %(self.team_color,
                                                                                 self.possessing_team_color, self.x,
                                                                                 self.y)
