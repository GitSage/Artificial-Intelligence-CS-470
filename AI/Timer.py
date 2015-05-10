import time
import logging
from PDController import PDController
__author__ = 'ben'


class Timer:

    def __init__(self, time_per_sleep, state):
        self.TIME_PER_SLEEP = time_per_sleep
        self.really_dumb_timers = {}
        self.pfc = None
        self.pdcontroller = PDController(time_per_sleep)
        self.todo = []
        self.state = state

    def tick(self):
        for task in self.todo:
            task.task(*task.args)

        time.sleep(self.TIME_PER_SLEEP)

    def add_task(self, task, args):
        self.todo.append(Task(task, args))

    def potential_fields_move(self, tank_index):
        tank = self.state.mytanks[tank_index]
        tank.shoot()  # attempt to clear obstacles
        pf_vec = self.pfc.potential_fields_calc(tank.x, tank.y)
        next_action = self.pdcontroller.get_next_action(tank, pf_vec)
        tank.speed(next_action['speed'])
        tank.set_angvel(next_action['angvel'])
        self.state.update_mytanks()
        logging.info("New tank status: %s", tank)

    def set_pfc(self, pfc):
        self.pfc = pfc

    def really_dumb_agent(self, tank):

        if tank not in self.really_dumb_timers:
            self.really_dumb_timers[tank] = 0

        if self.really_dumb_timers[tank] == 0:
            tank.speed(1)
            tank.shoot()

        if self.really_dumb_timers[tank] == 3:
            tank.speed(0)

        if self.really_dumb_timers[tank] == 5:
            tank.set_angvel(1)
            tank.shoot()

        if self.really_dumb_timers[tank] == 7:
            tank.set_angvel(0)
            self.really_dumb_timers[tank] = -1

        self.really_dumb_timers[tank] += self.TIME_PER_SLEEP


class Task:

    def __init__(self, task, *args):
        self.task = task
        self.args = args