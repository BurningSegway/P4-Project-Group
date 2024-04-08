import socket 
import xml.etree.ElementTree as ET

HOST = "192.168.1.34"
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
        data = data.decode()
        root = ET.fromstring(data)
        
        name = str(root.find('name').text)
        timestamp = float(root.find('time').text)
        rotation = root.find('coordinate/rotation')
        rot_e1 = float(rotation.find('e1').text)
        rot_e2 = float(rotation.find('e2').text)
        rot_e3 = float(rotation.find('e3').text)
        rot_e4 = float(rotation.find('e4').text)
        rot_bol = bool(rotation.find('condition').text)
        translation = root.find('coordinate/translation')
        trans_x = float(translation.find('x').text)
        trans_y = float(translation.find('y').text)
        trans_z = float(translation.find('z').text)
        trans_bol = bool(translation.find('condition').text)


        print(name)
        print(timestamp)
        print(rot_e2)
        print(trans_bol)
        print(trans_x)
        
        #print(root.find('name').text)
        #print(float(rot_x.text))


        #print(f"server modtog: {data}")



        
        
        
        
        
        
        
        
        
        
        
        
        











