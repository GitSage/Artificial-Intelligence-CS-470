from Timer import Timer
from PotentialFieldCalculator import *
from PDController import PDController

class Agent:

    def __init__(self, tank_index, state):
        self.tank_index = tank_index
        self.state = state

    pass


class ReallyDumbAgent(Agent):

    def __init__(self, tank_index, state):
        self.tank_index = tank_index
        self.state = state
        self.timer_id = Timer.add_task(self.really_dumb_agent)
        self.count = 0

    def really_dumb_agent(self):
        """Performs the same sequence of actions every 7 tics. Fires, moves forward, stops, fires, turns left,
        repeats.
        This function will be passed into timer.todo. As such, it does not need
        :return: None
        """
        tank = self.state.mytanks[self.tank_index]

        if self.count == 0:
            tank.speed(1)
            # tank.shoot()

        if self.count == 3:
            tank.speed(0)

        if self.count == 5:
            tank.set_angvel(1)
            # tank.shoot()

        if self.count == 7:
            tank.set_angvel(0)
            self.count = -1

        self.count += Timer.TIME_PER_SLEEP


class PDFlagRetriever(Agent):

    def __init__(self, tank_index, flag_index, state):
        self.tank_index = tank_index
        self.flag_index = flag_index
        self.state = state
        self.timer_id = Timer.add_task(self.potential_fields_move)
        self.pfc = self.setup_potential_fields()
        self.pdcontroller = PDController()

    def potential_fields_move(self):

        # determine if I'm trying to attack the enemy or return home
        enemy_flag = self.state.flags[self.flag_index]
        if enemy_flag.possessing_team_color != self.state.me.color:  # attacking enemy
            flag = self.state.flags[self.flag_index]
        else:  # returning home
            flag = self.state.me.flag
        attractive = [AttractiveObject(x=flag.x, y=flag.y, radius=10, spread=100, alpha=1)]
        self.pfc.update(attractive, self.pfc.repulsive, self.pfc.tangential)

        # set up tank
        tank = self.state.mytanks[self.tank_index]
        # tank.shoot()  # attempt to clear obstacles

        # get the vector suggested by the potential field
        pf_vec = self.pfc.potential_fields_calc(tank.x, tank.y)

        # give the vector to the pd controller for actionable speed and angvel
        next_action = self.pdcontroller.get_next_action(tank, pf_vec)

        # act upon the new speed and angvel
        tank.speed(next_action['speed'])
        tank.set_angvel(next_action['angvel'])
        self.state.update_mytanks()
        self.state.update_flags()

        # logging.info("New tank status: %s", tank)

    def setup_potential_fields(self):
        flag = self.state.flags[self.flag_index]

        attractive = []
        repulsive = []
        tangential = []

        # attractive. One flag that I chose at random.
        logging.debug("Seeking flag %s", str(flag))
        attractive.append(AttractiveObject(x=flag.x, y=flag.y, radius=10, spread=1000000, alpha=1))

        return PotentialFieldCalculator(attractive, repulsive, tangential)