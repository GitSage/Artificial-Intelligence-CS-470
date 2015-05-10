

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