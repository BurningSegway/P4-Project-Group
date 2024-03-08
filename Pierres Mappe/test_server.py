# echo-server.py

import socket

HOST = "192.168.138.26"  # Standard loopback interface address (localhost)
PORT = 20001  # Port to listen on (non-privileged ports are > 1023)

msg = str.encode("Hello TCP Creature, you dare contact meeeeee????")

while(True):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                print(data)
                if not data:
                    break
                conn.sendto(msg, addr)