# Runs an AI that will KICK YOUR BUTT.

import argparse
import threading
import subprocess
import time
from AI.Messenger import Messenger
from AI.State import State
from AI.Agents import *


PLAYER = 'red'
LOG_FILENAME = 'log.log'
TIME_PER_SLEEP = .1
hello_var = 0
state = None
messenger = None
game = None


def main():
    global messenger, state, TIME_PER_SLEEP, PLAYER

    init_logging()
    args = parse_args()

    if args.port:
        port = args.port
    else:
        start_game()
        port = ports[PLAYER]

    messenger = Messenger(port, 'localhost')
    state = State(messenger, PLAYER)
    timer = Timer(TIME_PER_SLEEP)

    # assign agents to tanks
    # ReallyDumbAgent('0', state)
    # ReallyDumbAgent('1', state)
    # ReallyDumbAgent('2', state)
    # ReallyDumbAgent('3', state)
    # ReallyDumbAgent('4', state)
    # ReallyDumbAgent('5', state)
    # ReallyDumbAgent('6', state)
    # ReallyDumbAgent('7', state)
    # ReallyDumbAgent('8', state)

    PDFlagRetriever('0', 'blue', state)
    PDFlagRetriever('1', 'blue', state)
    PDFlagRetriever('2', 'blue', state)
    PDFlagRetriever('3', 'blue', state)
    PDFlagRetriever('4', 'blue', state)
    PDFlagRetriever('5', 'blue', state)
    PDFlagRetriever('6', 'blue', state)
    PDFlagRetriever('7', 'blue', state)
    PDFlagRetriever('8', 'blue', state)
    PDFlagRetriever('9', 'blue', state)

    while 1:
        timer.tick()


def parse_args():

    # analyze arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p',
                        '--port',
                        type=int,
                        help='port',
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
    proc = subprocess.Popen(["python", "bin/bzrflag"], stdout=subprocess.PIPE)
    ports = {}
    for i in range(0, 4):
        line = proc.stdout.readline().split(" ")
        ports[line[2][:-1]] = int(line[-1])
    print ports


def init_logging():
    logging.basicConfig(level=logging.INFO)
    logging.StreamHandler().setLevel(logging.INFO)
    logging.FileHandler(LOG_FILENAME).setLevel(logging.INFO)
    logging.debug('Starting main.')


if __name__ == '__main__':
    main()
