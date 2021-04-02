import socket 

host = "127.0.0.1"
port = 1338

#Note that I won't need to create a port for the client, the OS handles that for me

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.connect((host, port))

myString = "Ping"
clientByteMessage = myString.encode()

mySocket(clientByteMessage)
print("I sent the message")

bytesFromServer = mySocket.recv(2000)
result = bytesFromServer.decode()

print(result)