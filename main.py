from code.visualisation import plot as plot
from code.classes import classes as classs
from code.functions import delete as delete
from code.algorithms import Astar as astar
import copy



if __name__ == '__main__':
    # Create netlist by loading file in class
    netlist = classs.Netlist("data/netlist_1.csv").netlist
    # print(netlist)

    # Create list for gate coordinates
    gate_coordinates = classs.Gate_coordinate("data/pritn_1.csv").gate_coordinates
    # print(gate_coordinates)

    """
    # TODO
        geef de begin en eindgate mee
        alle gate_coordinaten
        geef een lijst mee met coordinaten waar al draad ligt
    """ 
    for net in netlist: 
        # Astarroute = astar.a_star
        # print(net)
        print("From", gate_coordinates[int(net.gate_1) - 1], "To", gate_coordinates[int(net.gate_2) - 1])

    # ax = plot.make_grid(8, 16)
        
    # for gate_coordinate in gate_coordinates: 
    #     print(gate_coordinate)
    #     plot.set_gate(gate_coordinate, ax)
    #     plot.plt.pause(0.001)

    # plot.plt.show()

