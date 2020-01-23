from code.visualisation import plot as plot
from code.classes import classes as classs
from code.functions import astardelete as astardelete                     
from code.algorithms import Astar as Astar
import copy
import matplotlib.pyplot as plt
import time
import csv



if __name__ == '__main__':
    start_time = time.time()
    # Create netlist by loading file in class
    netlist = classs.Netlist("data/netlist_1.csv").netlist

    # Create list for gate coordinates
    gate_coordinates = classs.Gate_coordinate("data/pritn_1.csv").gate_coordinates
  
    gate_connections = {}

    

   
    
    """
    # TODO
        geef de begin en eindgate mee
        alle gate_coordinaten
        geef een lijst mee met coordinaten waar al draad ligt
    """ 
    ax = plot.make_grid(8, 16)
    # string_gates = [] 
    blocked = []
    allwires = []


    for gate_coordinate in gate_coordinates: 
        # blocked.append(Astar.Node(gate_coordinate[0], gate_coordinate[1], gate_coordinate[2]).set_blocked())
        blocked.append(str(gate_coordinate))
        plot.set_gate(gate_coordinate, ax)
            
    distances = {}
    # for net in netlist: 
    #     start = gate_coordinates[int(net.gate_1) - 1]
    #     goal = gate_coordinates[int(net.gate_2) - 1]

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
    distances = list(distances.items())
    for max_number in range(len(distances)-1, -1, -1):
        swapped = False
        for count in range(max_number):
            if distances[count][1] > distances[count + 1][1]:
                distances[count], distances[count + 1] = distances[count + 1], distances[count]
                swapped = True
        if not swapped:
            break

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
        
        # Saves all coordinates around current start coordinate in list
        coordinate_check = [coordinate_1, coordinate_2, coordinate_3, coordinate_4, coordinate_5]
        
        # Creates list for all coordinates that are already occupied
        all_coordinates = []
        for coo in allwires:
            # print("JOEJOE")
            all_coordinates.append(coo.get_coordinate())
        
        print("Before1st: ", len(allwires))

        # Checks whether wire can move in any direction, if at least one coordinate around current coordinate is free
        if all(elem in all_coordinates for elem in coordinate_check):
            print("INNNN")
            for coor in coordinate_check:
                for item_start in allwires:
                    if item_start.coordinate == coor and item_start.net[0] != gate_start and item_start.net[1] != gate_start:
                        (wires, x_coordinate_start, y_coordinate_start, z_coordinate_start, coordinate, gate_connections, allwires, blocked) = astardelete.delete_wire(coordinate_begin, item_start.net, distances, gate_connections, allwires, blocked)
                        break
        print("AFTER1st: ", len(allwires))

        a_star_route = Astar.a_star(coordinate_begin, coordinate_end, blocked, connected_gate)

        print("LENALLWIRES: ",len(allwires))

        if str(a_star_route[0]) != str(coordinate_end):
            print("EQUAL: ", str(a_star_route[0]), str(coordinate_end))
            # Define all 5 coordinates that surround current end coordinate
            x_coordinate_endcheck = x_coordinate_end + 1
            coordinate_end_1 = [x_coordinate_endcheck, y_coordinate_end, z_coordinate_end]
            x_coordinate_endcheck2 = x_coordinate_end - 1
            coordinate_end_2 = [x_coordinate_endcheck2, y_coordinate_end, z_coordinate_end]
            y_coordinate_endcheck = y_coordinate_end + 1
            coordinate_end_3 = [x_coordinate_end, y_coordinate_endcheck, z_coordinate_end]
            y_coordinate_endcheck2 = y_coordinate_end - 1
            coordinate_end_4 = [x_coordinate_end, y_coordinate_endcheck2, z_coordinate_end]
            z_coordinate_endcheck = z_coordinate_end + 1
            coordinate_end_5 = [x_coordinate_end, y_coordinate_end, z_coordinate_endcheck]

            # Saves all coordinates around current start coordinate in list
            coordinate_end_check = [coordinate_end_1, coordinate_end_2, coordinate_end_3, coordinate_end_4, coordinate_end_5]
            
            # Creates list for all coordinates that are already occupied
            all_coordinates_for_end = []
            counter = 0
            for coo_wire in allwires:
                counter += 1
                print("ADD: ", coo_wire.get_coordinate(), counter)
                all_coordinates_for_end.append(coo_wire.get_coordinate())
            
            print("CHECKCOOR", all_coordinates_for_end, "CHECK", coordinate_end_check)
            # Checks whether wire can move in any direction, if at least one coordinate around current coordinate is free
            if all(elem in all_coordinates_for_end for elem in coordinate_end_check):
                # print("ELEM2", elem, coordinate_end_check)
                for coor_end in coordinate_check:
                    for item_end in allwires:
                        if item_end.coordinate == coor_end and item_end.net[0] != gate_end and item_end.net[1] != gate_end:
                            (wires, x_coordinate_start, y_coordinate_start, z_coordinate_start, coordinate, gate_connections, allwires, blocked) = astardelete.delete_wire(coordinate_begin, item_start.net, distances, gate_connections, allwires, blocked)
                            break
                a_star_route = Astar.a_star(coordinate_begin, coordinate_end, blocked, connected_gate)          
            
        for i in a_star_route:
            wire = classs.Wire([i.x, i.y, i.z], connected_gate)
            allwires.append(wire)    
            blocked.append(str(i))
        
        a_star_route.reverse()
        print("NET: ", a_star_route)
        gate_connections.update({connected_gate: a_star_route})
        

    
        # if len(gate_connections) > 26: 
        #     break






    end_time = time.time()
    print("TIME: ", end_time - start_time)
    print(len(gate_connections))

    allConnections = []
    colours = ['b','lightgreen','cyan','m','yellow','k', 'pink']
    colourcounter = 0
    for keys in gate_connections:
        allConnections = gate_connections[keys]
        print(len(allConnections))
        allconnectionlist = []
        for listconnection in allConnections: 
            allconnectionlist.append(listconnection)
        if colourcounter < 6:
            colourcounter += 1
        else: 
            colourcounter = 0

        for i in range(len(allconnectionlist)):
            try: 
                plot.draw_line([allconnectionlist[i].x, allconnectionlist[i].y, allconnectionlist[i].z], [allconnectionlist[i + 1].x, allconnectionlist[i + 1].y, allconnectionlist[i + 1].z], colours[colourcounter], ax)
            except: 
                break 
    
    plt.show()
