#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def crossChecker(city1, city2, cities, tour):
    """
    input
    city : index
    cities : list [(x,y),(x,y)...]

    output cross_list : list [(index, index), ...]
    """
    city1 = cities[city1]
    city2 = cities[city2]
    for i in range(len(tour[:-1])):
        city3 = cities[tour[i]]
        city4 = cities[tour[i + 1]]
        #line eq (x2-x1)*(y-y1)+(y2-y1)*(x1-x)=0
        t1 = (city2[0] - city1[0]) * (city3[1] - city1[1]) + \
            (city2[1] - city1[1]) * (city1[0] - city3[0])
        t2 = (city2[0] - city1[0]) * (city4[1] - city1[1]) + \
            (city2[1] - city1[1]) * (city1[0] - city4[0])
        t3 = (city4[0] - city3[0]) * (city1[1] - city3[1]) + \
            (city4[1] - city3[1]) * (city3[0] - city1[0])
        t4 = (city4[0] - city3[0]) * (city2[1] - city3[1]) + \
            (city4[1] - city3[1]) * (city3[0] - city2[0])
        if t1 * t2 < 0 and t3 * t4 < 0:  # cross
            return tour[i], tour[i + 1]
    return None, None


def change_lines(city1, city2, city3, city4, tour):
    """
    input_tour : ... city1 -> city2 ... city3 -> city4 ...
    output_tour : ... city1 -> city3 ... city2 -> city4 ...
    """
    start = tour.index(city2)
    end = tour.index(city3)
    tour = tour[:start] + tour[start: end + 1][::-1] + tour[end + 1:]
    return tour


def removeCross(current_city, next_city, cities, tour):
    city1, city2 = crossChecker(current_city, next_city, cities, tour)
    city3 = current_city
    city4 = next_city
    #print(cross_list)
    if city1:
        if tour.index(city1) < tour.index(city3):
            c1, c2, c3, c4 = city1, city2, city3, city4
        else:
            c1, c2, c3, c4 = city3, city4, city1, city2
        #print(tour.index(c1),tour.index(c2),tour.index(c3))
        tour = change_lines(c1, c2, c3, c4, tour)
        tour = removeCross(c1, c3, cities, tour)
        tour = removeCross(c2, c4, cities, tour)
    return tour


def solve_helper(cities, start_city=0):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = start_city
    unvisited_cities = set(range(0, N))
    unvisited_cities.remove(current_city)
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        #remove cross
        tour = removeCross(current_city, next_city, cities, tour)
        tour.append(next_city)
        current_city = next_city
    #最後の１本
    next_city = tour.pop(0)
    new_tour = removeCross(current_city, next_city, cities, tour)
    if len(new_tour) != len(cities) - 1:
        new_tour = tour
    return [next_city] + new_tour


def solve(cities):
    N = len(cities)
    tours = []
    min_length = float('inf')
    for i in range(N):
        print(i)
        try:
            tour = solve_helper(cities, start_city=i)
            path_length = sum(distance(cities[tour[i]], cities[tour[(i + 1) % N]]) for i in range(N))
            if path_length < min_length:
                index = i
                min_length = path_length
            tours.append(tour)
        except:
            print("Error")
            tours.append(None)
    return tours[index]


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    print("")
    print(len(tour))
