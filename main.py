from code.visualisation import plot as plot
from code.classes import classes as classs
from code.functions import delete as delete
import copy


if __name__ == '__main__':
    # Create netlist by loading file in class
    netlist = classs.Netlist("data/netlist_4.csv").netlist
    print(netlist)

    # Create list for gate coordinates
    gate_coordinates = classs.Gate_coordinate("data/print_2.csv").gate_coordinates
    print(gate_coordinates)





    plot.make_grid(5, 5)
    plot.draw_line([0,0,0], [1,1,1], "red")
    plot.draw_line([0,0,0], [1,2,1], "blue")
    plot.plt.show()