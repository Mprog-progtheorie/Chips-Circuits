from queue import PriorityQueue
import numpy as np
import time

def heuristic(current, goal):
    x = abs(np.array(current) - np.array(goal))
    return x.sum()

def neighbours(current, grid, path):
    neighbours = list()

    # kan in for loop
    moves = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

    for i in moves:
        neighbour = tuple(np.array(current) + np.array(i))
        # print(type(neighbour))
        # if neighbour not in set(path):
        if neighbour not in path:
            if neighbour in grid:
                if grid[neighbour]:
                    # print(grid[neighbour])
                    neighbours.append(neighbour)

    return neighbours

def a_star(start, end, grid):
    pq = PriorityQueue()

    path = [start]
    for i in range(8):
        force_up = list(path[-1])
        force_up[2] = i
        force_up = tuple(force_up)
        if grid[force_up]:
            path.append(force_up)
        else:
            neighbour_list = neighbours(path[-1], grid, path)
            if neighbour_list:
                for neighbour in neighbour_list:
                    path.append(neighbour)
                    break
            else:
                break
    f = 0 + heuristic(force_up, end)

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
<<<<<<< HEAD
 
    return False
=======

        # print(len(path))
>>>>>>> a3dcd50bba99dd6a84d48fbca19750c7958edced

    return False

def make_grid():
    grid = {}
    for x in range(17):
        for y in range(13):
            for z in range(8):
                grid[(x, y, z)] = True
     
    return grid

# start_time = time.time()
# grid = make_grid()


# start = (1, 1, 0)
# end = (1, 5, 0)
# search = a_star(start, end, grid)
# for crd in search:
#     grid[crd] = False
# print(search)


# start = (0, 2, 0)
# end = (2, 4, 0)
# search = a_star(start, end, grid)
# print(search)
# end_time = time.time()
# print("time", end_time - start_time) 
