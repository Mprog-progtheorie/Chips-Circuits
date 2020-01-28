from code.visualisation import plot as plot
from code.classes import classes as classs                 
from code.algorithms import Astar2 as Astar
import copy
import matplotlib.pyplot as plt
import time
import csv
import random
import sys

def main():
    # Setted high so can never break a solvable algorithm if not entered
    number_of_solutions = 1000
    print("Welcome to our case Chips and Circuits! By De Mandarijntjes \n --------------------------")
    net_option = input("Please enter a number from 1 to 6 to choose a netlist: ")
    if int(net_option) > 2: 
        number_of_solutions = input("You have entered a netlist that this algorithm cannot solve please enter the max number of different solutions you want to give the algorithm: ")
    
    while True:
        bool_input = input("Do you want to use the hill climber over the end result algorithm? Y/N ")
        if bool_input.capitalize() == "Y" or bool_input.capitalize() == "Yes":
            hill_climb_bool = True
            break
        else:
            hill_climb_bool = False
            break

    return net_option, number_of_solutions, hill_climb_bool

if __name__ == '__main__':
    net_option, number_of_solutions, hill_climb_bool = main()
    start_time = time.time()

    if int(net_option) <= 3:
        netliststring = "data/" + "netlist_" + net_option + ".csv"
        printstring = "data/" + "print_1" + ".csv"
    elif int(net_option) <= 6:
        netliststring = "data/" + "netlist_" + net_option + ".csv"
        printstring = "data/" + "print_2" + ".csv"
   
    # Create netlist by loading file in class
    netlist = classs.Netlist(netliststring).netlist

    # Create list for gate coordinates
    gate_coordinates = classs.Gate_coordinate(printstring).gate_coordinates

    
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
    
    # HEURISTIC
    for max_number in range(len(distances)-1, -1, -1):
        swapped = False
        for count in range(max_number):
            if distances[count][1] > distances[count + 1][1]:
                distances[count], distances[count + 1] = distances[count + 1], distances[count]
                swapped = True
        if not swapped:
            break
    
    
    count = 1

    ceiling_counter = 2

    results = {}
    while count == 1:
        count = 0

        gate_connections = {}

        
        # string_gates = [] 
        
        grid = Astar.make_grid(gate_coordinates)
        temp_path = list()
        for gate_coo in gate_coordinates:
            grid[tuple(gate_coo)][0] = False

            # HEURISTIC
            gate_neighbours_list = Astar.gate_neighbours(tuple(gate_coo), grid, temp_path)
            for neighbour in gate_neighbours_list:
                grid.get(neighbour)[1] += 25

        blocking_wires = []
        # random.shuffle(distances)
        for chips in distances:
            gate_start = int(chips[0][0])
            gate_end = int(chips[0][1])
            manhatten_length = chips[1]


            connected_gate = (gate_start, gate_end)

            coordinate_begin = gate_coordinates[gate_start - 1]
            coordinate_end = gate_coordinates[gate_end - 1]

            grid[tuple(coordinate_begin)][0] = True
            grid[tuple(coordinate_end)][0] = True
            
            search = Astar.a_star(tuple(coordinate_begin), tuple(coordinate_end), grid, ceiling_counter)
            ceiling_counter += 1

            if ceiling_counter == 8:
                ceiling_counter = 2
            # print("SEARCH: ",search, connected_gate) 
            
            try:
                for crd in search:
                    grid[crd][0] = False
                gate_connections.update({connected_gate: search})
            except:
                blocking_wires.append((connected_gate, manhatten_length))
                # break

        
           
        #    HEURISTIC
        if len(blocking_wires) != 0:
            newnetlist = []
            for blocking_wire in blocking_wires:
                if blocking_wire in distances:
                    distances.remove(blocking_wire)
                    newnetlist.append(blocking_wire)
            
            # random.shuffle(newnetlist)
            for net in distances:
                newnetlist.append(net)
            distances = newnetlist

            count = 1
            wires_length = 0
            # Calculate total length of wires
            for key in gate_connections:
                wire = gate_connections[key]
                wires_length = wires_length + len(wire)
            
            print("RESULTSLEN: ", len(results))
            if len(results) >= int(number_of_solutions):
                results.update({len(gate_connections)  : (wires_length, gate_connections)})
                break
            print("Wires of solution: ",len(gate_connections), "Length:", wires_length)
            print("BLOCKING WIRES: ", blocking_wires)
            print()
            results.update({len(gate_connections)  : (wires_length, gate_connections)})
        else: 
            results.update({len(gate_connections)  : (wires_length, gate_connections)})
            print("FINISHED NETLIST")


    if hill_climb_bool:
        new_wires_list = []
        for gate_connection in gate_connections:
            wire = gate_connections[gate_connection]
            original_wirelength = len(wire)
            for crd in wire:
                grid[crd][0] = True
            
            newpath = Astar.a_star_basic(tuple(gate_coordinates[(gate_connection[0] - 1)]), tuple(gate_coordinates[(gate_connection[1] - 1)]), grid)
            if newpath:
                if len(newpath) < len(wire):
                    # print("YES ERRASE")
                    new_wires_list.append((gate_connection, newpath))
                    for crd in newpath:
                        grid[crd][0] = False
                else: 
                    for crd in wire:
                        grid[crd][0] = False
        print("number of reroutes for better solution", len(new_wires_list))
        for new_wire in new_wires_list:
            del gate_connections[new_wire[0]]
            gate_connections.update({new_wire[0] : new_wire[1]})

    gate_connections = results[max(results, key=int)][1]
    ax = plot.make_grid(8, 17)
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
    
    with open('output/Astar_output.csv', mode= 'w') as outputfile:
        output_writer = csv.writer(outputfile, delimiter= ',')

        for keys in gate_connections:
            output_writer.writerow([keys, gate_connections[keys]])