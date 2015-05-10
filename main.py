# Runs an AI that will KICK YOUR BUTT.

import argparse
import threading
import subprocess
import time
from AI.Messenger import Messenger
from AI.State import State
from AI.Agents import *


PLAYER = 'blue'
LOG_FILENAME = 'log.log'
TIME_PER_SLEEP = .25
hello_var = 0
state = None
messenger = None
game = None


def main():
    global messenger, state, TIME_PER_SLEEP, PLAYER

    init_logging()
    # args = parse_args()

    start_game()
    port = ports['blue']

    messenger = Messenger(port, 'localhost')
    state = State(messenger, PLAYER)
    init_state()
    timer = Timer(TIME_PER_SLEEP)

    # assign agents to tanks
    ReallyDumbAgent('0', state)
    PDFlagRetriever('1', 'red', state)
    PDFlagRetriever('2', 'red', state)
    PDFlagRetriever('3', 'red', state)
    PDFlagRetriever('4', 'purple', state)
    PDFlagRetriever('5', 'purple', state)
    PDFlagRetriever('6', 'purple', state)
    PDFlagRetriever('7', 'green', state)
    PDFlagRetriever('8', 'green', state)
    PDFlagRetriever('9', 'green', state)

    while 1:
        timer.tick()


def parse_args():

    # analyze arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--spread-out',
                        action='store_true',
                        help='Causes your army to spread out before anything else.',
                        required=False)
    parser.add_argument('-p',
                        '--port',
                        type=int,
                        help='port',
                        required=True)
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
    proc = subprocess.Popen(["python", "bin/bzrflag"], stdout=subprocess.PIPE)
    ports = {}
    for i in range(0, 4):
        line = proc.stdout.readline().split(" ")
        ports[line[2][:-1]] = int(line[-1])
    print ports


def init_state():
    global state
    logging.debug("Initializing state.")
    state.update_mytanks()
    state.update_obstacles()
    state.update_flags()
    logging.debug("state: " + str(state))


def init_logging():
    logging.basicConfig(level=logging.INFO)
    logging.StreamHandler().setLevel(logging.INFO)
    logging.FileHandler(LOG_FILENAME).setLevel(logging.INFO)
    logging.debug('Starting main.')


if __name__ == '__main__':
    main()
