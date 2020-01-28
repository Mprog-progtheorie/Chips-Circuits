"""
change_coordinates.py

Tom Kamstra, Izhar Hamer, Julia Linde

Defines functions needed for the script.
"""
    
def change_coor(gate_conn, coor, gate_coor, wires, coor_end, coor_start1, step1, coor_start2, step2):
    """
    Checks whether current coordinate is available, if not coordinate is changed by one step in another direction.
    """
    for key in gate_conn:
        selected_wires = gate_conn[key]
        if coor in selected_wires or coor in gate_coor or coor in wires:
            if coor != coor_end:
                # Change coordinate if end coordinate is not reached yet
                coor_start1 = coor_start1 + step1
                coor_start2 = coor_start2 + step2
                break
                
    return coor_start1, coor_start2
    
def change_coor2(coor, wires, gate_coor, coor_end, coor_start1, step1, coor_start2, step2):
    """
    Checks whether current coordinate is available in case of no gate_connections, if not coordinate is changed by one step in another direction.
    """
    if coor in gate_coor or coor in wires and coor != coor_end:
        coor_start1 = coor_start1 + step1
        coor_start2 = coor_start2 + step2
    
    return coor_start1, coor_start2