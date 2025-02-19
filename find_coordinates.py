import numpy as np

def calculate_coordinates():
    # Assumed dimensions (in meters)
    width_asphalt = 4
    side_distance = 3
    asphalt_thickness = 0.14
    base_thickness = 0.1
    width_concrete_channel = 0.8
    height_concrete_channel = 0.65
    wall_thickness = 0.1
    cushion_thickness = 0.07
    depth_below_channel = 3
    pipe_diameter = 0.25
    
    # Define missing variable
    x1 = 0
    y1 = 0
    
    # Compute key positions
    x2 = 2 * side_distance + width_asphalt
    y2 = y1  
    x3 = x2
    y3 = depth_below_channel + height_concrete_channel + base_thickness + 0.5 * asphalt_thickness
    x4 = x3 - side_distance
    y4 = y3
    x5 = x4
    y5 = y3 + 0.5 * asphalt_thickness
    x6 = x5 - width_asphalt
    y6 = y5
    x7 = x6
    y7 = y4
    x8 = x1
    y8 = y7
    x9 = x7
    y9 = y6 - asphalt_thickness
    x10 = x4
    y10 = y5 - asphalt_thickness
    
    # Out concrete channel coordinates
    x11 = x1 +  ((2 * side_distance  + width_asphalt) / 2) - (width_concrete_channel / 2)
    y11 = y1 + depth_below_channel  
    x12 = x11 + width_concrete_channel
    y12 = y11
    x13 = x12
    y13 = y12 + height_concrete_channel
    x14 = x11
    y14 = y13

    # Inner concrete channel coordinates
    x15 = x11 + wall_thickness
    y15 = y11 + wall_thickness
    x16 = x15 + (width_concrete_channel - 2 * wall_thickness)
    y16 = y15
    x17 = x16
    y17 = y16 + (height_concrete_channel - 2 * wall_thickness)
    x18 = x15
    y18 = y17

    # Cushion coordinates
    x19 = x15
    y19 = y15 + cushion_thickness
    x20 = x16
    y20 = y19

    # Pipe position (centered in the channel)
    x21 = (x15 + x16) / 2
    y21 = y20 + pipe_diameter / 2
    x22 = x21
    y22 = y21 - pipe_diameter / 2
    
    coordinates = {
        '1': (x1, y1),
        '2': (x2, y2),
        '3': (x3, y3),
        '4': (x4, y4),
        '5': (x5, y5),
        '6': (x6, y6),
        '7': (x7, y7),
        '8': (x8, y8),
        '9': (x9, y9),
        '10': (x10, y10),
        '11': (x11, y11),
        '12': (x12, y12),
        '13': (x13, y13),
        '14': (x14, y14),
        '15': (x15, y15),
        '16': (x16, y16),
        '17': (x17, y17),
        '18': (x18, y18),
        '19': (x19, y19),
        '20': (x20, y20),
        '21': (x21, y21),
        '22': (x22, y22)
    }
    
    return coordinates

# Run and display
coords = calculate_coordinates()
for point, (x, y) in coords.items():
    print(f'Point {point}: ({x:.2f}, {y:.2f})')
