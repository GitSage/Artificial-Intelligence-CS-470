__author__ = 'byocum'

class BayesianFilter:

    def __init__(self, model):
        self.model = model  # this is an array of probabilities. Initially equal to 0.5, 0.5.

    def parse_occgrid_from_list(self):
        """
        The messenger will give the following:
        at 20,20
        size 5x4
        0110
        0111
        0111
        0001
        0100

        We will convert that into an array like this:
        [[00000]
         [11101]
         [11100]
         [01110]]

        :return array: an array like the one described above
        """

        pass

    # ONLY WORK ON THIS FUNCTION
    def bayesian_grid(visible_grid, x, y):
        """
        Runs visible_grid through a Bayesian filter and then updates self.model with the new information.
        :param visible_grid: a python 2d array of 0s and 1s. Size variable. Centered on the location specified by x, y.
                             This is a rectangle.
        :param x: the location of the UPPER LEFT CORNER of the array
        :param y: the location of the UPPER LEFT CORNER of the array
        :return None: No return value.
        """

        pass
