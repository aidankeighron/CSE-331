import time
import numpy as np
from tabulate import tabulate

def time_test(default_input, input_generator=None, iteration_options=[1,100,1000,100_000]):
    def decorate(fn):
        def wrapper():
            rows = []
            def run_iterations(n):
                iterations = 0
                elapsed_time = 0
                for _ in range(n):
                    start = time.time_ns()
                    fn(input_generator() if input_generator else default_input)
                    end = time.time_ns()
                    iterations += 1
                    elapsed_time += end-start
                
                rows.append([iterations, time_to_string(elapsed_time), time_to_string(elapsed_time/iterations)])
                
            for n in iteration_options:
                run_iterations(n)
                
            print(tabulate(rows, headers=['Iterations', 'Total', 'Average'], tablefmt="plain"))
            return True
        return wrapper
    return decorate

def iterations(count, input_generator=None):
    def decorate(fn):
        def wrapper():
            elapsed_time = 0
            iterations = 0
            start_time = time.time_ns()
            
            if input_generator:
                for _ in range(count):
                    start = time.time_ns()
                    fn(*input_generator())
                    end = time.time_ns()
                    iterations += 1
                    elapsed_time += end-start
            else:
                for _ in range(count):
                    start = time.time_ns()
                    fn()
                    iterations += 1
                    end = time.time_ns()
                    elapsed_time += end-start
            
            time_took = time.time_ns() - start_time
            print(tabulate([[time_to_string(time_took), time_to_string(elapsed_time), time_to_string(elapsed_time/iterations)]], 
                           headers=['Total', 'Elapsed', 'Average']))
            return True
        return wrapper
    return decorate

def random_list_generator(max_size, max_int, random=False):
    length = np.random.randint(max_size)
    return lambda: [np.random.randint(max_int, size=length if random else max_size)]
    
def time_to_string(time):
    units = "ns"
    
    microseconds = time > 1000
    if microseconds:
        units = 'μs'
        time /= 1000
    
    milliseconds = time > 1000
    if milliseconds:
        units = 'ms'
        time /= 1000
    
    seconds = time > 1000
    if seconds:
        units = 's'
        time /= 1000
    
    return f"{round(time, 3)} {units}"
