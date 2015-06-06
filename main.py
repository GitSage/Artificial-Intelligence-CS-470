# Runs an AI that will KICK YOUR BUTT.

import argparse
import threading
import subprocess
from AI.Messenger import Messenger
from AI.State import State
from AI.Agents import *
from AI.BayesianGridVisualizer import BayesianGridVisualizer
from AI.BayesianFilter import BayesianFilter
from AI.KalmanAgents import *

PLAYER = 'red'
LOG_FILENAME = 'log.log'
TIME_PER_TICK = 0.1
hello_var = 0
state = None
messenger = None
game = None

game_args = ["python", "bin/bzrflag"]  # default is to run the binary with default settings

def main():
    global messenger, state, TIME_PER_TICK, PLAYER, game_args

    init_logging()
    args = parse_args()

    enemy_port = None
    enemy_player = 'blue'

    # if no port specified, start a game and connect to it.
    if args.port is None or args.port is "":
        if args.bayesian_filter is True:
            true_positive = 0.9
            true_negative = 0.9
            game_args = ["python", "bin/bzrflag", "--default-true-positive=" + str(true_positive),
                         "--default-true-negative=" + str(true_negative), "--occgrid-width=100",
                         "--no-report-obstacles"]
        elif args.kalman_filter is True:
            game_args = ["python", "bin/bzrflag", "--default-posnoise=5", "--red-tanks=1", "--blue-tanks=1",
                         "--green-tanks=1", "--purple-tanks=1", "--no-report-obstacles"]

        start_game()
        port = ports[PLAYER]
        enemy_port = ports[enemy_player]
    else:
        port = args.port
        enemy_port = args.enemy_port

    # connect to the server and set up global variables
    messenger = Messenger(port, 'localhost')
    state = State(messenger, PLAYER)
    timer = Timer(TIME_PER_TICK)

    # run lab 2
    if args.bayesian_filter is True:

        bay_vis = BayesianGridVisualizer()
        bay_vis.init_window(800, 800)
        bay_filter = BayesianFilter(800, 800, true_positive, true_negative)
        # bay_filter = BayesianFilter(800, 800, 0.6, 0.6)
        BayesianGridSearchAgent('0', bay_vis, bay_filter, state)
        BayesianGridSearchAgent('1', bay_vis, bay_filter, state)
        BayesianGridSearchAgent('2', bay_vis, bay_filter, state)
        BayesianGridSearchAgent('3', bay_vis, bay_filter, state)
        BayesianGridSearchAgent('4', bay_vis, bay_filter, state)
        BayesianGridSearchAgent('5', bay_vis, bay_filter, state)
        BayesianGridSearchAgent('6', bay_vis, bay_filter, state)
        BayesianGridSearchAgent('7', bay_vis, bay_filter, state)
        BayesianGridSearchAgent('8', bay_vis, bay_filter, state)
        BayesianGridSearchAgent('9', bay_vis, bay_filter, state)

    # run lab 3
    elif args.kalman_filter is True:
        # set up enemy, including port, messenger, and state
        enemy_messenger = Messenger(enemy_port, 'localhost')
        enemy_state = State(enemy_messenger, 'blue')

        game_args = ["python", "bin/bzrflag", "--default-posnoise=5", "--[red]-tanks=1", "--[blue]-tanks=1",
                     "--[green]-tanks=1", "--[purple]-tanks=1", "--no-report-obstacles"]
        StationaryClayPigeon('0', enemy_state)

    # no lab was specified
    else:
        pass
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
    parser.add_argument('-e',
                        '--enemy-port',
                        type=int,
                        help='The port of the enemy.',
                        required=False)
    parser.add_argument('--bayesian-filter',
                        action='store_true',
                        help='Run the Bayesian Filter lab (lab 2).',
                        required=False)
    parser.add_argument('--kalman-filter',
                        action='store_true',
                        help='Run the Kalman Filter lab (lab 2).',
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
    global ports, game_args
    proc = subprocess.Popen(game_args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
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
