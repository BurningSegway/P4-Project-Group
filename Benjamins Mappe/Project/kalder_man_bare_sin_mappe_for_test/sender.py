import socket 
import time
 
# Create a socket object 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
 
# Get the hostname of the server machine 
#server_host = socket.gethostname() 
server_host = "192.168.1.37"
# Define the port to connect to 
server_port = 32007 

HOST = "192.168.1.37"
PORT = 65432
 
# Connect to the server 
client_socket.connect((HOST, PORT))


while True:
    client_socket.sendall(b"Affald")
    data = client_socket.recv(1024)
    print(f"Recieved: {data}")
    time.sleep(0.1)