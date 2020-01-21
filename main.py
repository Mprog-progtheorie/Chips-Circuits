from code.visualisation import plot as plot
from code.classes import classes as classs
from code.functions import delete as delete                     
from code.algorithms import Astar as Astar
import copy


if __name__ == '__main__':
    # Create netlist by loading file in class
    netlist = classs.Netlist("data/netlist_1.csv").netlist
    # print(netlist)

    # Create list for gate coordinates
    gate_coordinates = classs.Gate_coordinate("data/pritn_1.csv").gate_coordinates
    # print(gate_coordinates)
    # print("!@@@@@")

    """
    # TODO
        geef de begin en eindgate mee
        alle gate_coordinaten
        geef een lijst mee met coordinaten waar al draad ligt
    """ 
    wire_nodes = []
    for net in netlist: 
        start = gate_coordinates[int(net.gate_1) - 1]
        goal = gate_coordinates[int(net.gate_2) - 1]
        a_star_route = Astar.a_star(start, goal, wire_nodes)
        for i in a_star_route:
            wire_nodes.append(i)
        print(a_star_route)
        


    