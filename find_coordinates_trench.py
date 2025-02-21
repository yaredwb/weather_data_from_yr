import matplotlib.pyplot as plt

def calculate_coordinates():
    """
    Calculates the coordinates of points 1-18 on the sketch based on given dimensions.
    Assumes point 1 is at (0,0).
    """

    dimensions = {
        "Width": 10,  # Assuming 'Width' refers to the total width based on point 1 and 2
        "Height": 4,
        "Asphalt_thickness": 0.14,
        "Depth_of_trench": 1.5,
        "Top_width_of_trench": 3,
        "Bottom_width_of_trench": 1.5,
        "Cushion_thickness": 0.1,
        "Thickness_of_insulation": 0.05,
        "Width_of_insulation": 0.8,
        "Depth_of_pipe": 1.2,
        "Pipe_diameter": 0.25,
        "Distance_b_n_insulation_and_pipe": 0.1,
    }

    W = dimensions["Width"]
    H = dimensions["Height"]
    At = dimensions["Asphalt_thickness"]
    Dt = dimensions["Depth_of_trench"]
    TWT = dimensions["Top_width_of_trench"]
    BWT = dimensions["Bottom_width_of_trench"]
    Ct = dimensions["Cushion_thickness"]
    Ti = dimensions["Thickness_of_insulation"]
    Wi = dimensions["Width_of_insulation"]
    Dp = dimensions["Depth_of_pipe"]
    Pd = dimensions["Pipe_diameter"]
    Dip = dimensions["Distance_b_n_insulation_and_pipe"]

    # Point coordinates as individual x,y variables
    x1, y1 = 0, 0
    x2, y2 = W, 0
    x3, y3 = W, H
    x4, y4 = 0, H
    x5, y5 = 0, H - At
    x6, y6 = W, H - At
    x7, y7 = (W - TWT) / 2, H
    x8, y8 = (W - BWT) / 2, H - Dt
    x9, y9 = x8 + BWT, H - Dt
    x10, y10 = x7 + TWT, H
    x11, y11 = (W - Wi) / 2, H - Dt + Ct + Pd + Dip
    x12, y12 = (W + Wi) / 2, H - Dt + Ct + Pd + Dip
    x13, y13 = x12, y12 + Ti
    x14, y14 = x11, y11 + Ti
    x15, y15 = x11 + Ti, y11 + Ti
    x16, y16 = x12 - Ti, y12 + Ti
    x17, y17 = W / 2, y8 + Ct + Pd / 2
    x18, y18 = W / 2, y17 - Pd / 2

    return {
        'x': [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18],
        'y': [y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, y17, y18]
    }

def plot_trench(coordinates):
    """Plot the trench structure with numbered points."""
    plt.figure(figsize=(12, 8))
    
    x = coordinates['x']
    y = coordinates['y']
    
    # Plot all points
    plt.scatter(x, y, color='red')
    
    # Add point labels
    for i in range(len(x)):
        point_num = i + 1
        if point_num in [15, 16]:  # Skip unused points
            continue
        plt.annotate(f'P{point_num}', (x[i], y[i]), 
                    xytext=(5, 5), textcoords='offset points')
    
    # Connect points to show the structure
    # Outer frame
    plt.plot([x[0], x[1]], [y[0], y[1]], 'b-')  # 1-2
    plt.plot([x[1], x[2]], [y[1], y[2]], 'b-')  # 2-3
    plt.plot([x[2], x[3]], [y[2], y[3]], 'b-')  # 3-4
    plt.plot([x[3], x[0]], [y[3], y[0]], 'b-')  # 4-1
    
    # Trench outline
    plt.plot([x[6], x[7]], [y[6], y[7]], 'g-')  # 7-8
    plt.plot([x[9], x[10]], [y[9], y[10]], 'g-')  # 10-11
    plt.plot([x[10], x[11]], [y[10], y[11]], 'g-')  # 11-12
    
    plt.grid(True)
    plt.axis('equal')
    plt.title('Trench Structure')
    plt.xlabel('Width')
    plt.ylabel('Height')
    plt.show()

if __name__ == "__main__":
    coordinates = calculate_coordinates()
    
    # Print coordinates
    for i in range(len(coordinates['x'])):
        point_num = i + 1        
        print(f"Point {point_num}: x={coordinates['x'][i]}, y={coordinates['y'][i]}")
    
    # Plot the trench
    plot_trench(coordinates)