import socket 

host = ""
port = 1338

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind((host, port))
mySocket.listen(1)

conn, address = mySocket.accept()
#Wait for the client to send me something

bytesFromClient = mySocket.recv(2000) #Receive up to 2000 bytes

result = bytesFromClient.decode()
print(result)

myString = "Pong"
serverByteMessage = myString.encode()
conn.send(serverByteMessage)
print("I sent the message")