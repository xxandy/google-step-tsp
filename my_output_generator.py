#!/usr/bin/env python3

from common import format_tour, read_input
import os

import solver_greedy
import solver_random
import solver_remove_cross

CHALLENGES = 7


def generate_sample_output():
    for i in range(CHALLENGES):
        cities = read_input(f'input_{i}.csv')
        for solver, name in ((solver_remove_cross, 'remove_cross'), (solver_random, 'random')):
            tour = solver.solve(cities)
            os.makedirs("my_ans/" + name, exist_ok = True)
            with open(f'my_ans/{name}/output_{i}.csv', 'w') as f:
                f.write(format_tour(tour) + '\n')


if __name__ == '__main__':
    generate_sample_output()
