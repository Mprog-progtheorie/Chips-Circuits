from code.visualisation import plot as plot
from code.classes import classes as classs
from code.functions import delete as delete
import copy


if __name__ == '__main__':
    # Create netlist by loading file in class
    netlist = classs.Netlist("data/netlist_1.csv").netlist
    print(netlist)

    # Create list for gate coordinates
    gate_coordinates = classs.Gate_coordinate("data/pritn_1.csv").gate_coordinates
    print(gate_coordinates)

    """
    # TODO
        geef de begin en eindgate mee
        alle gate_coordinaten
        geef een lijst mee met coordinaten waar al draad ligt
    """ 
    for net in netlist: 
        Astarroute = Astar_search(int(net.gate_1))
        print("From", gate_coordinates[int(net.gate_1)], "To", gate_coordinates[int(net.gate_2)])


    