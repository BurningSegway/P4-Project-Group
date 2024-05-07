import socket

HOST = "172.20.66.47"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    inst = 2
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            data_corrected = data.split(b'.')
            print(f"Received from PLC: {data_corrected[0]}")
            if not data:
                break
            conn.sendall(b'2000')