import time
__author__ = 'ben'


class Timer:
    todo = []  # static
    TIME_PER_TICK = 0.0
    time_passed = 0.0

    def __init__(self, time_per_sleep):
        Timer.TIME_PER_TICK = time_per_sleep

    @classmethod
    def add_task(cls, task):
        cls.todo.append(task)
        return len(cls.todo)-1

    @classmethod
    def remove_task(cls, task_index):
        cls.todo.remove(task_index)

    @classmethod
    def tick(cls):
        """
        Performs every action on the todo list.
        If the tick took less time than TIME_PER_TICK, sleeps until TIME_PER_TICK has passed.
        cls.time_passed will be updated with the true time that passed during the current tick (always greater than or
        equal to TIME_PER_TICK).
        :return: none
        """
        start = time.time()
        for task in cls.todo:
            task()
        spent = start - time.time()

        # if spent is less than TIME_PER_TICK, sleep the remaining period
        to_sleep = max(0, cls.TIME_PER_TICK - spent)
        time.sleep(to_sleep)

        # update cls.time_passed with the true amount of time that passed
        cls.time_passed = max(cls.TIME_PER_TICK, spent)
