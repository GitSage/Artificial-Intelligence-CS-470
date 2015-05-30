__author__ = 'byocum'

class BayesianFilter:

    def __init__(self, width, height):
        """
        Initializes the filter with an array of size (width,height).
        :param width:
        :param height:
        :return:
        """
        # this is an array of probabilities. Initially equal to 0.5.
        self.model = [[0.5 for x in range(height)] for x in range(width)]
        #TODO: Make True_negative and true_positive parameters!
        self.true_negative = 0.9
        self.true_positive = 0.97
        self.false_negative = 1.0 - self.true_positive
        self.false_positive = 1.0 - self.true_negative

    # ONLY WORK ON THIS FUNCTION

    def changeToInts(self, visible_grid):
        for i in range(len(visible_grid)):
            for j in range(len(visible_grid[i])):
                visible_grid[i][j]=float(visible_grid[i][j])


    def bayesian_grid(self, visible_grid, x, y):
        """
        Runs visible_grid through a Bayesian filter and then updates self.model with the new information.
        :param visible_grid: a python 2d array of 0s and 1s. Size variable. UPPER LEFT CORNER / BOTTOM LEFT CORNER of the world is x, y.
                    The bottom-left corner of the world is 0,0. The upper-right corner is lenx,leny.
                             This is a rectangle.
        :param x: the location of the UPPER LEFT CORNER of the array / BOTTOM LEFT CORNER of the world
        :param y: the location of the UPPER LEFT CORNER of the array / BOTTOM LEFT CORNER of the world
        :return None: No return value.
        """
        #self.changeToInts(visible_grid)



        for row in range (0, len(visible_grid)):
            for col in range (0, len(visible_grid[row])):
                modelRow = row + 400 + y
                modelCol = col + 400 + x
                if((modelRow < 800) and (modelRow >= 0) and (modelCol < 800) and (modelCol >= 0)):
                    self.model[modelRow][modelCol] = 1.0 - self.updateBayes(observation=visible_grid[row][col],
                                                                            prior=1.0 -self.model[modelRow][modelCol])


    def updateBayes(self, observation, prior):
        '''
        :param observation 1 if occupied, 0 if unoccupied.
        :param prior your prior belief, a float ranging from 0 to 1. 0 corresponds to belief that it is unoccupied, and 1 corresponds to "occupied".
        '''
        false_prior = 1.0 - prior
        #IF OBSERVATON EQUALS UNOCCUPIED:
        if observation == 0:
            alpha = 1.0/((self.true_negative * false_prior) + (self.false_negative * prior))
            new_prior = self.false_negative * prior * alpha
            return new_prior
        elif observation == 1:
            alpha = 1.0/((self.false_positive * false_prior) + (self.true_positive * prior))
            new_prior = self.true_positive * prior * alpha
            return new_prior

    def test(self, visible_grid, x, y):
        for row in range (0, len(visible_grid)):
            for col in range (0, len(visible_grid[row])):
                modelRow = row + 400 + y
                modelCol = col + 400 + x
                if((modelRow < 800) and (modelRow >= 0) and (modelCol < 800) and (modelCol >= 0)):
                    self.model[modelRow][modelCol] = 1.0 - visible_grid[row][col]


if __name__ == "__main__":
    bf = BayesianFilter(800,800)
    print "Result1: " + str(bf.updateBayes(0, 0.63))
    print "Result2: " + str(bf.updateBayes(1, 0.72))