from code.visualisation import plot as plot
from code.classes import classes as classs
from code.functions import DeleteNew as delete                     
from code.algorithms import Astar2 as Astar
import copy
import matplotlib.pyplot as plt
import time
import csv
import random

if __name__ == '__main__':
    start_time = time.time()
    # Create netlist by loading file in class
    netlist = classs.Netlist("data/example_net3.csv").netlist

    # Create list for gate coordinates
    gate_coordinates = classs.Gate_coordinate("data/example_prit3.csv").gate_coordinates

    
    distances = {}

    for item in netlist:
        gate_start = int(item.gate_1)
        gate_end = int(item.gate_2)

        # Create tuple for gates that have to be connected
        connected_gate = (gate_start, gate_end)

        coordinate_start = gate_coordinates[gate_start - 1]
        coordinate_end = gate_coordinates[gate_end - 1]

        x_coordinate_1 = int(coordinate_start[0])
        y_coordinate_1 = int(coordinate_start[1])

        x_coordinate_2 = int(coordinate_end[0])
        y_coordinate_2 = int(coordinate_end[1])

        # Calculate total shortest distance between gates
        total_dist = abs(x_coordinate_1 - x_coordinate_2) + abs(y_coordinate_1 - y_coordinate_2)

        distances.update({connected_gate: total_dist})

    # Sort connections from smallest to largest distance in dictionary
    print(distances.items())
    distances = list(distances.items())
    
    for max_number in range(len(distances)-1, -1, -1):
        swapped = False
        for count in range(max_number):
            if distances[count][1] > distances[count + 1][1]:
                distances[count], distances[count + 1] = distances[count + 1], distances[count]
                swapped = True
        if not swapped:
            break
    
    
    count = 1
    
    while count == 1:
        count = 0

        gate_connections = {}

        
        # string_gates = [] 


       

        
        grid = Astar.make_grid()
        for gate_coo in gate_coordinates:
            grid[tuple(gate_coo)] = False

        blocking_wires = []
        # random.shuffle(distances)
        for chips in distances:
            gate_start = int(chips[0][0])
            gate_end = int(chips[0][1])
            manhatten_length = chips[1]


            connected_gate = (gate_start, gate_end)

            coordinate_begin = gate_coordinates[gate_start - 1]
            coordinate_end = gate_coordinates[gate_end - 1]

            grid[tuple(coordinate_begin)] = True
            grid[tuple(coordinate_end)] = True
            
            search = Astar.a_star(tuple(coordinate_begin), tuple(coordinate_end), grid)
            # print("SEARCH: ",search, connected_gate) 
            
            try:
                for crd in search:
                    grid[crd] = False
                gate_connections.update({connected_gate: search})
            except:
                blocking_wires.append((connected_gate, manhatten_length))
                # break
           
        
        
        if len(blocking_wires) != 0:
            newnetlist = []
            for blocking_wire in blocking_wires:
                if blocking_wire in distances:
                    distances.remove(blocking_wire)
                    newnetlist.append(blocking_wire)
            
            random.shuffle(newnetlist)
            for net in distances:
                newnetlist.append(net)
            distances = newnetlist

            count = 1

            # if len(gate_connections) > 39:
            #     print("FINISHED TROUGH BREAK")
            #     break
            
            

    ax = plot.make_grid(8, 5)
    for gate_coordinate in gate_coordinates: 
        # blocked.append(Astar.Node(gate_coordinate[0], gate_coordinate[1], gate_coordinate[2]).set_blocked())
        plot.set_gate(gate_coordinate, ax)
    print("WIRES: ",len(gate_connections))

    length = 0
    # Calculate total length of wires
    for key in gate_connections:
        wire = gate_connections[key]
        length = length + len(wire)
        
    print("TOTAL LENGTH")
    print(length)
    

    end_time = time.time()
    print("TIME: ", end_time - start_time)

    allConnections = []
    colours = ['b', 'darkblue', 'k', 'green', 'cyan','m','yellow','lightgreen', 'pink']
    colourcounter = 0
    for keys in gate_connections:
        allConnections = gate_connections[keys]
        # print(len(allConnections))
        allconnectionlist = []
        for listconnection in allConnections: 
            allconnectionlist.append(listconnection)
        if colourcounter < 6:
            colourcounter += 1
        else: 
            colourcounter = 0

        for i in range(len(allconnectionlist)):
            try: 
                plot.draw_line(allconnectionlist[i], allconnectionlist[i + 1], colours[colourcounter], ax)
            except: 
                break 

    plt.show()