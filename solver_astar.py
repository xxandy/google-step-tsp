#!/usr/bin/env python3

import sys
import math
import numpy as np

from common import print_tour, read_input


class Node():
    """
    f(n) ... startからgoalまでの最短距離
    g(n) ... startからnノードまでの最短距離
    h(n) ... nノードからgoalまでの最短距離
    f(n) = g(n) + h(n)

    h*(n)をnからgoalまでの直線距離と仮定して予測する。
    f*(n) = g*(n) + h*(n)
    """
    start = None
    goal = None

    def __init__(self, position, index):
        self.parent = None
        self.index = index
        self.position = position

        self.hs = (position[0] - self.goal[0])**2 + (position[1] - self.goal[1])**2
        self.fs = 0
    
    def search_goal(self):
        return self.position == self.goal


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def astar(cities, distance, unvisited, start_i = 0):
    dist = distance.copy()
    #最も遠い都市をゴールにしておく。
    lst = dist[start_i]
    goal_i = np.argmax(lst)
    print("goal", goal_i)

    Node.start = cities[start_i]
    Node.goal = cities[goal_i]

    open_list = []
    close_list = []
    start_node = Node(cities[start_i], start_i)
    start_node.fs = start_node.hs
    open_list.append(start_node)

    while True:
        if not open_list:
            break
        #openリストの中でf*が最小のもの
        cur_i = min(open_list, key = lambda x : x.fs)
        open_list.remove(cur_i)
        close_list.append(cur_i)
        #goalにたどり着いたら終了
        if cur_i.search_goal():
            end_node = cur_i
            break

        #g*() = f*() - h*()
        cur_gs = cur_i.fs - cur_i.hs
        #近い都市4つを次に訪れる候補にする
        cand_index = np.argsort(dist[cur_i.index])[1:5]
        for next_i in cand_index:
            #print("next: ",next_i)
            #もしopenリストに入っていたなら
            if next_i in open_list:
                #f*がより小さければnext_iのf*を更新して親を書き換える
                if next_i.fs > cur_gs + next_i.hs + dist[cur_i.index][next_i.index]:
                    next_i.fs = cur_gs + next_i.hs + dist[cur_i.index][next_i.index]
                    next_i.parent = cur_i
            #もしcloseリストに入っていたなら
            elif next_i in close_list:
                #f*がより小さければnext_iのf*を更新して親を書き換えてopenリストに追加する
                if next_i.fs > cur_gs + next_i.hs + dist[cur_i.index][next_i.index]:
                    next_i.fs = cur_gs + next_i.hs + dist[cur_i.index][next_i.index]
                    next_i.parent = cur_i
                    open_list.append(next_i)
                    close_list.remove(next_i)
            #どちらにも入っていないならopenリストに追加
            else:
                next_i = Node(cities[next_i], next_i)
                next_i.fs = cur_gs + next_i.hs + dist[cur_i.index][next_i.index]
                next_i.parent = cur_i
                open_list.append(next_i)
            #次の候補に選ばれないように
            dist[cur_i.index][next_i.index] = 10**10
    #tourに結果を格納。unvisitedも記録。
    tour = []
    unvisited.append(start_i)
    while end_node:
        print(end_node.index)
        tour.append(end_node.index)
        unvisited.remove(end_node.index)
        end_node = end_node.parent
    return tour, unvisited


def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    
    unvisited = [i for i in range(1, N)]
    
    tour, unvisited = astar(cities, dist, unvisited, start_i=0)
    return tour



if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print("-----")
    print_tour(tour)
    print("-----")
    print(len(tour))
