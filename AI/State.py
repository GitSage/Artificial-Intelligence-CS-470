from Tank import Tank
import logging

__author__ = 'ben'


class State:

    def __init__(self):
        self.mytanks = []

    def init_mytanks(self, data):
        # mytank [index] [callsign] [status] [shots available] [time to reload] [flag] [x] [y] [angle] [vx] [vy]
        # [angvel]
        for mytank in data.split("\n"):
            t = mytank.split(" ")
            logging.debug(t)
            self.mytanks.append(Tank(t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10], t[11], t[12]))

    def update_mytanks(self, data):
        if len(self.mytanks) == 0:
            self.init_mytanks(data)
        else:
            i = 0
            for mytank in data.split("\n"):
                t = mytank.split(" ")
                self.mytanks[i] = Tank(t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10], t[11], t[12])
