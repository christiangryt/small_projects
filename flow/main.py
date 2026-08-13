from cbs import *
from boards import *

# Make graph object
g = graph(hard)

# Solver
cbs = CBS_solver(g)

#cbs.solve_puzzle()

test = True
while test:

    solved = cbs.solve_puzzle_single_iteration()

    if solved:
        test = False
