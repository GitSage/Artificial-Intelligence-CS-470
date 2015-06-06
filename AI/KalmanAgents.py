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

class KalmanAgent(Agents.Agent):
    pass

class StationaryAgent(KalmanAgent):
    pass

class MovingAgent(KalmanAgent):
    pass

class RandomAgent(KalmanAgent):
    pass

class KalmanVisualizer:

    def draw_circle(self):
        pos = self.coord
        radius = self.radius
        color = (0, 0, 0)
        alpha = 255.0
        """Draw a circle <- return None
        """
        w, x, y = color
        w = w / 255.0 if w else 0
        x = x / 255.0 if x else 0
        y = y / 255.0 if y else 0
        z = alpha / 255.0 if alpha else 0
        glDisable(GL_TEXTURE_2D)

        c = gluNewQuadric()
        glColor4f(w, x, y, z)
        glPushMatrix()
        glTranslatef(pos[0], pos[1], 0)
        gluDisk(c, 0.5, radius, 100, 100)
        glPopMatrix()
        glEnable(GL_TEXTURE_2D)
        glFlush()
        glutSwapBuffers()

    def draw_grid(self):
        # This assumes you are using a numpy array for your grid

        width, height = self._grid.shape
        glRasterPos2f(-1, -1)
        glDrawPixels(width, height, GL_LUMINANCE, GL_FLOAT, self._grid)
        glFlush()
        glutSwapBuffers()

    def update_and_draw_circle(self, new_grid):
        """
        Overwrites current grid with this grid, and saves this grid in the class variables.
        :param new_grid: a numpy array containing the grayscale values to graph.
        """
        self.draw_grid()

    def init_window(self, width, height):
        glutInit(())
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        glutInitWindowPosition(0, 0)
        self._window = glutCreateWindow("Kalman Filter")
        glutDisplayFunc(self.draw_circle)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glutMainLoop()

    def __init__(self):
        '''
        This class is the same as the sample code, except that I changed the global variables to class member variables
         and I added the "update_and_draw_grid" method.
        '''
        self._window = None
        self.radius = 100
        self.coord = (0, 0)

if __name__ == "__main__":
    vis = KalmanVisualizer()
    vis.init_window(800, 800)
    vis.draw_circle()
    while 1:
        pass
