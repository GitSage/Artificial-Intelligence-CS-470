# Runs an AI that will KICK YOUR BUTT.

import argparse
import threading
import subprocess
import time
from AI.Messenger import Messenger
from AI.State import State
from AI.Agents import *
from AI.BayesianGridVisualizer import BayesianGridVisualizer
from AI.BayesianFilter import BayesianFilter

PLAYER = 'red'
LOG_FILENAME = 'log.log'
TIME_PER_TICK = 0.1
hello_var = 0
state = None
messenger = None
game = None
true_positive = 0.9
true_negative = 0.9

def main():
    global messenger, state, TIME_PER_TICK, PLAYER

    init_logging()
    args = parse_args()

    # if no port specified, start a game and connect to it.
    if args.port is None or args.port is "":
        start_game()
        port = ports[PLAYER]
    else:
        port = args.port

    # connect to the server and set up global variables
    messenger = Messenger(port, 'localhost')
    state = State(messenger, PLAYER)
    timer = Timer(TIME_PER_TICK)

    # run lab 2
    if args.bayesian_filter is True:
        bay_vis = BayesianGridVisualizer()
        bay_vis.init_window(800, 800)
        bay_filter = BayesianFilter(800, 800, true_positive, true_negative)
        #bay_filter = BayesianFilter(800, 800, 0.6, 0.6)
        BayesianGridSearchAgent('0', bay_vis, bay_filter, state)
        BayesianGridSearchAgent('1', bay_vis, bay_filter, state)
        BayesianGridSearchAgent('2', bay_vis, bay_filter, state)
        BayesianGridSearchAgent('3', bay_vis, bay_filter, state)
        BayesianGridSearchAgent('4', bay_vis, bay_filter, state)
        #BayesianGridSearchAgent('5', bay_vis, bay_filter, state)
        #BayesianGridSearchAgent('6', bay_vis, bay_filter, state)
        #BayesianGridSearchAgent('7', bay_vis, bay_filter, state)
        #BayesianGridSearchAgent('8', bay_vis, bay_filter, state)
        #BayesianGridSearchAgent('9', bay_vis, bay_filter, state)
    # assign agents to tanks
    # ReallyDumbAgent('0', state)
    # BayesianGridSearchAgent('1', bay_vis, bay_filter, state)
    # BayesianGridSearchAgent('2', state)
    # BayesianGridSearchAgent('3', state)
    # PDFlagRetriever('4', 'purple', state)
    # PDFlagRetriever('5', 'purple', state)
    # PDFlagRetriever('6', 'purple', state)
    # PDFlagRetriever('7', 'green', state)
    # PDFlagRetriever('8', 'green', state)
    # PDFlagRetriever('9', 'green', state)

    while 1:
        timer.tick()


def parse_args():

    # analyze arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        help='The host of the server.',
                        required=False)
    parser.add_argument('-p',
                        '--port',
                        type=int,
                        help='The port of the server.',
                        required=False)
    parser.add_argument('--bayesian-filter',
                        action='store_true',
                        help='Run the Bayesian Filter lab (lab 2).',
                        required=False)
    args = parser.parse_args()
    logging.debug("Arguments: %s", args)
    return args


def start_game():
    global game
    game = threading.Thread(target=t_start_game)
    game.daemon = True
    game.start()
    time.sleep(2)


def t_start_game():
    global ports
    print str(true_positive)
    print str(true_negative)
    proc = subprocess.Popen(["python", "bin/bzrflag", "--default-true-positive=" + str(true_positive), "--default-true-negative=" + str(true_negative),
                             "--occgrid-width=100", "--no-report-obstacles"], stdout=subprocess.PIPE)
    ports = {}
    for i in range(0, 4):
        line = proc.stdout.readline().split(" ")
        print line

        ports[line[2][:-1]] = int(line[-1])
    print ports


def init_logging():
    logging.basicConfig(level=logging.INFO)
    logging.StreamHandler().setLevel(logging.INFO)
    logging.FileHandler(LOG_FILENAME).setLevel(logging.INFO)
    logging.debug('Starting main.')


if __name__ == '__main__':
    main()
