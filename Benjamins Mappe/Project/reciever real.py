import socket 
import xml.etree.ElementTree as ET

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
        print(f"Server modtag: {data.decode()}")

root = ET.fromstring(data)

string1 = root.find('name')
string2 = root.find('time')
rotation = root.find('coordinate/rotation')
rot_x = rotation.find('x')
rot_y = rotation.find('y')
rot_z = rotation.find('z')
rot_bol = rotation.find('condition')
translation = root.find('coordinate/rotation')
trans_x = translation.find('x')
trans_y = translation.find('y')
trans_z = translation.find('z')
trans_bol = translation.find('condition')









