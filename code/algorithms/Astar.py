##################################################
# Astar_2.py
# 
# By team De Madarijntjes
# 
# Pseudocode source: http://mat.uab.cat/~alseda/MasterOpt/AStar-Algorithm.pdf
##################################################
import time
from operator import attrgetter

class Grid():
    def __init__(self):
        self.grid = []
        self.g = 0

    def make_grid(self, blocked, start, goal, net):
        # start_time_1 = time.time()
        for x in range(-1, 5):
            for y in range(-1, 5):
                for z in range(8):
                    node = Node(x, y, z, net)
                    # if str(node) not in blocked:
                    #     self.grid.append(node)
                    # else: 
                    #     self.grid.append(node).
                    self.grid.append(node)
                    if str(node) in blocked and str(node) != str(start) and str(node) != str(goal):
                        node.set_blocked()
        
        # end_time_1 = time.time()
        # print("TIME 1: ", end_time_1 - start_time_1)

    def get_grid(self):
        return self.grid
        

class Node():
    def __init__(self, x, y, z, net):
        self.x = x
        self.y = y
        self.z = z
        self.net = net
        self.g = 0
        self.blocked = False
        self.parent = None

    def get_blocked(self):
        return self.blocked

    def set_blocked(self):
        self.blocked = True
        
    def set_f(self):
        self.f = self.g + self.h

    def get_f(self):
        return self.f

    def get_coordinate(self):
        return str([self.x, self.y, self.z])
    
    def get_g(self):
        return self.g
    
    def set_g(self, value):
        # Heuristic to let the program prefer higher layers
        # self.g = value + 8 - self.z
        self.g = value
    
    def set_h(self, current, goal):
        self.h = abs(current.x - goal.x) + abs(current.y - goal.y) + abs(current.z - goal.z)
        
        return self.h
    
    def set_parent(self, node):
        self.parent = node
    
    def get_parent(self):
        return self.parent

    def successors(self, grid, node_current, closed_list, blocked, start, goal):
        self.node_successors = set()
        
        # grid maken waar blocked niet in zit 

        for i in grid:
            for j in grid:
                if i.x == node_current.x and i.y == node_current.y and i.z == node_current.z:
                    if abs(j.x - i.x) == 1 and j.y - i.y == 0 and j.z - i.z == 0:   
                        if j not in closed_list and str(j) != str(start):
                            if not j.get_blocked():
                                self.node_successors.add(j)
                    elif abs(j.y - i.y) == 1 and j.x - i.x == 0 and j.z - i.z == 0:
                        if j not in closed_list and str(j) != str(start):
                            if not j.get_blocked():
                                self.node_successors.add(j)
                    elif abs(j.z - i.z) == 1 and j.x - i.x == 0 and j.y - i.y == 0:
                        if j not in closed_list and str(j) != str(start):
                            if not j.get_blocked():
                                self.node_successors.add(j)
        
        return self.node_successors

    def __repr__(self):
        return str([self.x, self.y, self.z])


def search(open_list, closed_list, blocked, grid, start, goal):
    # print(open_list, closed_list, blocked, start, goal)
    # input()

    while open_list:
        # start_time_3 = time.time()
        # f_list = []
        # for i in open_list:
        #     f_list.append(i.f_score())
        # minimum = min(f_list)
        # for i in range(len(f_list)):
        #     if f_list[i] == minimum:
        #         q = open_list[i]

        # Kan sneller
        for i in open_list:
            i.set_f()

            # snellere code als start automatisch 1 omhoog gaat?
            
        q = min(open_list, key=attrgetter('f'))
        
        # end_time_3 = time.time()
        # print("TIME 3: ", end_time_3 - start_time_3)

        if str(q) == str(goal):
            print("finished")
            break
        
        # start_time_4 = time.time()
        successors = q.successors(grid, q, closed_list, blocked, start, goal)
        # end_time_4 = time.time()
        # print("TIME 4: ", end_time_4 - start_time_4)
        # print("Q", q, successors)

        
        # Om code sneller te maken: Forceer hem naar boven als z + 1 kan en x en y hetzelfde zijn als start
        # if q.x == start.x and q.y == start.y and q.z != start.z:
        #     pass
        # for i in successors:
        #     if i.x == start.x and i.y == start.y:
        #         continue
        #     else:
        #         successors.remove(i)


        # Dit maakt hem slomer
        # if q.z < 6 and q.x == start.x and q.y == start.y:
        #     successors = [item for item in successors if item.x == start.x and item.y == start.y]

        # print("Q", q, successors)
        for i in successors:
            # if i.x == start.x and i.y == start.y:
            # start_time_5 = time.time()
            
            

            # Make it more expensive to traverse the x or y axis on lower layers
            weight = 1
            if i.x != q.x or i.y != q.y:
                weight += 8 - q.z


            successor_current_cost = q.get_g() + weight
            # end_time_5 = time.time()
            # print("TIME 5: ", end_time_5 - start_time_5)

            # start_time_6 = time.time()
            if i in open_list:
                if i.get_g() <= successor_current_cost:
                    i.set_g(successor_current_cost)
                    i.set_parent(q)    

            elif i in closed_list:
                if i.get_g() <= successor_current_cost:
                    # print("2")
                    break
                # print("3")
                closed_list.remove(i)
                open_list.append(i)
            
            else:
                # print("4")
                open_list.append(i)
                i.set_h(i, goal)
            # end_time_6 = time.time()
            # print("TIME 6: ", end_time_6 - start_time_6)
            # A star werkt niet als alles dezelfde kost heeft toch een stap terug moet extra kosten hebben doordat de huristiek daar groter wordt.
            # print("plus 1:::: ", successor_current_cost, i.h, i)
            
            i.set_g(successor_current_cost)
            i.set_parent(q)    
         
        open_list.remove(q)
        closed_list.append(q)
        
        # input()
        
    return q

def generate_path(crd):
    path = [crd]

    while crd.get_parent() != None:
        crd = crd.get_parent()
        path.append(crd)

    return path

def initialize_grid(blocked, start, goal, net):
    grid = Grid()
    grid.make_grid(blocked, start, goal, net)
    return grid.get_grid()

def a_star(start, goal, blocked, net):
    # Set start and goal
    start = Node(start[0], start[1], start[2], net)
    goal = Node(goal[0], goal[1], goal[2], net)
    print(start, goal)

    # Initialize the grid for program to run on
    grid = initialize_grid(blocked, start, goal, net)

    # Calculate h for start node
    start.set_h(start, goal)

    print(start.h)

    # Create lists to keep track of open nodes, closed nodes, and previous nodes for optimal path
    open_list = [start]

    closed_list = []
    # start_time_2 = time.time()
    q =  search(open_list, closed_list, blocked, grid, start, goal)
    # end_time_2 = time.time()
    # print("TIME 2: ", end_time_2 - start_time_2)
    
    return generate_path(q)

# print(a_star())
