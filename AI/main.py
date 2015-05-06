# Runs an AI that will KICK YOUR BUTT.

import argparse
import logging
from Messenger import Messenger

LOG_FILENAME = 'log.log'


def main():
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

    messenger = Messenger(port=args.port, host='localhost')
    messenger.shoot(1)
    messenger.obstacles()

if __name__ == '__main__':
    main()
