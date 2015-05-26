import logging
import re
import socket


class Messenger:

    def __init__(self, port, host):
        self.port = port
        self.host = host
        self.sock = BZSocket(port=port, host=host)
        logging.debug("Messenger created with parameters port=%d, host=%s")

    def shoot(self, tank):
        self.sock.send("shoot %d" % tank)

    def speed(self, tank, speed):
        self.sock.send("speed %d %f" % (tank, speed))

    def angvel(self, tank, angvel):
        self.sock.send("angvel %d %f" % (tank, angvel))

    def accelx(self, tank, accel):
        self.sock.send("accelx %d %f" % (tank, accel))

    def accely(self, tank, accel):
        self.sock.send("accely %d %f" % (tank, accel))

    def teams(self):
        self.sock.send("teams")

    def obstacles(self):
        msg = self.get_list_from_response(self.sock.send("obstacles"))
        return msg

    def bases(self):
        return self.get_list_from_response(self.sock.send("bases"))

    def flags(self):
        return self.get_list_from_response(self.sock.send("flags"))

    def shots(self):
        self.sock.send("shots")

    def mytanks(self):
        msg = self.get_list_from_response(self.sock.send("mytanks"))
        return msg

    def othertanks(self):
        self.sock.send("othertanks")

    def constants(self):
        self.sock.send("constants")

    def occgrid(self, tank):
        x, y, grid = self.parse_occgrid_response(self.sock.send("occgrid %s" % tank))
        return x, y, grid

    def get_list_from_response(self, msg):
        msg = msg[msg.index('\n')+1:]  # remove first line ("ack...")
        msg = msg[msg.index('\n')+1:]  # remove second line ("begin")
        msg = msg[:msg.rfind('\n')]  # remove last line ("\n")
        msg = msg[:msg.rfind('\n')]  # remove second to last line ("end")
        msg = re.sub(' +', ' ', msg).strip()  # reduce multiple spaces to a single space

        return msg

    def parse_occgrid_response(self, msg):
        """
        An example message looks like this:
        ack 0.258136987686 occgrid
        begin
        at -400,-35
        size 4x4
        0000
        0000
        0000
        0000
        end
        :param msg: the message from the server as above
        :return: x, y, grid, where x and y are the locations mentioned ("at -400, -35") and the grid is the list
                 following that.
        """
        msg = msg[msg.index('\n')+1:]  # remove first line ("ack...")
        msg = msg[msg.index('\n')+1:]  # remove second line ("begin")
        msg = msg[:msg.rfind('\n')]  # remove last line ("\n")
        msg = msg[:msg.rfind('\n')]  # remove second to last line ("end")
        x, y = ((msg.split("\n")[0]).split(" ")[1]).split(",")
        msg = msg[msg.index('\n')+1:]  # remove third line ("at -400,-35")
        msg = msg[msg.index('\n')+1:]  # remove fourth line ("size 4x4")

        return x, y, msg


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