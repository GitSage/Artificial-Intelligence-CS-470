# Runs an AI that will KICK YOUR BUTT.

import argparse
import logging
from Messenger import Messenger
from State import State
import time

LOG_FILENAME = 'log.log'

messenger = None
state = State()


def main():
    global messenger, state

    # set up logging
    logging.basicConfig(level=logging.DEBUG,)
    logging.StreamHandler().setLevel(logging.DEBUG)
    logging.FileHandler(LOG_FILENAME).setLevel(logging.DEBUG)

    logging.debug('Starting main.')

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

    messenger = Messenger(port=args.port, host='localhost', state=state)
    init_state()

    # timer
    TIME_PER_SLEEP = 1
    elapsed = 0
    go_timer = 0
    shoot_timer = 0
    turn_timer = 0
    TANK = 8


    while 1:
        if go_timer == 0:
            messenger.speed(TANK, 1)

        if go_timer == 3:
            messenger.speed(TANK, 0)

        if go_timer == 6:
            go_timer = -1

        if turn_timer == 5:
            messenger.angvel(TANK, 1)

        if turn_timer == 7:
            messenger.angvel(TANK, 0)
            turn_timer = 0

        if shoot_timer == 0:
            pass



        time.sleep(TIME_PER_SLEEP)
        go_timer += TIME_PER_SLEEP
        turn_timer += TIME_PER_SLEEP



def init_state():
    global messenger, state
    logging.debug("Initializing state.")

    messenger.mytanks()
    logging.debug("mytanks: " + str(state.mytanks))

    messenger.bases()

def really_dumb_agent():
    messenger.speed(1, 0)




if __name__ == '__main__':
    main()
