import time
import numpy as np

start_time = 0

def iterations(count, output=False, input_generator=lambda: True):
    def decorate(fn):
        def wrapper():
            result = []
            for _ in range(count):
                result.append(fn(*input_generator()))
            return result if output else True
        return wrapper
    return decorate

def random_list_generator(n, max_int):
    return lambda: [np.random.randint(max_int, size=n)]


def start_timer():
    global start_time
    start_time = time.time_ns()

def end_time():
    time_took = (time.time_ns() - start_time) / 1e6
    print("Program took", time_took, "ms to run.")