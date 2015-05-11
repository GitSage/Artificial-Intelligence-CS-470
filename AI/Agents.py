import logging
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
            tank.shoot()

        if self.count == 3:
            tank.speed(0)

        if self.count == 5:
            tank.set_angvel(1)
            tank.shoot()

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
        self.attacking = True

    def potential_fields_move(self):

        # set up tank
        tank = self.state.mytanks[self.tank_index]
        tank.shoot()  # attempt to clear obstacles

        # check if I just picked up the enemy flag
        if tank.flag != '-' and self.attacking:
            self.return_to_base()

        # check if I just returned the enemy flag
        if tank.flag == '-' and not self.attacking:
            self.attack_enemy_flag()

        # get the vector suggested by the potential field
        pf_vec = self.pfc.potential_fields_calc(tank.x, tank.y)

        # give the vector to the pd controller for actionable speed and angvel
        next_action = self.pdcontroller.get_next_action(tank, pf_vec)

        # act upon the new speed and angvel
        tank.speed(next_action['speed'])
        tank.set_angvel(next_action['angvel'])
        self.state.update_mytanks()
        self.state.update_flags()

    def setup_potential_fields(self):
        flag = self.state.flags[self.flag_index]

        attractive = []
        repulsive = []
        tangential = []

        # attractive. One flag that I chose at random.
        logging.debug("Tank %s is seeking flag %s", self.tank_index, str(flag))
        attractive.append(AttractiveObject(x=flag.x, y=flag.y, radius=10, spread=1000000, alpha=1),)

        # repulsive. The corner of every obstacle gets a small, hard repulsive field, and the center gets a large, weak
        # field.
        obstacles = self.state.obstacles
        for obstacle in obstacles:
            for point in obstacle.points:
                repulsive.append(RepulsiveObject(x=point[0], y=point[1], radius=3, spread=6, alpha=10))
            centerpoint = obstacle.get_centerpoint()
            repulsive.append(RepulsiveObject(x=centerpoint['x'], y=centerpoint['y'], radius=obstacle.get_radius()+20,
                                             spread=50, alpha=10))

        # tangential. Same rules as repulsive.
        obstacles = self.state.obstacles
        for obstacle in obstacles:
            for point in obstacle.points:
                tangential.append(TangentialObject(x=point[0], y=point[1], radius=3, spread=6, alpha=10))
            centerpoint = obstacle.get_centerpoint()
            tangential.append(TangentialObject(x=centerpoint['x'], y=centerpoint['y'], radius=obstacle.get_radius()+20,
                                               spread=50, alpha=10))

        return PotentialFieldCalculator(attractive, repulsive, tangential)

    def return_to_base(self):
        self.attacking = False
        base_coords = self.state.me.base.get_centerpoint()
        attractive = [AttractiveObject(x=base_coords['x'], y=base_coords['y'], radius=10, spread=100, alpha=1)]
        self.pfc.update(attractive, self.pfc.repulsive, self.pfc.tangential)

    def attack_enemy_flag(self):
        self.attacking = True
        flag = self.state.flags[self.flag_index]
        attractive = [AttractiveObject(x=flag.x, y=flag.y, radius=10, spread=100, alpha=1)]
        self.pfc.update(attractive, self.pfc.repulsive, self.pfc.tangential)