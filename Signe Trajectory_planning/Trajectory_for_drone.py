#describing the coordinate placement of a drone in 3D space using Cubic polynominal while taking into acount the orientation of the drone in 3D space
#object oriented programming
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

def generate_points(top_left, top_right, bottom_right, bottom_left, distance, altityde):
    # Calculate the number of lines based on the distance
    num_lines = int(np.linalg.norm(np.array(top_right) - np.array(top_left)) // distance)

    # Initialize the list of points
    points = []

    for i in range(num_lines + 1):
        # Calculate the start and end points of the line
        start = np.array(top_left) + i * (np.array(bottom_left) - np.array(top_left)) / num_lines
        end = np.array(top_right) + i * (np.array(bottom_right) - np.array(top_right)) / num_lines

        if i == 0:
            start1 = np.append(start, 0)
            points.append(start1)
            
        start = np.append(start, altityde)
        end = np.append(end, altityde)
        
        if i % 2 == 0:
            points.append(start)
            points.append(end)
            if i == num_lines:
                end1 = [end[0], end[1], 0]
                points.append(end1)
        else:
            points.append(end)
            points.append(start)
            if i == num_lines:
                end1 = [start[0], start[1], 0]
                points.append(end1)
                
    return points


def create_times(points):  # create the points and times for the drone to reach each point
    # Create a list of points in 3D space    
    distances = []
    time_coefficient = 0.5 # this has to be determined later
    for i in range(len(points)-1):
        distances.append(np.sqrt((points[i+1][0]-points[i][0])**2 + (points[i+1][1]-points[i][1])**2 + (points[i+1][2]-points[i][2])**2))
    # based on the distance between the points and a coefficient, calculate the time to reach each point
    times = [time_coefficient*distances[i] for i in range(len(distances))]
    
    return times 

def determine_rotation_z_axis(points):  # determine the rotation of the drone in the z-axis based on the points
    rotation = []
    vector1 = [1,0]
    for i in range(len(points)-1):
        vector2 = [points[i+1][0]-points[i][0], points[i+1][1]-points[i][1]]
        if np.linalg.norm(vector1) == 0 or np.linalg.norm(vector2) == 0:
            angle = 0
            rotation.append(angle)
            continue
        angle = (math.acos((vector1[0]*vector2[0] + vector1[1]*vector2[1])/(np.linalg.norm(vector1)*np.linalg.norm(vector2)))) * 180 / math.pi #convert to degrees
        if vector1[0]*vector2[1] - vector1[1]*vector2[0] < 0:
            angle = -angle  #determine the direction of the rotation
        vector1 = vector2
        rotation.append(angle)
    return rotation
      

#coefficients of the cubic polynomial for no via points
def equations_coefficients(start_val, stop_val, tf):  # tf=sluttid calculate the coefficients of the cubic polynomial
    a0 = start_val
    a1 = 0 #acceleration at the start is 0
    a2 = (3/(tf**2))*(stop_val-start_val)
    a3 = ((-2)/(tf**3))*(stop_val-start_val)
    coefficients = [a0,a1,a2,a3]
    return coefficients

def calculate_coeffecients(times):  # calculate the coefficients of the cubic polynomial for each segment
    coeffecients = []
    for i in range(len(points)-1):
        for j in range(3):
            # Calculate the coefficients of the cubic polynomial
            coeff = equations_coefficients(points[i][j], points[i+1][j], times[i])
            coeffecients.append(coeff)    
    return coeffecients

# Define your functions
def xyz(t, point_number, coeffecients,addxyz,t_old):
    point_number = point_number + addxyz
    return coeffecients[point_number][0] + coeffecients[point_number][1]*(t-t_old) + coeffecients[point_number][2]*(t-t_old)**2 + coeffecients[point_number][3]*(t-t_old)**3

def xyz_dot(t, point_number, coeffecients,addxyz,t_old):
    point_number = point_number + addxyz
    return coeffecients[point_number][1] + 2*coeffecients[point_number][2]*(t-t_old) + 3*coeffecients[point_number][3]*(t-t_old)**2

def xyz_dot_dot(t, point_number, coeffecients,addxyz,t_old):
    point_number = point_number + addxyz
    return 2*coeffecients[point_number][2] + 6*coeffecients[point_number][3]*(t-t_old)

                              
def plot_points(coeffecients, times):  # plot the points in 3D space using the cubic polynomial
    # Create a list of time values
    t_values = np.linspace(0, np.sum(times), int(round(np.sum(times)*1000))) #start, stop, number of samples
    
    # Calculate the x, y, and z functions
    point_number = 0
    t_old = 0
    x_values = []
    x_dot_values = []
    x_dot_dot_values = []
    y_values = []
    y_dot_values = []
    y_dot_dot_values = []
    z_values = []
    z_dot_values = []
    z_dot_dot_values = []
    
    for t in t_values: 
        
        if t - t_old >= times[point_number//3] and point_number <= len(times)*3-3:
            point_number =point_number + 3
            t_old = t
            
        x_values.append(xyz(t, point_number, coeffecients,0,t_old))
        x_dot_values.append(xyz_dot(t, point_number, coeffecients,0,t_old))
        x_dot_dot_values.append(xyz_dot_dot(t, point_number, coeffecients,0,t_old))
        y_values.append(xyz(t, point_number, coeffecients,1, t_old))
        y_dot_values.append(xyz_dot(t, point_number, coeffecients,1, t_old))
        y_dot_dot_values.append(xyz_dot_dot(t, point_number, coeffecients,1, t_old))
        z_values.append(xyz(t, point_number, coeffecients, 2, t_old))
        z_dot_values.append(xyz_dot(t, point_number, coeffecients,2, t_old))
        z_dot_dot_values.append(xyz_dot_dot(t, point_number, coeffecients,2, t_old))
        
    # from now on it is plotting
    # Create a figure and a grid of subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    
    # Plot position, speed, and acceleration for x
    ax1.plot(t_values, x_values, color='blue', label='Position')
    ax1.plot(t_values, x_dot_values, color='green', label='Speed')
    ax1.plot(t_values, x_dot_dot_values, color='red', label='Acceleration')
    ax1.set_title('x(t)')
    ax1.set_ylabel('x')
    ax1.legend()

    # Plot position, speed, and acceleration for y
    ax2.plot(t_values, y_values, color='blue', label='Position')
    ax2.plot(t_values, y_dot_values, color='green', label='Speed')
    ax2.plot(t_values, y_dot_dot_values, color='red', label='Acceleration')
    ax2.set_title('y(t)')
    ax2.set_ylabel('y')
    ax2.legend()

    # Plot position, speed, and acceleration for z
    ax3.plot(t_values, z_values, color='blue', label='Position')
    ax3.plot(t_values, z_dot_values, color='green', label='Speed')
    ax3.plot(t_values, z_dot_dot_values, color='red', label='Acceleration')
    ax3.set_title('z(t)')
    ax3.set_xlabel('Time (t)')
    ax3.set_ylabel('z')
    ax3.legend()

    # Create a 3D plot of the x, y, and z values with points
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_values, y_values, z_values)
    ax.scatter([point[0] for point in points], [point[1] for point in points], [point[2] for point in points], c='r', marker='o')
    plt.show()

points = generate_points([0,0], [30,0], [15,10], [0,5], 5, 30)
times = create_times(points)
coeffecients = calculate_coeffecients(times)
angles = determine_rotation_z_axis(points)
plot_points(coeffecients, times)