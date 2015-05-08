from Tank import Tank
import logging

__author__ = 'ben'


class State:

    def __init__(self, messenger):
        self.messenger = messenger
        self.mytanks = {}

    def update_mytanks(self):
        # mytank [index] [callsign] [status] [shots available] [time to reload] [flag] [x] [y] [angle] [vx] [vy]
        # [angvel]
        data = self.messenger.mytanks()
        for mytank in data.split("\n"):
            t = mytank.split(" ")
            logging.debug("Tank: ")
            logging.debug(t)
            self.mytanks[t[1]] = Tank(t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10], t[11], t[12],
                                      self.messenger)
