__author__ = 'ben'

import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import zeros
import numpy
import time
import Agents

class ClayPigeonAgent(Agents.Agent):
    pass

class StationaryClayPigeon(ClayPigeonAgent):
    pass

class ConstantVelocityClayPigeon(ClayPigeonAgent):
    pass

class NonConformingClayPigeon(ClayPigeonAgent):
    pass

class KalmanAgent(Agents.Agent):
    pass

class KalmanVisualizer:
    pass

if __name__ == "__main__":
    vis = KalmanVisualizer()
    vis.init_window(800, 800)
    vis.draw_circle()
    while 1:
        pass
