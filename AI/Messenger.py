import logging, re
from BZSocket import BZSocket


class Messenger:

    def __init__(self, port, host, state):
        self.port = port
        self.host = host
        self.sock = BZSocket(port=port, host=host)
        self.state = state
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
        self.sock.send("obstacles")

    def bases(self):
        self.sock.send("bases")

    def flag(self):
        self.sock.send("flags")

    def shots(self):
        self.sock.send("shots")

    def mytanks(self):
        msg = self.get_list_from_response(self.sock.send("mytanks"))
        self.state.update_mytanks(msg)

    def othertanks(self):
        self.sock.send("othertanks")

    def constants(self):
        self.sock.send("constants")

    def occgrid(self, tank):
        self.sock.send("occgrid %d" % tank)

    def get_list_from_response(self, msg):
        msg = msg[msg.index('\n')+1:]  # remove first line ("ack...")
        msg = msg[msg.index('\n')+1:]  # remove second line ("begin")
        msg = msg[:msg.rfind('\n')]  # remove last line ("\n")
        msg = msg[:msg.rfind('\n')]  # remove second to last line ("end")
        msg = re.sub(' +', ' ', msg).strip()  # reduce multiple spaces to a single space

        return msg