import time
from PotentialFieldCalculator import PotentialFieldCalculator

__author__ = 'ben'


class Timer:

    def __init__(self, time_per_sleep):
        self.TIME_PER_SLEEP = time_per_sleep
        self.really_dumb_timers = {}
        # self.potential_field_calculator = PotentialFieldCalculator()
        self.todo = []

    def tick(self):
        for task in self.todo:
            task.task(*task.args)

        time.sleep(self.TIME_PER_SLEEP)

    def add_task(self, task, args):
        self.todo.append(Task(task, args))

    def potential_fields_move(self, tank, goal):
        # self.potential_fields_calculator =
        next_action = self.potential_fields_calculator.get_next_action(tank.x, tank.y)
        tank.dir = next_action['dir']

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