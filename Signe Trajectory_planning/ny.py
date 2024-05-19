#describing the coordinate placement of a drone in 3D space using Cubic polynominal while taking into acount the orientation of the drone in 3D space
#object oriented programming
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#points in 3D space
points = [[0,0,0],[0,0,30], [30,30,30], [40,20,30], [0,0,30], [0,0,0]]

#time to reach each point
times = [5,5,5,5,5] 



def generate_points(top_left, top_right, bottom_right, bottom_left, distance):
    # Calculate the number of lines based on the distance
    num_lines = int(np.linalg.norm(np.array(top_right) - np.array(top_left)) // distance)

    # Initialize the list of points
    points = []

    for i in range(num_lines + 1):
        # Calculate the start and end points of the line
        start = np.array(top_left) + i * (np.array(bottom_left) - np.array(top_left)) / num_lines
        end = np.array(top_right) + i * (np.array(bottom_right) - np.array(top_right)) / num_lines

        # Generate the points on the line
        line_points = [start + j * (end - start) / 100 for j in range(101)]

        # Add the points to the list
        points.extend(line_points if i % 2 == 0 else line_points[::-1])

    return points

# Define the 4 points of the square field
top_left = [0, 0]
top_right = [10, 0]
bottom_right = [10, 10]
bottom_left = [0, 10]

# Define the distance between the lines
distance = 1

# Generate the points
#points = generate_points(top_left, top_right, bottom_right, bottom_left, distance)




def create_points_and_times():  # create the points and times for the drone to reach each point
    # Create a list of points in 3D space
    points = [[0,0,0],[25,30,8], [10,10,10], [40,20,50], [-30,-10,10], [0,0,0]]
    
    
    distances = []
    time_coefficient = 0.5 # this has to be determined later
    for i in range(len(points)-1):
        distances.append(np.sqrt((points[i+1][0]-points[i][0])**2 + (points[i+1][1]-points[i][1])**2 + (points[i+1][2]-points[i][2])**2))
    # based on the distance between the points and a coefficient, calculate the time to reach each point
    times = [time_coefficient*distance for distance in distances]
    print(times)
    return points, times

create_points_and_times()

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
    t_values = np.linspace(0, np.sum(times), np.sum(times)*1000) #start, stop, number of samples
    
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
        z_values.append(xyz(t, point_number, coeffecients,2, t_old))
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

    """
    # Plot x_values
    ax1.plot(t_values, x_values, color='blue', label='x(t)')
    ax1.set_title('x(t)')
    ax1.set_ylabel('x')

    # Plot y_values
    ax2.plot(t_values, y_values, color='green', label='y(t)')
    ax2.set_title('y(t)')
    ax2.set_ylabel('y')

    # Plot z_values
    ax3.plot(t_values, z_values, color='red', label='z(t)')
    ax3.set_title('z(t)')
    ax3.set_xlabel('Time (t)')
    ax3.set_ylabel('z')

    # Display the figure with the subplots
    plt.tight_layout()
    plt.show()
    """
    # Create a 3D plot of the x, y, and z values with points
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_values, y_values, z_values)
    ax.scatter([point[0] for point in points], [point[1] for point in points], [point[2] for point in points], c='r', marker='o')
    plt.show()
    

plot_points( calculate_coeffecients(times), times)
