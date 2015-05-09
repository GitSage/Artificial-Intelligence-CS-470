__author__ = 'byocum'
import sys
import math


class PotentialFieldCalculator:

    def __init__(self, attractive, repulsive, tangential):
        self.attractive = attractive
        self.repulsive = repulsive
        self.tangential = tangential
        self.DEFAULT_VEC = [0, 0]
        self.ATTR_RANGE = sys.maxint
        self.REP_RANGE = sys.maxint
        self.TANG_RANGE = sys.maxint

    def update(self, attractive, repulsive, tangential):
        self.attractive = attractive
        self.repulsive = repulsive
        self.tangential = tangential

    def get_next_dir(self, x, y):
        vec = self.calc(x, y)
        self.pd_get_dir(vec)

    def calc(self, x, y):
        vec = self.DEFAULT_VEC
        self.add_vec(vec, self.attractive_vec(x, y))
        self.add_vec(vec, self.repulsive_vec(x, y))
        self.add_vec(vec, self.tangential_vec(x, y))
        return vec

    def attractive_vec(self, x, y):
        result_vec = self.DEFAULT_VEC  # vector that will contain the cumulative effect of all tangential fields

        # calculate cumulative effect of all tangential fields
        for obj in self.attractive:
            self.add_vec(result_vec, obj.get_vec(x, y))
        return result_vec

    def repulsive_vec(self, x, y):
        pass

    def tangential_vec(self, x, y):
        result_vec = self.DEFAULT_VEC  # vector that will contain the cumulative effect of all tangential fields

        # calculate cumulative effect of all tangential fields
        for obj in self.tangential:
            self.add_vec(result_vec, obj.get_vec(x, y))

        return result_vec

    def add_vec(self, vec1, vec2):
        for i in range(0, len(vec1)):
            vec1[i] += vec2[i]

    def pd_get_next_action(self, vec):
        pass


class PotentialFieldObject:

    def __init__(self, x, y, radius, spread, alpha):
        self.x = x  # the x-coordinate of the center of the goal object.
        self.y = y  # the y-coordinate of the center of the goal object.
        self.r = radius
        self.s = spread
        self.a = alpha

    def dist(self, x, y):
        return math.sqrt((x - self._x)**2 + (y - self._y)**2)

    def ang(self, x, y):
        return math.arctan2(self._y - y, self._x - x)


class AttractiveObject(PotentialFieldObject):

    def get_vec(self, x, y):
        ang = self.ang(x, self.x, y, self.y)
        d = self.dist(x, self.x, y, self.y)

        # If the agent is already on the goal, no effect
        if d < self.r:
            return [0, 0]

        # If the agent is outside the goal but inside the spread, calculate the effect
        elif self.r <= d <= self.s + self.r:
            xval = self.a * (d - self.r) * math.cos(ang)
            yval = self.a * (d - self.r) * math.sin(ang)
            return [xval, yval]

        # If the agent is outside the spread, calculate the effect
        else:
            xval = self.a * self.s * math.cos(ang)
            yval = self.a * self.s * math.sin(ang)
            return [xval, yval]


class RepulsiveObject(PotentialFieldObject):

    def get_vec(self, x, y):
        ang = self.ang(x, self.x, y, self.y)
        d = self.dist(x, self.x, y, self.y)

        # If the agent is inside the repulsive object, push away infinitely hard
        if d < self.r:
            xval = (-self.sign(math.cos(ang))*float('inf'))  # TODO: these look wrong
            yval = (-self.sign(math.sin(ang))*float('inf'))  # TODO: these look wrong
            return [xval, yval]

        # If the agent is outside the repulsive object but inside the spread, calculate the effect
        elif self.r <= d <= self.s + self.r:
            xval = self.a * (self.s + self.r - d) * math.cos(ang)
            yval = self.a * (self.s + self.r - d) * math.sin(ang)
            return [xval, yval]

        # If the agent is outside the spread, no effect
        else:
            return [0, 0]


class TangentialObject(PotentialFieldObject):

    def get_vec(self, x, y):
        ang = self.ang(x, self.x, y, self.y)
        d = self.dist(x, self.x, y, self.y)

        # TODO all of these
        # If the agent is already on the goal, push away infinitely hard
        if d < self.r:
            return [sys.maxint, sys.maxint]

        # If the agent is outside the goal but inside the spread, calculate the effect
        elif self.r <= d <= self.s + self.r:
            xval = self.a * (self.s + self.r - d) * math.cos(ang)
            yval = self.a * (self.s + self.r - d) * math.sin(ang)
            return [xval, yval]

        # If the agent is outside the spread, no effect
        else:
            return [0, 0]
