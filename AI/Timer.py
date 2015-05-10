import time
__author__ = 'ben'


class Timer:
    todo = []  # static
    TIME_PER_SLEEP = 0

    def __init__(self, time_per_sleep):
        Timer.TIME_PER_SLEEP = time_per_sleep

    @classmethod
    def add_task(cls, task):
        cls.todo.append(task)
        return len(cls.todo)-1

    @classmethod
    def remove_task(cls, task_index):
        cls.todo.remove(task_index)

    @classmethod
    def tick(cls):
        for task in cls.todo:
            task()

        time.sleep(cls.TIME_PER_SLEEP)
