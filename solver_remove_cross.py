#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def crossChecker(city1, city2, lines, cities):
    """
    input
    city : index
    cities : list [(x,y),(x,y)...]
    lines : list [(from_index, to_index), ...]

    output
    cross cities , lines
    """
    city1 = cities[city1]
    city2 = cities[city2]
    for line in lines:
        city3 = cities[line[0]]
        city4 = cities[line[1]]
        #line eq (x2-x1)*(y-y1)+(y2-y1)*(x1-x)=0
        t1 = (city2[0] - city1[0]) * (city3[1] - city1[1]) + (city2[1] - city1[1]) * (city1[0] - city3[0])
        t2 = (city2[0] - city1[0]) * (city4[1] - city1[1]) + (city2[1] - city1[1]) * (city1[0] - city4[0])
        t3 = (city4[0] - city3[0]) * (city1[1] - city3[1]) + (city4[1] - city3[1]) * (city3[0] - city1[0])
        t4 = (city4[0] - city3[0]) * (city2[1] - city3[1]) + (city4[1] - city3[1]) * (city3[0] - city2[0])
        if t1 * t2 < 0 and t3 * t4 < 0: #cross
            lines.remove((line[0], line[1]))
            return line[0], line[1] , lines
    return None, None, lines


def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]
    lines = []

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        #cross check
        city1, city2, lines = crossChecker(current_city, next_city, lines, cities)
        if city1:
            start = min(tour.index(city1), tour.index(city2))
            tour = tour[:start + 1] + tour[start + 1:][::-1]
            lines.append((city1, current_city))
            lines.append((city2, next_city))
        else:
            lines.append((current_city, next_city))
        tour.append(next_city)
        current_city = next_city
        #print(tour)
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
