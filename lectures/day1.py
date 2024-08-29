import sys
sys.path.append("../CSE-331")
from helper import start_timer, iterations, end_time, random_list_generator

start_timer()

@iterations(1_000, input_generator=random_list_generator(10, 100))
def run(l):
    if not len(l):
        l = [1,2,3]

    s = 0
    out = []
    n = len(l)
    for i in range(n):
        s += l[i]
        out.append(s/(i+1))
    # print(out)
run()

end_time()