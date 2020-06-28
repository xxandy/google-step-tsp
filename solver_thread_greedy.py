#!/usr/bin/env python3

import sys
import math
import time
import numpy as np

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def sub_greedy(index, tour, unvisited_cities, dist, current_city):
    #6都市先に進んだ時の長さを求める。
    sub_tour = tour.copy()
    sub_unvisited_cities = unvisited_cities.copy()
    distance = 0
    #index+1番目に近い都市をnext_cityにする。
    cand_cities = sorted(sub_unvisited_cities,
                         key=lambda city: dist[current_city][city])
    if index+1 >= len(cand_cities):
        return None, None, None
    next_city = cand_cities[index]
    distance += dist[current_city][next_city]
    sub_unvisited_cities.remove(next_city)
    sub_tour.append(next_city)
    current_city = next_city
    for _ in range(5):
        if not sub_unvisited_cities:
            break
        next_city = min(sub_unvisited_cities,
                             key=lambda city: dist[current_city][city])
        distance += dist[current_city][next_city]
        sub_unvisited_cities.remove(next_city)
        sub_tour.append(next_city)
        current_city = next_city
    return sub_tour, sub_unvisited_cities, distance


def remove_cross(tour, dist, flag = True):
    N = len(tour)
    while True:
        end_flag = True
        for i in range(N-2):
            for j in range(i+1, N-1):
                cur_dist = dist[tour[i]][tour[i+1]] + dist[tour[j]][tour[j+1]]
                new_dist = dist[tour[i]][tour[j]] + dist[tour[i+1]][tour[j+1]]
                if new_dist < cur_dist:
                    end_flag = False
                    tour = tour[:i + 1] + tour[i + 1: j + 1][::-1] + tour[j + 1:]
        if end_flag:
            break
    #print(tour)
    if flag:
        #最後の一本
        copy_tour = tour.copy()[1:]
        start_city = tour[0]
        new_tour = remove_cross(copy_tour + [start_city], dist, flag = False)
        if len(new_tour) != N:
            new_tour = copy_tour
        tour = [start_city] + new_tour
    return tour


def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    flag = 0
    while unvisited_cities and flag == 0:
        tour1, unvisited_cities1, distance1 = sub_greedy(0, tour, unvisited_cities, dist, current_city)
        tour2, unvisited_cities2, distance2 = sub_greedy(
            1, tour, unvisited_cities, dist, current_city)
        tour3, unvisited_cities3, distance3 = sub_greedy(
            2, tour, unvisited_cities, dist, current_city)
        tour4, unvisited_cities4, distance4 = sub_greedy(
            3, tour, unvisited_cities, dist, current_city)
        tour5, unvisited_cities5, distance5 = sub_greedy(
            4, tour, unvisited_cities, dist, current_city)
        distances = np.array([distance1, distance2, distance3, distance4, distance5])
        can_tour = [tour1, tour2, tour3, tour4, tour5]
        can_unvisited_cities = [unvisited_cities1, unvisited_cities2, unvisited_cities3, unvisited_cities4, unvisited_cities5]
        if None in distances:
            while unvisited_cities:
                next_city = min(unvisited_cities,
                                key=lambda city: dist[current_city][city])
                unvisited_cities.remove(next_city)
                tour.append(next_city)
                current_city = next_city
            flag = 1
        else:
            mi = np.argmin(distances)
            tour = can_tour[mi]
            unvisited_cities = can_unvisited_cities[mi]
    tour = remove_cross(tour, dist)
    return tour



if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    
