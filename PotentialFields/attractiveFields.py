
__author__ = 'lexic92'

import matplotlib.pyplot as plt
import numpy
import math
from PotentialFields.model import Goal

class AttractiveFields():

    def _generateAttractiveFieldGraph(self):
        # CODE FROM WALTER'S EXAMPLE IN SIMPLE.PY (UNMODIFIED, except for some parameters Ben might have modified)
        fig = plt.figure()
        ax = fig.add_subplot(111)

        #generate grid
        x = numpy.linspace(-2, 2, 24)
        y = numpy.linspace(-1.5, 1.5, 24)
        x, y = numpy.meshgrid(x, y)

        #--------------------------MY CODE----------------------------
        #To fix a bug (See http://stackoverflow.com/questions/13730468/from-2d-to-1d-arrays)
        x = numpy.reshape(x, (1,numpy.product(x.shape)))[0]
        y = numpy.reshape(y, (1,numpy.product(y.shape)))[0]

        #initialize vectors (actually just lists)
        vx = []
        vy = []

        #Loop from 0 to x.length-1, therefore running x.length times:
        for i in range(0, x.size):
            sum_vx = 0 #Add all of the attractive fields and sum them up for each given position
            sum_vy = 0 #Add all of the attractive fields and sum them up for each given position

            for goal in self._goals:
                #calculate distance to goal
                d = goal.getDistanceTo(x[i], y[i])
                r = goal._radius
                s = goal._spread
                theta = goal.getAngleToGoalFrom(x[i], y[i])

                #FOLLOWING FORMULA FROM Potential Fields PDF ON LEARNING SUITE CONTENT TAB
                if d < r:
                    sum_vx += 0
                    sum_vy += 0
                elif d <= (r + s):
                    sum_vx += (self._alpha*(d - r)*math.cos(theta))
                    sum_vy += (self._alpha*(d - r)*math.sin(theta))
                elif d > (r + s):
                    sum_vx += (self._alpha*s*math.cos(theta))
                    sum_vy += (self._alpha*s*math.sin(theta))

            vx.append(sum_vx)
            vy.append(sum_vy)
        #------------------------------------------------------------

        # CODE FROM WALTER'S EXAMPLE IN SIMPLE.PY (UNMODIFIED, except for the filename it is saved as.)
        ax.quiver(x, y ,vx, vy, pivot='middle', color='r', headwidth=4, headlength=6)
        ax.set_xlabel('$x$') # $ cosmetically changes how the x looks
        ax.set_ylabel('$y$')
        ax.axis('image')
        plt.savefig(self._FILE_NAME)
        plt.show()

    #--------------------------MY CODE----------------------------
    def __init__(self, goals):
        #Initialize variables first!
        self._FILE_NAME = 'attractive_fields.png' #File name to save the figure as.
        self._goals = goals #List of "Goal" objects to make an attractive field of.
        self._alpha = 1 #For scaling the vx and vy values.

        #do stuff
        self._generateAttractiveFieldGraph()
    #------------------------------------------------------------



if __name__ == "__main__":
    #TEST CASE runs when this file is run individually.
    goals = []
    goals.append(Goal.Goal(0, 0, 1, 2))
    AttractiveFields(goals)