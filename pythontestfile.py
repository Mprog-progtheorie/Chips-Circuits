"""
Breng wires als eerst helemaal naar boven, werk daarna omlaag
"""

while z_coordinate_start < 7:
    z_coordinate_start = z_coordinate_start + 1
    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
    if gate_connections:
        (z_coordinate_start, x_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, z_coordinate_start, -1, x_coordinate_start, step_x)
        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
        (x_coor_notrelevant, x_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, x_coordinate_start, step_x, x_coordinate_start, (-2*step_x))
        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
        (x_coordinate_start, y_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, x_coordinate_start, step_x, y_coordinate_start, step_y)
        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
        (y_coor_notrelevant, y_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, step_y, y_coordinate_start, (-2*step_y))
    elif coordinate in gate_coordinates and coordinate != coordinate_end:
        z_coordinate_start = z_coordinate_start - 1
        x_coordinate_start = x_coordinate_start + step_x
        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
        (x_coor_notrelevant, x_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, step_x, x_coordinate_start, (-2*step_x))
        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
        (x_coordinate_start, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, step_x, y_coordinate_start, step_y)
        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
        (y_coor_notrelevant, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, y_coordinate_start, step_y, y_coordinate_start, (-2*step_y))


if switch_variable == 0:
    # Loop until x-coordinate from start gate equals x-coordinate from end gate
    while x_coordinate_start != x_coordinate_end:
        x_coordinate_start = x_coordinate_start + step_x
        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
        # Check for other gates or other wires
        if gate_connections:
            (x_coordinate_start, z_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, x_coordinate_start, -step_x, z_coordinate_start, -1)
            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
            (z_coordinate_start, y_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, z_coordinate_start, 1, y_coordinate_start, step_y)
            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
            # Coordinate changes 2 times in y-direction, so step_y is doubled
            (y_coor_notrelevant, y_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, step_y, y_coordinate_start, (-2*step_y))
            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
            (y_coordinate_start, x_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, step_y, x_coordinate_start, -step_x)
        elif coordinate in gate_coordinates and coordinate != coordinate_end:
            x_coordinate_start = x_coordinate_start - step_x
            # z kan nu niet meerdere stappen omhoog/omlaag
            z_coordinate_start = z_coordinate_start - 1
            #checken of na deze stap geen gate zit
            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
            (z_coordinate_start, x_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, z_coordinate_start, 1, x_coordinate_start, -step_x)
            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
            (x_coordinate_start, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, step_x, y_coordinate_start, step_y)
            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
            # Coordinate changes 2 times in y-direction, so step_y is doubled
            (y_coor_notrelevant, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, y_coordinate_start, step_y, y_coordinate_start, (-2*step_y))

        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
        wires.append(coordinate)
        print(coordinate)
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
            if z_coordinate_start > z_coordinate_end:
                z_step = -1
            elif z_coordinate_start < z_coordinate_end:
                z_step = 1
            z_coordinate_start = z_coordinate_start + z_step
            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
            if gate_connections:
                (z_coordinate_start, x_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, z_coordinate_start, -z_step, x_coordinate_start, step_x)
                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                (x_coordinate_start, y_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, x_coordinate_start, -step_x, y_coordinate_start, step_y)
                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                (y_coor_notrelevant, y_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, step_y, y_coordinate_start, (-2*step_y))
                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                (y_coordinate_start, x_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, step_y, x_coordinate_start, -step_x)
            elif coordinate in gate_coordinates and coordinate != coordinate_end:
                z_coordinate_start = z_coordinate_start -z_step
                x_coordinate_start = x_coordinate_start + step_x
                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                (x_coordinate_start, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, -step_x, y_coordinate_start, step_y)
                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                (y_coor_notrelevant, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, y_coordinate_start, step_y, y_coordinate_start, (-2*step_y))
                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                (x_coordinate_start, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, -step_x, y_coordinate_start, step_y)
        
            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
            wires.append(coordinate)
            print(coordinate)
            wire = classs.Wire(coordinate, connected_gate)
            allwires.append(wire)
            
# Redefine step in direction of y-coordinate    
if y_coordinate_start < y_coordinate_end:
    step_y = 1
elif y_coordinate_start > y_coordinate_end:
    step_y = -1

# Loop until y-coordinate from start gate equals y-coordinate from end gate
while y_coordinate_start != y_coordinate_end:
   y_coordinate_start = y_coordinate_start + step_y
   coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
   # Check for other gates or other wires
   if gate_connections:
       try:
           step_x = step_x
       except:
           step_x = 0
       (y_coordinate_start, z_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, -step_y, z_coordinate_start, -1)
       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
       (z_coordinate_start, x_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, z_coordinate_start, 1, x_coordinate_start, step_x)
       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
       (x_coor_notrelevant, x_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, x_coordinate_start, step_x, x_coordinate_start, (-2*step_x))
       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
       (x_coordinate_start, y_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, x_coordinate_start, step_x, y_coordinate_start, -step_y)
   elif coordinate in gate_coordinates and coordinate != coordinate_end:
       y_coordinate_start = y_coordinate_start - step_y
       z_coordinate_start = z_coordinate_start - 1
       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
       (x_coordinate_start, z_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, step_x, z_coordinate_start, 1)
       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
       (x_coor_notrelevant, x_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, step_x, x_coordinate_start, (-2*step_x))
       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
       (x_coordinate_start, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, step_x, y_coordinate_start, -step_y)

   # Reset switch variable to be able to move in x-direction
   switch_variable = 0
   
   coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
   wires.append(coordinate)
   print(coordinate)
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
           if z_coordinate_start > z_coordinate_end:
               z_step = -1
           elif z_coordinate_start < z_coordinate_end:
               z_step = 1
           z_coordinate_start = z_coordinate_start + z_step
           coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
           if gate_connections:
               (z_coordinate_start, x_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, z_coordinate_start, -z_step, x_coordinate_start, step_x)
               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
               (x_coordinate_start, y_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, x_coordinate_start, -step_x, y_coordinate_start, step_y)
               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
               (y_coor_notrelevant, y_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, step_y, y_coordinate_start, (-2*step_y))
               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
               (y_coordinate_start, x_coordinate_start) = change.change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, step_y, x_coordinate_start, -step_x)
           elif coordinate in gate_coordinates and coordinate != coordinate_end:
               z_coordinate_start = z_coordinate_start -z_step
               x_coordinate_start = x_coordinate_start + step_x
               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
               (x_coordinate_start, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, -step_x, y_coordinate_start, step_y)
               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
               (y_coor_notrelevant, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, y_coordinate_start, step_y, y_coordinate_start, (-2*step_y))
               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
               (x_coordinate_start, y_coordinate_start) = change.change_coor2(coordinate, wires, gate_coordinates, coordinate_end, x_coordinate_start, -step_x, y_coordinate_start, step_y)
                           
           coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
           wires.append(coordinate)
           print(coordinate)
           wire = classs.Wire(coordinate, connected_gate)
           allwires.append(wire)