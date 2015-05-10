# Runs an AI that will KICK YOUR BUTT.

import argparse
import logging
import threading
import subprocess
import time
from AI.Timer import Timer
from AI.Messenger import Messenger
from AI.State import State
from AI.PotentialFieldCalculator import *


LOG_FILENAME = 'log.log'
TIME_PER_SLEEP = 1
hello_var = 0
state = None
messenger = None
game = None


def main():
    global messenger, state, TIME_PER_SLEEP

    init_logging()
    # args = parse_args()

    start_game()
    port = ports[1]

    messenger = Messenger(port, 'localhost')
    state = State(messenger)
    init_state()
    timer = Timer(TIME_PER_SLEEP, state)

    # timer.add_task(timer.really_dumb_agent, state.mytanks['1'])
    # timer.add_task(timer.really_dumb_agent, state.mytanks['2'])

    # set up potential fields calculator
    timer.set_pfc(setup_potential_fields())
    timer.add_task(timer.potential_fields_move, '1')

    while 1:
        timer.tick()


def setup_potential_fields():
    global state
    attractive = repulsive = tangential = []

    # attractive. One flag that I chose at random.
    flag = state.flags[3]
    logging.info("Seeking flag %s", str(flag))
    attractive.append(AttractiveObject(x=flag.x, y=flag.y, radius=10, spread=1000000, alpha=1))

    return PotentialFieldCalculator(attractive, repulsive, tangential)


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
    ports = []
    for i in range(0, 4):
        line = proc.stdout.readline()
        ports.append(int(line.split(" ")[-1]))


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
