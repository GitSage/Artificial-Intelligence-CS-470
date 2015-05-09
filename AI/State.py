from Tank import Tank
from Flag import Flag
from Obstacle import Obstacle
import logging

__author__ = 'ben'


class State:

    def __init__(self, messenger):
        self.messenger = messenger
        self.mytanks = {}
        self.obstacles = []
        self.flags = []

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
        self.flags = []
        data = self.messenger.obstacles()
        for flag in data.split("\n"):
            f = flag.split(" ")
            self.flags.append(Flag(f[1], f[2], f[3], f[4]))