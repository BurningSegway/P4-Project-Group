import socket 
import time
 
HOST = "192.168.1.37"
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen()
conn,addr = s.accept()

 
with conn:
    print(f"connected to: {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)
        print(f"Server modtag: {data}")