import csv

class Wire():
    def __init__(self, coordinate, net):
        self.coordinate = coordinate
        self.net = net
        
    def get_coordinate(self):
        return self.coordinate
        
    def __repr__(self):
        # return f"{self.coordinate}, {self.net}"
        return str(self.coordinate, self.net)

class Gate_coordinate():
    def __init__(self, gate_file):
        self.gate_coordinates = self.load_gates(gate_file)
    
    def load_gates(self, gates_file):
        allgates = open(gates_file)
        reader = csv.reader(allgates)

        gate_coordinates = []

        for number, x, y in reader:
            if x != " x":
                x = int(x)
                y = int(y)
                coordinates = [x, y, 0]
                gate_coordinates.append(coordinates)
                
        return gate_coordinates 

class Net():
    def __init__(self, gate_1, gate_2):
        self.gate_1 = gate_1
        self.gate_2 = gate_2
        self.wires = []
        
    def create_wires(self, wire):
        self.wires.append(wire)
        
    def get_wire():
        return self.wires
        
    def __repr__(self):
        # return f"{self.gate_1}, {self.gate_2}, {self.wires}"
        return str(self.gate_1) + ", " + str(self.gate_2) + ", " + str(self.wires)
        
class Netlist():
    def __init__(self, net_file):
        self.netlist = self.load_netlist(net_file)
    
    def load_netlist(self, netlist_file):
        data = open(netlist_file)
        reader = csv.reader(data)
        
        netlist = []
        
        for net_1, net_2 in reader:
            if net_1 != "chip_a":
                net = Net(net_1, net_2)
                netlist.append(net)
        
        return netlist