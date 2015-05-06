import logging
from BZSocket import BZSocket
import time


class Messenger:

    port = None
    host = None
    sock = None

    def __init__(self, port, host):
        self.port = port
        self.host = host
        self.sock = BZSocket(port=port, host=host)

    def shoot(self, tank):
        self.sock.send("shoot %d" % tank)

    def teams(self):
        self.sock.send("teams")

    def obstacles(self):
        self.sock.send("obstacles")