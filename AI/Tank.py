

class Tank:

    def __init__(self, index, callsign, status, shots_available, time_to_reload, flag, x, y, angle, vx, vy, angvel):
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

    def update(self, index, callsign, status, shots_available, time_to_reload, flag, x, y, angle, vx, vy, angvel):
        self.__init__(index, callsign, status, shots_available, time_to_reload, flag, x, y, angle, vx, vy, angvel)

    def __repr__(self):
        return "tank"