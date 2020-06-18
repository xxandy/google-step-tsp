import numpy as np
import sys
import math

from common import print_tour, read_input

#Kmeans法
def update_label(cities, center, k):
    label = []
    for i in range(len(cities)):
        min_dis = float('inf')
        for j in range(k):
            distance = (cities[i][1] - center[j][1]) ** 2 + (cities[i][0] - center[j][0]) ** 2
            if distance < min_dis:
                l = j
                min_dis = distance
        label.append(l)
    return np.array(label)


def update_center(cities, label, k):
    label = np.array(label)
    cities = np.array(cities)
    center = []
    for i in range(k):
        cen_lis = np.mean(cities[np.where(label == i)],axis = 0)
        center.append((cen_lis[0], cen_lis[1]))
    return np.array(center)


def k_means(cities, k, max_iter):
    copy =  cities
    np.random.shuffle(copy)
    center = copy[:k]  # 重心の初期値

    before_label = np.ones(len(cities))  # 新しいラベルとの差を見るため。
    label = np.zeros(len(cities))

    iter = 0
    while (not (before_label == label).all() and iter < max_iter):
        before_label = label
        label = update_label(cities, center, k)
        center = update_center(cities, label, k)
        iter += 1
    return center, label


#citiesを1グループdev_num個になるようにkmeansで分ける
def divide_cities(cities, dev_num):
    k = len(cities) // dev_num
    if k == 0:
        k += 1
    center, labels = k_means(cities, k, max_iter = 300)
    divided_cities = {}
    for l, city in zip(labels, cities):
        if not l in divided_cities:
            divided_cities[l] = []
        divided_cities[l].append(city)
    return center, divided_cities


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


def solve_sub(cities, start_city=0, flag = True):
    dic = {}
    for i, city in enumerate(cities):
        dic[i] = city

    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = start_city
    unvisited_cities = set(range(1, N))
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
    new_tour = [next_city] + new_tour
    if not flag:
        return new_tour
    answer = []
    for city in new_tour:
        answer.append(dic[city])
    return answer


def solve(cities):
    dic = {}
    for i, city in enumerate(cities):
        dic[city] = i
    tours = []
    center_pos, divided_cities = divide_cities(cities, 100)
    for i in range(len(divided_cities)):
        cities = divided_cities[i]
        #print(len(cities))
        tour = solve_sub(cities)
        tours.append(tour)
    answer = []
    #どの塊から回るかを中心座標から判断
    index_list = solve_sub(center_pos, 0, False)
    #print(index_list)
    for i in index_list:
        answer += tours[i]
    for i in range(len(answer)):
        answer[i] = dic[answer[i]]
    return answer


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    print("")
    print(len(tour))
