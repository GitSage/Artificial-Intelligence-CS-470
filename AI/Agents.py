import logging
import random
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
        self.prev_x = 0
        self.prev_y = 0
        self.time_spent_stuck = 0  # stuck for more than 10 seconds, get a new random vector
        self.time_without_moving = 0  # consider ourselves stuck only after 5 seconds
        self.stuck_vector = [0, 0]
        self.stuck = False

    def potential_fields_move(self):

        # set up tank
        tank = self.state.mytanks[self.tank_index]
        tank.shoot()

        # check if I'm stuck and respond appropriately if so
        self.check_stuck(tank)

        # check if I just picked up the enemy flag
        if tank.flag != '-' and self.attacking:
            self.return_to_base()

        # check if I just returned the enemy flag
        if tank.flag == '-' and not self.attacking:
            self.attack_enemy_flag()

        if not self.stuck:
            # get the vector suggested by the potential field
            pf_vec = self.pfc.potential_fields_calc(tank.x, tank.y)
        else:
            pf_vec = self.stuck_vector

        # give the vector to the pd controller for actionable speed and angvel
        next_action = self.pdcontroller.get_next_action(tank, pf_vec)

        # act upon the new speed and angvel
        tank.speed(next_action['speed'])
        tank.set_angvel(next_action['angvel'])
        self.state.update_mytanks()
        self.state.update_flags()
        self.prev_x = tank.x
        self.prev_y = tank.y

    def check_stuck(self, tank):
        # check if I've moved recently
        if tank.x == self.prev_x and tank.y == self.prev_y:
            self.time_without_moving += Timer.TIME_PER_SLEEP
            tank.shoot()

            # check if I'm stuck. Considered "stuck" if I haven't changed position in 5 seconds.
            if self.time_without_moving > .5:

                self.stuck = True
                # print "STUCK!"

                # if we just got stuck or we've been stuck for too long, get new random vector and shoot.
                if self.time_spent_stuck == 0:
                    self.stuck_vector = [random.random() * 200 - 100, random.random() * 200 - 100]
                    # print "Generated random vector ", self.stuck_vector


                # add to the stuck timer. If it's longer than 10 seconds, reset to 0.
                self.time_spent_stuck += Timer.TIME_PER_SLEEP
                if self.time_spent_stuck >= 2.5:
                    self.time_spent_stuck = 0

        elif self.stuck:
            # print "RESETTING!"
            self.time_without_moving = 0
            self.stuck = False
            self.stuck_vector = [0, 0]

    def setup_potential_fields(self):

        flag = self.state.flags[self.flag_index]

        attractive = []
        repulsive = []
        tangential = []

        # attractive. One flag that I chose at random.
        logging.debug("Tank %s is seeking flag %s", self.tank_index, str(flag))

        attractive.append(AttractiveObject(x=flag.x, y=flag.y, radius=10, spread=20, alpha=1),)

        if len(self.state.obstacles) == 4:
            tangential.append(TangentialObject(x=121.2132034355, y=21.2132034356, radius=30, spread=60, alpha=1))

            #LEFT
            tangential.append(TangentialObject(x=-78.78679656439999, y=21.2132034356, radius=30, spread=60, alpha=1,
                                               clockwise=False))

            #TOP
            tangential.append(TangentialObject(x=21.2132034356, y=121.2132034355, radius=30, spread=60, alpha=1))

            #BOTTOM
            tangential.append(TangentialObject(x=21.2132034356, y=-78.78679656439999, radius=30, spread=60, alpha=1))
        else:

            # Top Left L
            tangential.append(TangentialObject(x=-90, y=120, radius=30, spread=100, alpha=1))
            tangential.append(TangentialObject(x=-90, y=180, radius=30, spread=100, alpha=1))
            tangential.append(TangentialObject(x=-150, y=120, radius=30, spread=100, alpha=1))

            # Top Right L
            tangential.append(TangentialObject(x=150, y=120, radius=30, spread=100, alpha=1))
            tangential.append(TangentialObject(x=150, y=180, radius=30, spread=100, alpha=1))
            tangential.append(TangentialObject(x=210, y=120, radius=30, spread=100, alpha=1))

            # Bottom Right L
            tangential.append(TangentialObject(x=150, y=-120, radius=30, spread=100, alpha=1))
            tangential.append(TangentialObject(x=210, y=-120, radius=30, spread=100, alpha=1))
            tangential.append(TangentialObject(x=150, y=-180, radius=30, spread=100, alpha=1))

            # Bottom Left L
            tangential.append(TangentialObject(x=-90, y=-120, radius=30, spread=100, alpha=1))
            tangential.append(TangentialObject(x=-90, y=-180, radius=30, spread=100, alpha=1))
            tangential.append(TangentialObject(x=-150, y=-120, radius=30, spread=100, alpha=1))

            # Top Left L
            tangential.append(TangentialObject(x=-90, y=120, radius=30, spread=100, alpha=1))
            tangential.append(TangentialObject(x=-90, y=180, radius=30, spread=100, alpha=1))
            tangential.append(TangentialObject(x=-150, y=120, radius=30, spread=100, alpha=1))

            # Middle Rectangular Obstacle
            tangential.append(TangentialObject(x=0, y=10, radius=60, spread=100, alpha=1))

        return PotentialFieldCalculator(attractive, repulsive, tangential)

    def return_to_base(self):
        self.attacking = False
        base_coords = self.state.me.base.get_centerpoint()
        attractive = [AttractiveObject(x=base_coords['x'], y=base_coords['y'], radius=10, spread=20, alpha=1)]
        self.pfc.update(attractive, self.pfc.repulsive, self.pfc.tangential)

    def attack_enemy_flag(self):
        self.attacking = True
        flag = self.state.flags[self.flag_index]
        attractive = [AttractiveObject(x=flag.x, y=flag.y, radius=10, spread=20, alpha=1)]
        self.pfc.update(attractive, self.pfc.repulsive, self.pfc.tangential)


class BayesianGridSearchAgent(Agent):

    def __init__(self, tank_index, bay_vis, bay_filter, state):
        self.tank_index = tank_index
        self.state = state
        self.bay_vis = bay_vis
        self.bay_filter = bay_filter

        # the tank should change goals periodically
        self.time_since_goal_change = 0
        self.goal_x = 0
        self.goal_y = 0

        self.pdcontroller = PDController()
        self.pfc = self.setup_potential_fields()

        # these variables are used to check if we're stuck
        self.time_without_moving = 0
        self.prev_x = 0
        self.prev_y = 0

        self.timer_id = Timer.add_task(self.bayesian_grid_search)

    def bayesian_grid_search(self):
        # set up tank
        tank = self.state.mytanks[self.tank_index]
        self.time_since_goal_change += Timer.TIME_PER_SLEEP
        if self.time_since_goal_change.is_integer():
            print self.time_since_goal_change

        self.check_new_direction(tank)

        # get the vector suggested by the potential field
        pf_vec = self.pfc.potential_fields_calc(tank.x, tank.y)

        # give the vector to the pd controller for actionable speed and angvel
        next_action = self.pdcontroller.get_next_action(tank, pf_vec)

        # act upon the new speed and angvel
        tank.speed(next_action['speed'])
        tank.set_angvel(next_action['angvel'])
        self.state.update_mytanks()
        self.state.update_flags()
        self.prev_x = tank.x
        self.prev_y = tank.y

        # ask the server for current position and update the Grid Filter
        self.update_grid()

    def check_new_direction(self, tank):
        # check if stuck
        if self.is_stuck(tank):
            print "Tank %s stuck, changing direction" % self.tank_index
            self.new_direction()

        # check if tank arrived at goal
        if abs(tank.x - self.goal_x) < 10 and abs(tank.y - self.goal_y) < 10:
            print "Tank %s arrived at goal, changing direction" % self.tank_index
            self.new_direction()

        # check if tank hasn't changed direction in a long time
        if self.time_since_goal_change > 60:
            print "Tank %s timeout, changing direction" % self.tank_index
            self.new_direction()

    def is_stuck(self, tank):
        # check if I've moved recently
        if tank.x == self.prev_x and tank.y == self.prev_y:
            self.time_without_moving += Timer.TIME_PER_SLEEP

            # check if I'm stuck. Considered "stuck" if I haven't changed position in 1 second.
            if self.time_without_moving > 1:
                tank.shoot()
                self.time_without_moving = 0
                return True

    def new_direction(self):
        self.goal_x = random.randint(-400, 400)
        self.goal_y = random.randint(-400, 400)
        self.time_since_goal_change = 0
        attractive = [AttractiveObject(x=self.goal_x, y=self.goal_y, radius=10, spread=1000000, alpha=1000)]
        self.pfc.update(attractive, self.pfc.repulsive, self.pfc.tangential)
        print "Tank %s new goal (%f,%f)" % (self.tank_index, self.goal_x, self.goal_y)

    def setup_potential_fields(self):
        attractive = []
        repulsive = []
        tangential = []
        self.pfc = PotentialFieldCalculator(attractive, repulsive, tangential)
        self.new_direction()

        return self.pfc

    def update_grid(self):
        x, y, grid = self.state.update_occgrid(self.tank_index)  # ask the server for the occgrid
        #self.bay_filter.test(grid, int(x), int(y))  # run it through the fake bayesian filter
        self.bay_filter.bayesian_grid(grid, int(x), int(y))  # run it through the bayesian filter
        self.bay_vis.update_and_draw_grid(self.bay_filter.model)  # draw it
