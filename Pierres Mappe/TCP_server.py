# Initialization
import socket
localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024
msgFromServer = "Hello TCP Creature, you dare contact meeeeee????"
bytesToSend = str.encode(msgFromServer)


# Create a datagram socket, bind to address and ip
TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPServerSocket.bind((localIP, localPort))
print("TCP Server klar")

# Listen for incoming datagrams
while(True):

    bytesAddressPair = TCPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)
    print(clientMsg)
    print(clientIP)
    # Sending a reply to client
    TCPServerSocket.sendto(bytesToSend, address)
