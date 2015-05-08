# Runs an AI that will KICK YOUR BUTT.

import argparse
import logging
from Timer import Timer
from Messenger import Messenger
from State import State

LOG_FILENAME = 'log.log'
TIME_PER_SLEEP = 1
hello_var = 0
state = None
messenger = None


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


def main():
    global messenger, state, TIME_PER_SLEEP

    init_logging()
    args = parse_args()

    timer = Timer(TIME_PER_SLEEP)
    messenger = Messenger(args.port, 'localhost')
    state = State(messenger)
    init_state()

    timer.add_task(timer.really_dumb_agent, state.mytanks['1'])
    timer.add_task(timer.really_dumb_agent, state.mytanks['2'])

    while 1:
        timer.tick()


def init_state():
    global state
    logging.debug("Initializing state.")
    state.update_mytanks()
    logging.debug("mytanks: " + str(state.mytanks))

    messenger.bases()

def init_logging():
    logging.basicConfig(level=logging.DEBUG, )
    logging.StreamHandler().setLevel(logging.DEBUG)
    logging.FileHandler(LOG_FILENAME).setLevel(logging.DEBUG)
    logging.debug('Starting main.')

if __name__ == '__main__':
    main()
