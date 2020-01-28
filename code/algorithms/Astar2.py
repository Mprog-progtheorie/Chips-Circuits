from queue import PriorityQueue
import numpy as np
import time

def heuristic(current, goal):
    h = abs(np.array(current) - np.array(goal))
    return h.sum()

def gate_neighbours(current, grid, path):
    neighbours = list()

    # HEURISTIC
    moves = list()
    for x in range(-1, 2):
        for y in range(-1, 2):
            # HEURISTIC
            for z in range(8):
                moves.append((x, y, z))

    for i in moves:
        neighbour = tuple(np.array(current) + np.array(i))
        if neighbour not in path:
            if neighbour in grid:
                if grid.get(neighbour)[0]:
                    neighbours.append(neighbour)
    return neighbours



def neighbours(current, grid, path):
    neighbours = list()

    # kan in for loop
    moves = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

    for i in moves:
        neighbour = tuple(np.array(current) + np.array(i))
        if neighbour not in path:
            if neighbour in grid:
                if grid.get(neighbour)[0]:
                    neighbours.append(neighbour)

    return neighbours

def a_star(start, end, grid, ceiling_count):
    pq = PriorityQueue()

    path = [start]
    
    visited = set()

    test_bool = False
    test_count = 0
    test_old = None

    check_difference = 0

    # HEURISTIC
    # if heuristic(start, end) > 5:
    #     for i in range(ceiling_count):
    #         force_up = list(path[-1])
    #         # print("1", force_up)

    #         if test_bool:
    #             force_up[2] = test_count
    #             test_bool = False
    #         else:
    #             test_count += 1
    #             force_up[2] = test_count
    #         force_up = tuple(force_up)
    #         if test_old != None:
    #             print("old", test_old, force_up)
    #             check_difference = force_up[2] - test_old[2]
    #             print("CHECKDIFF", check_difference)

    #         if grid.get(force_up)[0]:
    #             if force_up != start:
    #                 if force_up not in visited:
    #                     path.append(force_up)
    #                 # print(force_up)
    #                     visited.add(force_up)
    #         else:
    #             # print("in")
    #             test_bool = True
    #             test_count = i
    #             neighbour_list = neighbours(path[-1], grid, path)
    #             if neighbour_list:
    #                 for neighbour in neighbour_list:
    #                     if grid.get(neighbour)[0]:
    #                         if neighbour not in visited:
    #                             if check_difference == 1:
    #                                 print(test_count, i, "neighbour", neighbour)
    #                                 test_old = neighbour
    #                                 path.append(neighbour)
    #                                 visited.add(neighbour)
    #                         break
    #             else:
    #                 return False
    #         # print(grid.get(force_up))
    # if start == (15, 11, 0):
    #     print(path)

    f = grid.get(path[-1])[1] + heuristic(path[-1], end)

    # input(path)
    pq.put((f, path))
    while not pq.empty():
        # print("path", path)
        path = pq.get()[1]
        # input(path)
        current = path[-1]
        if current == end:
            return path

        for i in neighbours(current, grid, path):
            # if i == (17, 11, 3):
            #     print("path", path, "curr", current)
            #     print("dict thingy", grid.get(i))
            #     input(i)
            new_path = path + [i]
            # HEURISTIC
            g = len(new_path) + grid.get(i)[1]
            f = g + heuristic(i, end)
            if i not in visited:
                pq.put((f, new_path))
                visited.add(i)


    return False

def a_star_basic(start, end, grid):
    pq = PriorityQueue()
    # print("START2", type(start))
    # print("IZHAR", grid)
    path = [start]
    # print("JOEJOE", heuristic(path[-1], end))
    # print("joe3,", path)
    # input(grid.get(path[-1]))
    f = 0 + heuristic(path[-1], end)

    visited = set()

    pq.put((f, path))

    while not pq.empty():
        path = pq.get()[1]
        current = path[-1]
        if current == end:
            return path

        for i in neighbours(current, grid, path):
            new_path = path + [i]
            f = len(new_path) + heuristic(i, end)
            if i not in visited:
                pq.put((f, new_path))
                visited.add(i)

    return False


def make_grid(gates):
    if len(gates) == 25:
        y_range = 13
    else:
        y_range = 17

    grid = {}
    for x in range(18):
        for y in range(y_range):
            for z in range(8):
                # HEURISTIC
                g = (8 - z) * 2

                grid[(x, y, z)] = [True, g]
     
    return grid
