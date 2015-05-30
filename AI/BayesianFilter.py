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

    # ONLY WORK ON THIS FUNCTION
    def bayesian_grid(self, visible_grid, x, y):
        """
        Runs visible_grid through a Bayesian filter and then updates self.model with the new information.
        :param visible_grid: a python 2d array of 0s and 1s. Size variable. Centered on the location specified by x, y.
                             This is a rectangle.
        :param x: the location of the UPPER LEFT CORNER of the array
        :param y: the location of the UPPER LEFT CORNER of the array
        :return None: No return value.
        """

        pass

    def test(self, visible_grid, x, y):
        self.assign_grid(visible_grid, x, y)

    def assign_grid(self, small_grid, x, y):
        for i in range (0, len(small_grid)):
            for j in range (0, len(small_grid[0])):
                if i + x < len(small_grid) and j + y < len(small_grid):
                    self.model[i+x][j+y] = small_grid[i][j]