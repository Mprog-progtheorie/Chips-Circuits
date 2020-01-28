"""
delete.py

Tom Kamstra, Izhar Hamer, Julia Linde

Defines functions needed for the script.
"""

import copy

def delete_wire(wires, coordinate_begin, itemnet, distances, gate_connections, allwires):
    """
    Delete wire from allwires list and and from gate_connections dictionary and appends it again to distances to be created again.
    """
    
    wires = []
    x_coordinate_start = int(coordinate_begin[0])
    y_coordinate_start = int(coordinate_begin[1])
    z_coordinate_start = int(coordinate_begin[2])
    coordinate = coordinate_begin
    
    # Switch order of gates
    end_gate = itemnet[0]
    start_gate = itemnet[1]
    
    # Append new wire to distances with low distance between gates, so that wire will not be deleted again
    low_distance = 2
    distances.append(((start_gate, end_gate), low_distance))

    # Delete wire from gate connections dictionary
    del gate_connections[itemnet]
    deletelist = []
    # Delete blocking wire
    for i, item2 in enumerate(allwires):
        if item2.net == itemnet:
            deletelist.append(allwires[i])

    for delete_wire in deletelist:
        allwires.remove(delete_wire)
    return wires, x_coordinate_start, y_coordinate_start, z_coordinate_start, coordinate, gate_connections, allwires

def delete_wires_maxlength(x_coor, y_coor, z_coor, all_wires, gate_end, wires, coor_begin, distances, gate_conn, deletinglen):
    """
    Delete wires if current wire is longer than maximum wirelength.
    """
    
    check_coordinate = [x_coor, y_coor, z_coor]
    for i, item in enumerate(all_wires):
        if item.coordinate == check_coordinate and item.net[0] != gate_end and item.net[1] != gate_end:
            (wires, x_coordinate_start, y_coordinate_start, z_coordinate_start, coordinate, gate_conn, all_wires) = delete_wire(wires, coor_begin, item.net, distances, gate_conn, all_wires)
            break
        else:
            copy_gate_connections = copy.deepcopy(gate_conn)
            for key in copy_gate_connections:
                if len(copy_gate_connections[key]) > deletinglen:
                    (wires, x_coordinate_start, y_coordinate_start, z_coordinate_start, coordinate, gate_conn, allwires) = delete_wire(wires, coor_begin, key, distances, gate_conn, all_wires)
        break
    return all_wires, wires, gate_conn