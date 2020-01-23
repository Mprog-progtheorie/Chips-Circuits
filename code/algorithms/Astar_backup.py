##################################################
# Astar_2.py
# 
# By team De Madarijntjes
# 
# Pseudocode source: http://mat.uab.cat/~alseda/MasterOpt/AStar-Algorithm.pdf
##################################################
class Grid():
    def __init__(self):
        self.grid = []
        self.g = 0

    def make_grid(self):
        for x in range(-1, 17):
            for y in range(-1, 12):
                for z in range(8):
                    self.grid.append(Node(x, y, z))
    
    def get_grid(self):
        return self.grid
        

class Node():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.g = 0
        self.parent = None

    def f_score(self):
        return self.g + self.h
    
    def get_g(self):
        return self.g
    
    def set_g(self, value):
        self.g = value
    
    def g_score(self, value):
        self.g += value
    
    def h_score(self, current, goal):
        self.h = abs(current.x - goal.x) + abs(current.y - goal.y) + abs(current.z - goal.z)
        
        return self.h
    
    def set_parent(self, node):
        self.parent = node
    
    def get_parent(self):
        return self.parent

    def successors(self, grid, node_current, blocked, start):
        self.node_successors = []

        for i in grid:
            for j in grid:
                if i.x == node_current.x and i.y == node_current.y and i.z == node_current.z:
                    if abs(j.x - i.x) == 1 and j.y - i.y == 0 and j.z - i.z == 0:   
                        if j not in blocked and str(j) != str(start): 
                            self.node_successors.append(j)
                    elif abs(j.y - i.y) == 1 and j.x - i.x == 0 and j.z - i.z == 0:
                        if j not in blocked and str(j) != str(start):
                            self.node_successors.append(j)
                    elif abs(j.z - i.z) == 1 and j.x - i.x == 0 and j.y - i.y == 0:
                        if j not in blocked and str(j) != str(start):
                            self.node_successors.append(j)
                    
        print("blocked", blocked)
        return self.node_successors

    def __repr__(self):
        return str([self.x, self.y, self.z])


def search(open_list, closed_list, grid, start, goal):
    

    while open_list:
        f_list = []
        for i in open_list:
            f_list.append(i.f_score())
        minimum = min(f_list)
        for i in range(len(f_list)):
            if f_list[i] == minimum:
                q = open_list[i]
        
        if str(q) == str(goal):
            print("finished")
            break

        successors = q.successors(grid, q, closed_list, start)
        
        node_previous = q
            

        for i in successors:

            # Set successor_current_cost = g(node_current) + w(node_current, node_successor)
            successor_current_cost = q.get_g() + 1
            if i in open_list:
                if i.get_g() <= successor_current_cost:
                    break

            elif i in closed_list:
                if i.get_g() <= successor_current_cost:
                    break
                closed_list.remove(i)
                open_list.append(i)
            
            else:
                open_list.append(i)
                i.h_score(i, goal)
            
            i.set_g(successor_current_cost)
            i.set_parent(q)
        
        open_list.remove(q)
        closed_list.append(q)
        print("closed12212", closed_list)
    return q

def generate_path(crd):
    path = [crd]

    while crd.get_parent() != None:
        crd = crd.get_parent()
        path.append(crd)

    return path

def initialize_grid():
    grid = Grid()
    grid.make_grid()
    return grid.get_grid()

def a_star(start, goal, wire_nodes):
    # Initialize the grid for program to run on
    grid = initialize_grid()

    # Set start and goal
    start = Node(start[0], start[1], start[2])
    goal = Node(goal[0], goal[1], goal[2])
    print(start, goal)

    # Calculate h for start node
    start.h_score(start, goal)

    print(start.h)

    # Create lists to keep track of open nodes, closed nodes, and previous nodes for optimal path
    open_list = [start]
    closed_list = []
    for i in wire_nodes:
        closed_list.append(i)

    q =  search(open_list, closed_list, grid, start, goal)
    
    return generate_path(q)

# print(a_star())
