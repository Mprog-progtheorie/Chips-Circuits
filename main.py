from code.visualisation import plot as plot
from code.classes import classes as classs                 
from code.algorithms import Astar as Astar
import copy
import matplotlib.pyplot as plt
import time
import csv
import random
import sys

def main():
    """
    Set high so can never break a solvable algorithm if not entered
    """
    number_of_solutions = 1000
    print("Welcome to our case Chips and Circuits! By De Mandarijntjes \n --------------------------")
    net_option = input("Please enter a integer from 1 to 6 to choose a netlist: ")
    if net_option.isnumeric():
        if int(net_option) > 2: 
            number_of_solutions = input("You have entered a netlist that this algorithm cannot solve please enter the max number of different solutions you want to give the algorithm: ")
            if number_of_solutions.isnumeric():
                while int(number_of_solutions) > 10 or int(number_of_solutions) < 0:
                    number_of_solutions = input("Please enter a integer inbetween the 0 and 10: ")
            else: 
                print("Please enter a integer")
                sys.exit()  
    else:
        print("Please enter a integer")
        sys.exit() 

    while True:
        bool_input = input("Do you want to use the hill climber over the end result algorithm? Y/N ")
        if bool_input.capitalize() == "Y" or bool_input.capitalize() == "Yes":
            hill_climb_bool = True
            break
        else:
            hill_climb_bool = False
            break

    return net_option, number_of_solutions, hill_climb_bool

def generate_distances(netlist, gate_coordinates):
    """
    Make a dictionary of all gates with the calculated distances between them.
    """
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

    return distances
if __name__ == '__main__':
    net_option, number_of_solutions, hill_climb_bool = main()
    start_time = time.time()

    # Get the user input to load the neetlist en print csv
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

    
    distances = generate_distances(netlist, gate_coordinates)

    # Sort connections from smallest to largest distance in dictionary
    print(distances.items())
    distances = list(distances.items())
    
    # Sort netlist by manhatten distance
    for max_number in range(len(distances)-1, -1, -1):
        swapped = False
        for count in range(max_number):
            if distances[count][1] > distances[count + 1][1]:
                distances[count], distances[count + 1] = distances[count + 1], distances[count]
                swapped = True
        if not swapped:
            break
     
    count = 1
    results = {}

    while count == 1:
        count = 0

        gate_connections = {}
        
        # Make the grid for Astar
        grid = Astar.make_grid(gate_coordinates)
        temp_path = list()
        for gate_coo in gate_coordinates:
            grid[tuple(gate_coo)][0] = False

            # Make it more expensive to near or above gates
            gate_neighbours_list = Astar.gate_neighbours(tuple(gate_coo), grid, temp_path)
            for neighbour in gate_neighbours_list:
                grid.get(neighbour)[1] += 25

        blocking_wires = list()

        for chips in distances:

            # Initialize the start and end nodes
            gate_start = int(chips[0][0])
            gate_end = int(chips[0][1])
            manhatten_length = chips[1]

            connected_gate = (gate_start, gate_end)

            coordinate_begin = gate_coordinates[gate_start - 1]
            coordinate_end = gate_coordinates[gate_end - 1]

            # Set the grid on True for the gates so Astar works
            grid[tuple(coordinate_begin)][0] = True
            grid[tuple(coordinate_end)][0] = True
            
            # Call the A star search algorithm
            search = Astar.a_star(tuple(coordinate_begin), tuple(coordinate_end), grid)
            
            # If wire has been made set the grid on False for the net
            try:
                for crd in search:
                    grid[crd][0] = False
                gate_connections.update({connected_gate: search})
            except:
                blocking_wires.append((connected_gate, manhatten_length))
        
           
        #  Check if the netlist has been solved
        if len(blocking_wires) != 0:

            # Enter the conflictingwires in the front of the netlist
            newnetlist = list()

            for blocking_wire in blocking_wires:
                if blocking_wire in distances:
                    distances.remove(blocking_wire)
                    newnetlist.append(blocking_wire)
            
            for net in distances:
                newnetlist.append(net)
            distances = newnetlist

            count = 1
            wires_length = 0

            # Calculate total length of wires 
            for key in gate_connections:
                wire = gate_connections[key]
                wires_length = wires_length + len(wire)
            
            # Print the results for the generated solution add them to the results dict
            print("Number of different results: ", len(results))
            if len(results) >= int(number_of_solutions):
                results.update({len(gate_connections)  : (wires_length, gate_connections)})
                break
            print("Wires of solution: ",len(gate_connections), "Length:", wires_length)
            print("BLOCKING WIRES: ", len(blocking_wires))
            print()
            # Add the solution to the results dictionary
            results.update({len(gate_connections)  : (wires_length, gate_connections)})
        else: 
            # Add the solved netlist to the results dictionary
            results.update({len(gate_connections)  : (wires_length, gate_connections)})
            print("FINISHED NETLIST")

    # Hill climber over the generated solution
    if hill_climb_bool:
        # Make a list for the wires that should be rerouted
        new_wires_list = list()
        # Set the grid on True for the wire coordinates in the solution
        for gate_connection in gate_connections:
            wire = gate_connections[gate_connection]
            original_wirelength = len(wire)
            for crd in wire:
                grid[crd][0] = True
            
            # Run Astar to return a new path
            newpath = Astar.a_star_basic(tuple(gate_coordinates[(gate_connection[0] - 1)]), tuple(gate_coordinates[(gate_connection[1] - 1)]), grid)
            
            # Check if Astar found a solution and check if the new solution is better
            if newpath:
                if len(newpath) < len(wire):
                    new_wires_list.append((gate_connection, newpath))
                    for crd in newpath:
                        grid[crd][0] = False
                else: 
                    for crd in wire:
                        grid[crd][0] = False
        print("Number of reroutes for better solution", len(new_wires_list))
        # Append the new wires that had a shorter length
        for new_wire in new_wires_list:
            del gate_connections[new_wire[0]]
            gate_connections.update({new_wire[0] : new_wire[1]})

    # Get the best result
    gate_connections = results[max(results, key=int)][1]
    print("Connections: ",len(gate_connections))

    # Make grid for plot
    ax = plot.make_grid(8, 17)

    # Plot the gate_coordinates
    for gate_coordinate in gate_coordinates: 
        plot.set_gate(gate_coordinate, ax)
   
    # Calculate total length of wires
    length = 0
    for key in gate_connections:
        wire = gate_connections[key]
        length = length + len(wire)
        
    print("TOTAL LENGTH: ", length)
    
    # Calculate the runtime and print it out
    end_time = time.time()
    print("RUNTIME: ", end_time - start_time)

    # Plot out all the wires of the solution
    allConnections = list()
    colours = ['b', 'darkblue', 'k', 'green', 'cyan','m','yellow','lightgreen', 'pink']
    colourcounter = 0
    for keys in gate_connections:
        allConnections = gate_connections[keys]
        allconnectionlist = list()
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
    # Show the plot
    plt.show()
    
    # Print out the solution in a csv
    with open('output/Astar_output.csv', mode= 'w') as outputfile:
        output_writer = csv.writer(outputfile, delimiter= ',')
        for keys in gate_connections:
            output_writer.writerow([keys, gate_connections[keys]])