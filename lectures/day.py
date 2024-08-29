import sys
sys.path.append("../CSE-331")
from helper import iterations, random_list_generator, time_test

@iterations(1000, input_generator=random_list_generator(100, 10000))
# @time_test([1]*100)
def run(lst):
    pass
run()