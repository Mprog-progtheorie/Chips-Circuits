"""
linespacer_ydirection.py

Tom Kamstra, Izhar Hamer, Julia Linde

Finds the optimal paths between gates based on distance in y-direction.
Deletes wires that are out of range.
"""
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("../code")
from classes import classes as classs
from functions import delete as delete
from functions import change_coordinates as change
import csv

# Create netlist by loading file in class
netlist = classs.Netlist("../data/netlist_1.csv").netlist

# Create list for gate coordinates
gate_coordinates = classs.Gate_coordinate("../data/pritn_1.csv").gate_coordinates

# Create dictionary for gate connections with corresponding shortest distance
distances = {}

for item in netlist:
    gate_start = int(item.gate_1)
    gate_end = int(item.gate_2)
    
    # Create tuple for gates that have to be connected
    connected_gate = (gate_start, gate_end)
    
    # Define coordinates of start and end gate
    coordinate_start = gate_coordinates[gate_start - 1]
    coordinate_end = gate_coordinates[gate_end - 1]
    
    # Define y coordinates for start and end gate
    y_coordinate_start = int(coordinate_start[1])
    y_coordinate_end = int(coordinate_end[1])

    # Calculate total shortest distance between gates
    y_dist = abs(y_coordinate_start - y_coordinate_end)

    distances.update({connected_gate: y_dist})

# Sort connections from smallest to largest distance in dictionary
distances = list(distances.items())
for max_number in range(len(distances)-1, -1, -1):
    swapped = False
    for index in range(max_number):
        if distances[index][1] > distances[index + 1][1]:
            distances[index], distances[index + 1] = distances[index + 1], distances[index]
            swapped = True
    if not swapped:
        break

# Create dictionary of wires with connected gates
gate_connections = {}

# Variable that counts connected gates
count = 0

# Saves all wires
allwires = []

# Define variable for deleted wires that are not created again
minus_num_wires = 0

# Define number for maximum number of layers
max_num_layers = 7

# Define number of new wires that are still created in same direction
num_newwires = 5

# Define minimum number of wires length for which wire can be checked on double coordinates
minimum_wireslength = 4

# Define number for which wire can be deleted and thus is too long
deleting_length = 75

# Define number for maximum length of wire
max_wirelength = 100

# Define step_x and step_y as 0 from the beginning
step_x = 0
step_y = 0

# Connect gates with eachother, starting with smallest distance
for chips in distances:
    gate_start = int(chips[0][0])
    gate_end = int(chips[0][1])
    
    connected_gate = (gate_start, gate_end)

    coordinate_begin = gate_coordinates[gate_start - 1]
    coordinate_end = gate_coordinates[gate_end - 1]
    
    # Define x, y and z coordinates of start and end gate
    x_coordinate_start = int(coordinate_begin[0])
    y_coordinate_start = int(coordinate_begin[1])
    z_coordinate_start = int(coordinate_begin[2])

    x_coordinate_end = int(coordinate_end[0])
    y_coordinate_end = int(coordinate_end[1])
    z_coordinate_end = int(coordinate_end[2])

    # Create list for wire coordinates
    wires = []

    # Define all 5 coordinates that surround current start coordinate
    x_coordinate_startcheck = x_coordinate_start + 1
    coordinate_1 = [x_coordinate_startcheck, y_coordinate_start, z_coordinate_start]
    x_coordinate_startcheck2 = x_coordinate_start - 1
    coordinate_2 = [x_coordinate_startcheck2, y_coordinate_start, z_coordinate_start]
    y_coordinate_startcheck = y_coordinate_start + 1
    coordinate_3 = [x_coordinate_start, y_coordinate_startcheck, z_coordinate_start]
    y_coordinate_startcheck2 = y_coordinate_start - 1
    coordinate_4 = [x_coordinate_start, y_coordinate_startcheck2, z_coordinate_start]
    z_coordinate_startcheck = z_coordinate_start + 1
    coordinate_5 = [x_coordinate_start, y_coordinate_start, z_coordinate_startcheck]
    
    # Save all coordinates around current start coordinate in list
    coordinate_check = [coordinate_1, coordinate_2, coordinate_3, coordinate_4, coordinate_5]
    
    # Creates list for all coordinates that are already occupied
    all_coordinates = []
    for coordnt in allwires:
        all_coordinates.append(coordnt.get_coordinate())

    # Checks whether wire can move in any direction, if at least one coordinate around current coordinate is free
    if all(elem in all_coordinates for elem in coordinate_check):
        for coor in coordinate_check:
            for item_start in allwires:
                if item_start.coordinate == coor and item_start.net[0] != gate_start and item_start.net[1] != gate_start:
                    # Delete one wire around start gate that has no connection with start gate if all surrounded coordinates are occupied
                    (wires, x_coordinate_start, y_coordinate_start, z_coordinate_start, coordinate, gate_connections, allwires) = delete.delete_wire(wires, coordinate_begin, item_start.net, distances, gate_connections, allwires)
                    break
    
    # Create switch variable to switch start moving direction
    if count > len(netlist) + num_newwires:
        # Reconnect deleted wires in switched direction
        switch_variable = 0
    else:
        switch_variable = 1
    
    # Overwrite coordinate but save coordinate_begin in different variable
    coordinate = coordinate_begin
    
    # Checks whether wire is created too often and will probably never connect
    connection_checker = 0
    
    while coordinate != coordinate_end:
        # Determine direction in which wire has to move
        if x_coordinate_start > x_coordinate_end:
            step_x = -1
        elif x_coordinate_start < x_coordinate_end:
            step_x = 1

        if y_coordinate_start > y_coordinate_end:
            step_y = -1
        elif y_coordinate_start < y_coordinate_end:
            step_y = 1
 
        # Append start coordinate to wire
        wires.append(coordinate)
        wire = classs.Wire(coordinate, connected_gate)
        allwires.append(wire)
        
        if switch_variable == 0:
            # Loop until x-coordinate from start gate equals x-coordinate from end gate
            while x_coordinate_start != x_coordinate_end:
                # Redefine coordinate by moving in different directions and check whether coordinate is available
                x_coordinate_start = x_coordinate_start + step_x
                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                # Check for other gates or other wires
                if gate_connections:
                    (x_coordinate_start, z_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, x_coordinate_start, -step_x, z_coordinate_start, 1)
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    (z_coordinate_start, y_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, z_coordinate_start, -1, y_coordinate_start, step_y)
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    # Coordinate changes 2 times in y-direction, so step_y is doubled
                    (y_coor_notrelevant, y_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, step_y, y_coordinate_start, (-2*step_y))
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    (y_coordinate_start, x_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, step_y, x_coordinate_start, -step_x)
                elif coordinate in gate_coordinates and coordinate != coordinate_end:
                    x_coordinate_start = x_coordinate_start - step_x
                    z_coordinate_start = z_coordinate_start + 1
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    (z_coordinate_start, x_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, z_coordinate_start, -1, x_coordinate_start, -step_x)
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    (x_coordinate_start, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, step_x, y_coordinate_start, step_y)
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    # Coordinate changes 2 times in y-direction, so step_y is doubled
                    (y_coor_notrelevant, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, y_coordinate_start, step_y, y_coordinate_start, (-2*step_y))
        
                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                wires.append(coordinate)
                wire = classs.Wire(coordinate, connected_gate)
                allwires.append(wire)
            
            # Redefine step in direction of y-coordinate
            if y_coordinate_start < y_coordinate_end:
                step_y = 1
            elif y_coordinate_start > y_coordinate_end:
                step_y = -1
            
            # Change z-coordinate if x- and y-coordinates are same as those from end gate
            if x_coordinate_start == x_coordinate_end and y_coordinate_start == y_coordinate_end:
                while z_coordinate_start != z_coordinate_end:
                    # Redefine coordinate by moving in different directions and check whether coordinate is available
                    z_coordinate_start = z_coordinate_start - 1
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    if gate_connections:
                        (z_coordinate_start, y_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, z_coordinate_start, 1, y_coordinate_start, step_y)
                        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                        (y_coordinate_start, x_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, -step_y, x_coordinate_start, step_x)
                        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                        (x_coor_notrelevant, x_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, x_coordinate_start, step_x, x_coordinate_start, (-2*step_x))
                        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                        (x_coordinate_start, y_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, x_coordinate_start, step_x, y_coordinate_start, -step_y)
                    elif coordinate in gate_coordinates and coordinate != coordinate_end:
                        z_coordinate_start = z_coordinate_start + 1
                        y_coordinate_start = y_coordinate_start + step_y
                        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                        (x_coordinate_start, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, step_x, y_coordinate_start, -step_y)
                        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                        (x_coor_notrelevant, x_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, step_x, x_coordinate_start, (-2*step_x))
                        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                        (x_coordinate_start, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, step_x, y_coordinate_start, -step_y)
         
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    wires.append(coordinate)
                    wire = classs.Wire(coordinate, connected_gate)
                    allwires.append(wire)
                    
        # Redefine step in direction of y-coordinate    
        if y_coordinate_start < y_coordinate_end:
            step_y = 1
        elif y_coordinate_start > y_coordinate_end:
            step_y = -1
        
        # Loop until y-coordinate from start gate equals y-coordinate from end gate
        while y_coordinate_start != y_coordinate_end:
            # Redefine coordinate by moving in different directions and check whether coordinate is available
           y_coordinate_start = y_coordinate_start + step_y
           coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
           # Check for other gates or other wires
           if gate_connections:
               (y_coordinate_start, z_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, -step_y, z_coordinate_start, 1)
               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
               (z_coordinate_start, x_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, z_coordinate_start, -1, x_coordinate_start, step_x)
               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
               (x_coor_notrelevant, x_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, x_coordinate_start, step_x, x_coordinate_start, (-2*step_x))
               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
               (x_coordinate_start, y_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, x_coordinate_start, step_x, y_coordinate_start, -step_y)
           elif coordinate in gate_coordinates and coordinate != coordinate_end:
               y_coordinate_start = y_coordinate_start - step_y
               z_coordinate_start = z_coordinate_start + 1
               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
               (x_coordinate_start, z_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, step_x, z_coordinate_start, -1)
               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
               (x_coor_notrelevant, x_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, step_x, x_coordinate_start, (-2*step_x))
               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
               (x_coordinate_start, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, step_x, y_coordinate_start, -step_y)

           # Reset switch variable to be able to move in x-direction
           switch_variable = 0
           
           coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
           wires.append(coordinate)
           wire = classs.Wire(coordinate, connected_gate)
           allwires.append(wire)
           
           # Redefine step in direction of y-coordinate
           if y_coordinate_start < y_coordinate_end:
               step_y = 1
           elif y_coordinate_start > y_coordinate_end:
               step_y = -1
           
           # Change z-coordinate if x- and y-coordinates are same as those from end gate
           if x_coordinate_start == x_coordinate_end and y_coordinate_start == y_coordinate_end:
               while z_coordinate_start != z_coordinate_end:
                   # Redefine coordinate by moving in different directions and check whether coordinate is available
                   z_coordinate_start = z_coordinate_start - 1
                   coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                   if gate_connections:
                       (z_coordinate_start, x_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, z_coordinate_start, 1, x_coordinate_start, step_x)
                       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                       (x_coordinate_start, y_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, x_coordinate_start, -step_x, y_coordinate_start, step_y)
                       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                       (y_coor_notrelevant, y_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, step_y, y_coordinate_start, (-2*step_y))
                       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                       (y_coordinate_start, x_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, step_y, x_coordinate_start, -step_x)
                   elif coordinate in gate_coordinates and coordinate != coordinate_end:
                       z_coordinate_start = z_coordinate_start + 1
                       x_coordinate_start = x_coordinate_start + step_x
                       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                       (x_coordinate_start, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, -step_x, y_coordinate_start, step_y)
                       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                       (y_coor_notrelevant, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, y_coordinate_start, step_y, y_coordinate_start, (-2*step_y))
                       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                       (x_coordinate_start, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, -step_x, y_coordinate_start, step_y)
                                   
                   coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                   wires.append(coordinate)
                   wire = classs.Wire(coordinate, connected_gate)
                   allwires.append(wire)
                   
        # Check whether wire isn't running into forever loop
        if len(wires) > max_wirelength:
            # Delete one wire around end gate or delete one wire that is too long
            # Check every wire around end gate by redefining check_coordinate
            x_coordinate_check = x_coordinate_end + step_x
            (allwires, wires, gate_connections) = delete.delete_wires_maxlength(x_coordinate_check, y_coordinate_end, z_coordinate_end, allwires, gate_end, wires, coordinate_begin, distances, gate_connections, deleting_length)          
            x_coordinate_check = x_coordinate_end - step_x
            (allwires, wires, gate_connections) = delete.delete_wires_maxlength(x_coordinate_check, y_coordinate_end, z_coordinate_end, allwires, gate_end, wires, coordinate_begin, distances, gate_connections, deleting_length)
            y_coordinate_check = y_coordinate_end + step_y
            (allwires, wires, gate_connections) = delete.delete_wires_maxlength(x_coordinate_end, y_coordinate_check, z_coordinate_end, allwires, gate_end, wires, coordinate_begin, distances, gate_connections, deleting_length)
            y_coordinate_check = y_coordinate_end - step_y
            (allwires, wires, gate_connections) = delete.delete_wires_maxlength(x_coordinate_end, y_coordinate_check, z_coordinate_end, allwires, gate_end, wires, coordinate_begin, distances, gate_connections, deleting_length)
            z_coordinate_check = z_coordinate_end + 1
            (allwires, wires, gate_connections) = delete.delete_wires_maxlength(x_coordinate_end, y_coordinate_end, z_coordinate_check, allwires, gate_end, wires, coordinate_begin, distances, gate_connections, deleting_length)
                    
            # If no wire can be deleted and current wire can still not reach end gate
            wires = []
            x_coordinate_start = int(coordinate_begin[0])
            y_coordinate_start = int(coordinate_begin[1])
            z_coordinate_start = int(coordinate_begin[2])
            coordinate = coordinate_begin
            # Change value of switch variable to start moving in other direction
            switch_variable = 1
        else: 
            connection_checker += 1
        # Break if wire is created too often and will probably never connect
        if connection_checker > 2*max_wirelength:
            break
               
    # New connection is created
    count += 1
    
    wires_length = len(wires)
    
    # Delete part of wire when wire goes back and forth on one line
    if wires_length > minimum_wireslength:
        indices = []
        for count in range(wires_length-2):
            coor_1 = wires[count]
            coor_2 = wires[count + 1]
            coor_3 = wires[count + 2]

            # Save indices of wires list
            if coor_1 == coor_3:
                if count not in indices and (count + 1) not in indices:
                    indices.append(count)
                    indices.append(count + 1)
        
        # Delete wire coordinate with highest index first
        for delete_count in range(wires_length):
            for index in indices:
                if (wires_length - delete_count) == index:
                    wires.pop(index)
    
    net = classs.Net(gate_start, gate_end)
    net.create_wires(wires)
    gate_connections.update({connected_gate: wires})
    
    if len(gate_connections) >= len(netlist) - minus_num_wires:
        # Check whether every wire reaches end gate
        for net in netlist:
            start_gate = int(net.gate_1)
            end_gate = int(net.gate_2)
            
            if (start_gate, end_gate) in gate_connections.keys():
                select_conn = gate_connections[(start_gate, end_gate)]
                gate_net = (start_gate, end_gate)
                new_net = (end_gate, start_gate)
                end_coordinate = gate_coordinates[end_gate - 1]
            elif (end_gate, start_gate) in gate_connections.keys():
                select_conn = gate_connections[(end_gate, start_gate)]
                gate_net = (end_gate, start_gate)
                new_net = (start_gate, end_gate)
                end_coordinate = gate_coordinates[start_gate - 1]
            else:
                select_conn = "Key already deleted"
            
            # Delete wire if wire doesn't reach end gate
            if select_conn != "Key already deleted" and end_coordinate not in select_conn:
                del gate_connections[gate_net]
                
                # Calculate total shortest distance between gates for appending to distances
                coor_start = gate_coordinates[start_gate - 1]
                coor_end = gate_coordinates[end_gate - 1]
    
                x_coordinate_start = int(coor_start[0])
                y_coordinate_start = int(coor_start[1])

                x_coordinate_end = int(coor_end[0])
                y_coordinate_end = int(coor_end[1])

                total_dist = abs(x_coordinate_start - x_coordinate_end) + abs(y_coordinate_start - y_coordinate_end)
                
                distances.append((new_net, total_dist))
    
                # Repeat this number 2 times
                for repeat in range(2):
                    longest_wire_length = 0
                    # Select longest wire and create again
                    for connection in gate_connections:
                        wire_length = len(gate_connections[connection])
                        if wire_length > longest_wire_length:
                            longest_wire_length = wire_length
                            delete_gate = connection
        
                    # Calculate total shortest distance between gates for appending to distances
                    coor_start = gate_coordinates[delete_gate[0] - 1]
                    coor_end = gate_coordinates[delete_gate[1] - 1]
    
                    x_coordinate_start = int(coor_start[0])
                    y_coordinate_start = int(coor_start[1])

                    x_coordinate_end = int(coor_end[0])
                    y_coordinate_end = int(coor_end[1])

                    total_dist = abs(x_coordinate_start - x_coordinate_end) + abs(y_coordinate_start - y_coordinate_end)
                    
                    new_wire = (delete_gate[1], delete_gate[0])
                    distances.append((new_wire, total_dist))
        
                    del gate_connections[delete_gate]

                    deletewire = []
                    # Delete wire from allwires list
                    for i, item2 in enumerate(allwires):
                        if item2.net == gate_net or item2.net == delete_gate:
                            deletewire.append(allwires[i])

                    for delete_wire in deletewire:
                        allwires.remove(delete_wire)
        
        # Delete wires that are not within the grid
        connections_list = list(gate_connections.items())

        for conn_index in connections_list:
            wire = conn_index[1]
            gatenet = conn_index[0]
            for coord in wire:
                x_coor = coord[0]
                y_coor = coord[1]
                z_coor = coord[2]
                if x_coor < 0 or y_coor < 0 or z_coor < 0 or z_coor > max_num_layers:
                    # Increase number of deleted wires
                    minus_num_wires += 1
                    
                    # Delete wire from gate_connections dictionary
                    del gate_connections[gatenet]
                    
                    # Calculate total shortest distance between gates for appending to distances
                    coor_start = gate_coordinates[gatenet[0] - 1]
                    coor_end = gate_coordinates[gatenet[1] - 1]
    
                    x_coordinate_start = int(coor_start[0])
                    y_coordinate_start = int(coor_start[1])

                    x_coordinate_end = int(coor_end[0])
                    y_coordinate_end = int(coor_end[1])

                    total_dist = abs(x_coordinate_start - x_coordinate_end) + abs(y_coordinate_start - y_coordinate_end)
                    
                    # Append deleted wire to distances in switched order
                    wire_new = (gatenet[1], gatenet[0])
                    distances.append((wire_new, total_dist))
                    
                    deletewire = []
                    # Delete wire from allwires list
                    for i, item2 in enumerate(allwires):
                        if item2.net == gatenet:
                            deletewire.append(allwires[i])

                    for delete_wire in deletewire:
                        allwires.remove(delete_wire)
                    break
                    
    # Print update about number of connected gates
    print("Currently", len(gate_connections), "wires out of", len(netlist), "wires.")
    
    # Let script stop if running in forever loop
    if len(distances) > 5*len(netlist):
        # Delete wires that are not within the grid
        connections_list = list(gate_connections.items())
                 
        for connection_index in connections_list:
            wire = connection_index[1]
            gatenet = connection_index[0]
            for coord in wire:
                x_coor = coord[0]
                y_coor = coord[1]
                z_coor = coord[2]
                if x_coor < 0 or y_coor < 0 or z_coor < 0 or z_coor > max_num_layers:
                    # Increase number of deleted wires
                    minus_num_wires += 1
                    
                    # Delete wire from gate_connections dictionary
                    del gate_connections[gatenet]
                
                    deletewire = []
                    # Delete wire from allwires list
                    for i, item2 in enumerate(allwires):
                        if item2.net == gatenet:
                            deletewire.append(allwires[i])

                    for delete_wire in deletewire:
                        allwires.remove(delete_wire)
                    break
        break
    
print("NUMBER OF WIRES: ", len(gate_connections))

length = 0
# Calculate total length of wires
for key in gate_connections:
    wire = gate_connections[key]
    length = length + len(wire)
    
print("TOTAL LENGTH: ", length)

def make_grid(layers, size):
    """
    Creates grid for the chip.
    """
    for i in range(layers): 
        GridX = np.linspace(0, size, (size + 1))
        GridY = np.linspace(0, size, (size + 1))
        X, Y = np.meshgrid(GridX, GridY)
        Z = (np.sin(np.sqrt(X ** 2 + Y ** 2)) * 0) + i
    #configure axes
    ax.set_zlim3d(0, layers)
    ax.set_xlim3d(0, size)
    ax.set_ylim3d(0, size)

def draw_line(crdFrom, crdTo, colour):
    """
    Draw lines between coordinates of the wires.
    """
    Xline = [crdFrom[0], crdTo[0]]
    Yline = [crdFrom[1], crdTo[1]]
    Zline = [crdFrom[2], crdTo[2]]
    # Draw line
    ax.plot(Xline, Yline, Zline,lw=2,  color=colour, ms=12)

def set_gate(crd):
    """
    Marks coordinates of gates with red dot.
    """
    PointX = [crd[0]]
    PointY = [crd[1]]
    PointZ = [crd[2]]
    # Plot points
    ax.plot(PointX, PointY, PointZ, ls="None", marker="o", color='red')

fig = plt.figure()
ax = plt.axes(projection="3d")

make_grid(8, 16)
# Mark coordinates of gates
for gate_coordinate in gate_coordinates: 
    set_gate(gate_coordinate)
    plt.pause(0.03)

# Create lines for every wire between gates with different colours
allConnections = []
colours = ['b','lightgreen','cyan','m','yellow','k', 'pink']
colourcounter = 0
for keys in gate_connections:
    allConnections = gate_connections[keys]
    allconnectionlist = []
    for listconnection in allConnections: 
        allconnectionlist.append(listconnection)
    if colourcounter < len(colours) - 1:
        colourcounter += 1
    else: 
        colourcounter = 0
    for i in range(len(allconnectionlist)):
        try:
            draw_line(allconnectionlist[i], allconnectionlist[i+1], colours[colourcounter] )
            plt.pause(0.000001)
        except: 
            break

# Create output file with coordinates of wires between gates and connected gates           
with open('../output/output_linespacerydirection.csv', mode= 'w') as outputfile:
    output_writer = csv.writer(outputfile, delimiter= ',')

    for keys in gate_connections:
        output_writer.writerow([keys, gate_connections[keys]])

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()