#!/usr/bin/env python3

import sys
import math
import time
import numpy as np

from concurrent.futures import ThreadPoolExecutor 

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


def solve_helper(cities, start_i):
    print("start : ", start_i)
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = start_i
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    flag = 0
    while unvisited_cities and flag == 0:
        how_far = [0,1,2,3,4]
        executor = ThreadPoolExecutor(max_workers=5)
        can_tour = []
        can_unvisited_cities = []
        distances = []
        #Threadを使って５つの経路を同時探索し、最短のものを採用する。
        for far in how_far:
            future = executor.submit(sub_greedy, far, tour, unvisited_cities, dist, current_city)
            can_tour.append(future.result()[0])
            can_unvisited_cities.append(future.result()[1])
            distances.append(future.result()[2])
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
    print("finish : ", start_i)
    return tour


def solve(cities):
    tours = []
    N = len(cities)
    executor = ThreadPoolExecutor(max_workers=N)
    start_index = [i for i in range(N)]
    #threadを用いて各スタート地点から始めた場合の経路を同時探索する
    for start_i in start_index:
        future = executor.submit(solve_helper, cities, start_i)
        tours.append(future.result())
    #経路が一番短いものを採用
    ans_tour = None
    min_length = float('inf')
    for j in range(N):
        tour = tours[i]
        path_l = sum(distance(cities[tour[i]], cities[tour[(i + 1) % N]]) for i in range(N))
        if path_l < min_length:
            min_length = path_l
            ans_tour = tour
    return ans_tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    print("---")
    print(len(tour))
    
