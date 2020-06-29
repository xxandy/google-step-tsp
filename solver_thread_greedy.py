#!/usr/bin/env python3

import sys
import math
import time
import numpy as np

import random 
import threading

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def sub_greedy(index, tour, unvisited_cities, dist, current_city, results):
    #6都市先に進んだ時の長さを求める。
    sub_tour = tour.copy()
    sub_unvisited_cities = unvisited_cities.copy()
    distance = 0
    #index+1番目に近い都市をnext_cityにする。
    cand_cities = sorted(sub_unvisited_cities,
                         key=lambda city: dist[current_city][city])
    if index+1 >= len(cand_cities):
        results.append([None, None, None])
        return
    next_city = cand_cities[index]
    distance += dist[current_city][next_city]
    sub_unvisited_cities.remove(next_city)
    sub_tour.append(next_city)
    current_city = next_city
    for _ in range(5): #need tuning
        if not sub_unvisited_cities:
            break
        next_city = min(sub_unvisited_cities,
                             key=lambda city: dist[current_city][city])
        distance += dist[current_city][next_city]
        sub_unvisited_cities.remove(next_city)
        sub_tour.append(next_city)
        current_city = next_city
    results.append([sub_tour, sub_unvisited_cities, distance])


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
        tour = new_tour
    return tour


def solve_helper(cities, start_i, tours):
    print("start : ", start_i)
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = start_i
    unvisited_cities = [i for i in range(N)]
    unvisited_cities.remove(start_i)
    tour = [current_city]

    flag = 0
    #Threadを使って15個の経路を同時探索し、最短のものを採用する。
    while unvisited_cities and flag == 0:
        thread_list = []
        results = []
        for i in range(15): #need tuning
            thread = threading.Thread(target=sub_greedy, args=(
                [i, tour, unvisited_cities, dist, current_city, results]))
            thread_list.append(thread)
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()
        #経路が一番短いものを採用
        results = np.array(results)
        distances = results[:,2]
        can_tour = results[:,0]
        can_unvisited_cities = results[:,1]
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
    tours.append(tour)


def solve(cities):
    N = len(cities)
    #threadを用いて各スタート地点から始めた場合の経路を同時探索する
    #N>128ならランダムに10個のスタート地点を選ぶ
    start_list = [i for i in range(N)]
    if N > 128:
        #start_list = random.sample(start_list, 10)
        start_list = random.sample(start_list, 2)
    thread_list = []
    tours = []
    for start_i in start_list:
        thread = threading.Thread(target=solve_helper, args=([cities, start_i, tours]))
        thread_list.append(thread)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
    #経路が一番短いものを採用
    ans_tour = None
    min_length = float('inf')
    for j in range(len(start_list)):
        tour = tours[j]
        try:
            path_l = sum(distance(cities[tour[i]], cities[tour[(i + 1) % N]]) for i in range(N))
            if path_l < min_length:
                min_length = path_l
                ans_tour = tour
        except:
            pass
    print("path_length : ", min_length)
    return ans_tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    print("---")
    print(len(tour))
    
