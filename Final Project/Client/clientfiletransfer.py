import socket, json
from pathlib import Path
from os import chdir

host = "127.0.0.1"
port = 50166

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.connect((host,port))
print("Welcome to the final exam file transfer script")

isInvalidUser = True
while isInvalidUser:
    username = input("Please enter your username: ")
    usernameBytes = username.encode()

    mySocket.send(usernameBytes)
    responceBytes = mySocket.recv(1)
    responce = responceBytes.decode()

    print()
    if responce == "A":
        isInvalidUser = False
    else:
        print("Sorry, that is not a valid username.")

jsonBytes = mySocket.recv(5000)
jsonString = jsonBytes.decode()

dictionary = json.loads(jsonString)

print("Thank you. Here is a directory listing of the server's:", dictionary['parentdirectory'],'\n')

isPicking = True
selectedfilename = ""
while isPicking:
    filecount = 0
    directorycount = 0

    for file in dictionary['filenames']:
        filecount += 1
        print(f'{filecount}. {file}')
    for directory in dictionary['directorynames']:
        directorycount += 1
        print(f'{filecount + directorycount}. {directory} (Directory)')

    choice = input("What would you like: ")
    try:
        choice = int(choice)
    except:
        continue
    
    choice -= 1 # To take into account the differnet number scheme
    if choice < filecount:
        choicestring = "F" + str(choice)
        selectedfilename = dictionary['filenames'][choice]
        mySocket.send(choicestring.encode())
        isPicking = False
    elif choice < filecount + directorycount:
        choicestring = "D" + str(choice - filecount)
        mySocket.send(choicestring.encode())
        
        jsonBytes = mySocket.recv(5000)
        jsonString = jsonBytes.decode()

        dictionary = json.loads(jsonString)
        print("Here is a directory listing of the server's:", dictionary['parentdirectory'],'\n')
        continue

chdir(Path(__file__).resolve().parent)
print("Receiving", selectedfilename, "...")
with open(selectedfilename, "wb") as file:
    while True:
        fileBytes = mySocket.recv(1024)
        if not fileBytes:
            #transmission is done
            break
        file.write(fileBytes)

print("File saved to client directory as", selectedfilename, "\n\nThank you. Have a nice day!")
mySocket.close()

