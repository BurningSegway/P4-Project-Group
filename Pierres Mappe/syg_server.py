# echo-server.py

import base64
import socket
import cv2 as cv
import numpy as np
import pickle
import codecs

obj = cv.imread("Pierres Mappe/sygt.png")
obj_base64string = codecs.encode(pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL), "base64").decode('latin1')
obj_reconstituted = pickle.loads(codecs.decode(obj_base64string.encode('latin1'), "base64"))


img = cv.imread("Pierres Mappe/sygt.png")
#cv.imshow("Image", img)
print(img)

HOST = "192.168.138.26"  # Standard loopback interface address (localhost)
PORT = 20001  # Port to listen on (non-privileged ports are > 1023)
img_str = str(img)
msg = str.encode(img_str)
msg = base64.b64encode(img)

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
                conn.sendto(obj_base64string, addr)