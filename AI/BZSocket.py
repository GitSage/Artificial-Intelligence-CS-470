import socket
import logging
__author__ = 'ben'


class BZSocket:

    port = None
    host = None
    sock = None

    def __init__(self, port=None, host=None):
        self.port = port
        self.host = host

        # connect socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.handshake()

    def handshake(self):
        response = self.rec_line()
        if response == "bzrobots 1\n":
            self.send_no_response('agent 1')
        elif response == "bzrobots 2\n":
            self.send_no_response('agent 2')
        elif response == "bzrobots 3\n":
            self.send_no_response('agent 3')
        elif response == "bzrobots 4\n":
            self.send_no_response('agent 4')
        else:
            logging.critical('PROBLEM in connection handshake! Received response: %s', response)
            return

        logging.debug('Handshake successful.')

    def rec(self):
        msg = ''
        msg += self.rec_line()  # receive acknowledgement line
        msg2 = self.rec_line()  # receive message

        # get list
        if msg2 == "begin\n":
            while 'end' not in msg2:
                msg2 += self.rec_line()

        msg += msg2

        logging.debug("RECEIVED MESSAGE: %s" % msg)
        return msg

    def rec_line(self):
        msg = ''
        while '\n' not in msg:
            msg += self.sock.recv(1)
        return msg

    def send(self, msg):
        self.send_no_response(msg)
        return self.rec()

    def send_no_response(self, msg):
        logging.debug("SENDING MESSAGE: %s" % msg)
        self.sock.send(msg + "\n")