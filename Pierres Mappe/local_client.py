import socket
import cv2 as cv
import numpy as np

msgFromClient = "Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!Din mor!"
bytesToSend = str.encode(msgFromClient)

serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024

# Create a UDP socket on client side
TCPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPClientSocket.connect(serverAddressPort)

# Send to server using created UDP socket
TCPClientSocket.sendto(bytesToSend, serverAddressPort)
msgFromServer = TCPClientSocket.recvfrom(bufferSize)
#img_str = str(msgFromServer[0], encoding='utf-8')
#print(img_str)

img = np.frombuffer(msgFromServer[0], dtype=np.uint8)
print(img)