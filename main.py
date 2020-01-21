from code.visualisation import plot as plot
from code.classes import classes as classs
from code.functions import delete as delete                     
from code.algorithms import Astar as Astar
import copy
import matplotlib.pyplot as plt
import time
import csv



if __name__ == '__main__':
    start_time = time.time()
    count = 0 
    # Create netlist by loading file in class
    netlist = classs.Netlist("data/netlist_1.csv").netlist
    # print(netlist)

    # Create list for gate coordinates
    gate_coordinates = classs.Gate_coordinate("data/pritn_1.csv").gate_coordinates
    # print(gate_coordinates)
    # print("!@@@@@")
    gate_connections = {}

    

   
    
    """
    # TODO
        geef de begin en eindgate mee
        alle gate_coordinaten
        geef een lijst mee met coordinaten waar al draad ligt
    """ 
    ax = plot.make_grid(8, 16)
    
    for gate_coordinate in gate_coordinates: 
        plot.set_gate(gate_coordinate, ax)

    for net in netlist:  
        count += 1
        start = gate_coordinates[int(net.gate_1) - 1]
        goal = gate_coordinates[int(net.gate_2) - 1]
        a_star_route = Astar.a_star(start, goal)
        
        print(start, goal)
       
        
        # # Als coordinaten van groot naar klein gaat begint de lijn volgens astar random op het laatste coordinaat maar dan op 7 hoog
        # if gate_coordinates[int(net.gate_1) -1][0]  <= gate_coordinates[int(net.gate_2) -1][0] :
        #     a_star_route = Astar.a_star(gate_coordinates[int(net.gate_1) -1], gate_coordinates[int(net.gate_2) -1])
        # else: 
        #     a_star_route = Astar.a_star(gate_coordinates[int(net.gate_2) -1], gate_coordinates[int(net.gate_1) -1])

        gate_connections.update({net: a_star_route})
        print(a_star_route)
        # for i, coo in enumerate(a_star_route): 
        #     plot.draw_line(coo[i], coo[i+1], "red", ax)
        print()
        # a_star_route = Astar.a_star([15, 11, 0], [14, 11, 0])
        # print(a_star_route)p

    end_time = time.time()
    print("TIME: ", end_time - start_time)
    allConnections = []
    colours = ['b','lightgreen','cyan','m','yellow','k', 'pink']
    colourcounter = 0
    for keys in gate_connections:
        allConnections = gate_connections[keys]
        print(len(allConnections))
        allconnectionlist = []
        for listconnection in allConnections: 
            allconnectionlist.append(listconnection)
            print("Test: ", listconnection)
        if colourcounter < 6:
            colourcounter += 1
        else: 
            colourcounter = 0

        print("LENGTE: ",len(allconnectionlist))
        for i in range(len(allconnectionlist)):
            try: 
                print("LineFromTo", [allconnectionlist[i].x, allconnectionlist[i].y, allconnectionlist[i + 1].z], "To",[allconnectionlist[i + 1].x, allconnectionlist[i + 1].y, allconnectionlist[i + 1].z],  colours[colourcounter])
                plot.draw_line([allconnectionlist[i].x, allconnectionlist[i].y, allconnectionlist[i + 1].z], [allconnectionlist[i + 1].x, allconnectionlist[i + 1].y, allconnectionlist[i + 1].z], colours[colourcounter], ax)
            except: 
                break 
    
    plt.show()
# with open('output_astar.csv', mode= 'w') as outputfile:
#     output_writer = csv.writer(outputfile, delimiter= ',')

#     for keys in gate_connections:
#         output_writer.writerow([keys, gate_connections[keys]])