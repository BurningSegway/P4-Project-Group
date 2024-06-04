import socket 

HOST = "172.20.66.44"
PORT = 11382
data2 = '10'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen()
conn,addr = s.accept()
with conn:
    print(f"connected to: {addr}")
    while True:
        data = conn.recv(1024)
        print("dd", data)
        if not data:
            break
        conn.sendall(b'10000')



        
        
        
        
        
        
        
        
        
        
        
        
        











