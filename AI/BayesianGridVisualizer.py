__author__ = 'lexic92'

#!/usr/bin/env python

import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from numpy import zeros
import numpy
import time

class BayesianGridVisualizer():
    def draw_grid(self):
        # This assumes you are using a numpy array for your grid
        width, height = self._grid.shape
        glRasterPos2f(-1, -1)
        glDrawPixels(width, height, GL_LUMINANCE, GL_FLOAT, self._grid)
        glFlush()
        glutSwapBuffers()

    def update_grid(self, new_grid):
        self._grid = numpy.array(new_grid)

    def update_and_draw_grid(self, new_grid):
        """
        Overwrites current grid with this grid, and saves this grid in the class variables.
        :param new_grid: a numpy array containing the grayscale values to graph.
        """
        self.update_grid(new_grid)
        self.draw_grid()

    def init_window(self, width, height):
        self._grid = zeros((width, height))
        glutInit(())
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        glutInitWindowPosition(0, 0)
        self._window = glutCreateWindow("Grid filter")
        glutDisplayFunc(self.draw_grid)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        #glutMainLoop()

    def __init__(self):
        '''
        This class is the same as the sample code, except that I changed the global variables to class member variables
         and I added the "update_and_draw_grid" method.
        '''
        self._grid = None
        self._window = None


def Test():
    # grid characteristics
    mapMinX = -400
    mapMinY = -400
    mapMaxX = 400
    mapMaxY = 400
    stepX = 40
    stepY = 40
    windowWidth = 800
    windowHeight = 800

    # generate grid
    a = [ ]
    allZeroes = []
    allOnes = []

    for i in range(0,800):
        allZeroes.append(0)
        allOnes.append(1)
   # for i in range(0, 50):
     #   allZeroes[i] = 1
    for i in range(0, 400):
        a.append(allZeroes)
    for i in range(0,400):
        a.append(allOnes)


    array = numpy.array(a)
    array = numpy.flipud(array)

    #array = numpy.zeros((800, 800))
    # array.fill(0)

    b = BayesianGridVisualizer()
    b.init_window(windowWidth, windowHeight)
    b.update_and_draw_grid(array)

    time.sleep(5)

    array = numpy.flipud(array)
    b.update_and_draw_grid(array)


if __name__ == "__main__":
    #TEST CASE runs when this file is run individually.
    Test()
    while 1:
        pass