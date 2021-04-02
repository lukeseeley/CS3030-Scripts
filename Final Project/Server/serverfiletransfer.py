import socket, re, json
from pathlib import Path, WindowsPath
from os import chdir

host = ""
port = 50166

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind((host,port))
mySocket.listen(1)
print("Waiting to connect...")
conn, address = mySocket.accept()
user = ""
isInvalidUser = True
expression = r'[A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9]-[a-z]' # ABC1234-d # 3 upper letters 4 digits - 1 lower letter
print("Connected, now waiting for username...")
while isInvalidUser:
    userBytes = conn.recv(2000)
    user = userBytes.decode()
    matches = re.match(expression, user, re.S)
    if matches:
        print("Valid Username received")
        conn.send("A".encode()) # A for accepted
        isInvalidUser = False
    else:
        print("Invalid username received")
        conn.send("D".encode()) # D for denied

parent = Path(__file__).resolve().parent
chdir(Path(__file__).resolve().parent)

directories = [x for x in parent.iterdir() if x.is_dir()]
directorynames = []
for path in directories:
    parts = []
    if isinstance(path, WindowsPath):
        parts = str(path).split('\\')
    else:
        parts = str(path).split('/')
    directory = parts[-1]
    directorynames.append(directory)

files = [x for x in parent.iterdir() if not x.is_dir()]
filenames = []
for path in files:
    parts = []
    if isinstance(path, WindowsPath):
        parts = str(path).split('\\')
    else:
        parts = str(path).split('/')
    
    file = parts[-1]
    filenames.append(file)

clientDictionary = {
    'parentdirectory': str(parent),
    'directorynames': directorynames,
    'filenames': filenames
}

dictJson = json.dumps(clientDictionary)
jsonBytes = dictJson.encode()

print("Transmitting JSON package")
conn.send(jsonBytes)

isPicking = True
selectedfileindex = -1
while isPicking:
    responceBytes = conn.recv(5) #F/B for file then the number of the requested file/Directory
    responce = responceBytes.decode()
    print(user, "requested", responce)

    typeing = responce[0]
    index = int(responce[1:])

    if typeing == "F":
        selectedfileindex = index
        isPicking = False
    elif typeing == "D":
        chdir(clientDictionary['directorynames'][index])
        parent = Path.cwd()

        directories = [x for x in parent.iterdir() if x.is_dir()]
        directorynames = []
        for path in directories:
            parts = []
            if isinstance(path, WindowsPath):
                parts = str(path).split('\\')
            else:
                parts = str(path).split('/')
            directory = parts[-1]
            directorynames.append(directory)

        files = [x for x in parent.iterdir() if not x.is_dir()]
        filenames = []
        for path in files:
            parts = []
            if isinstance(path, WindowsPath):
                parts = str(path).split('\\')
            else:
                parts = str(path).split('/')
            
            file = parts[-1]
            filenames.append(file)

        clientDictionary = {
            'parentdirectory': str(parent),
            'directorynames': directorynames,
            'filenames': filenames
        }

        dictJson = json.dumps(clientDictionary)
        jsonBytes = dictJson.encode()

        print("Transmitting JSON package for new directory")
        conn.send(jsonBytes)
    else:
        raise Exception("Unexpected client request")

#Begin transmitting 
filename = clientDictionary['filenames'][selectedfileindex]
filedirectory = Path.cwd()
print("Transmitting",filename, "now...")
with open(filename, "rb") as file:
    while True:
        fileBytes = file.read(1024)
        if not fileBytes:
            # Transmission is done
            conn.send(bytes())
            break
        conn.send(fileBytes)

print("Transmission complete.")
chdir(Path(__file__).resolve().parent)

file = ""
try:
    file = open("servertransferlog.txt", "x")
except:
    file = open("servertransferlog.txt", "a")

file.write(f"User: {user} copied the file named: {filename} from: {filedirectory}")

conn.close()





