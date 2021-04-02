import socket
import random

def makeChoice():
    isWaiting = True
    while isWaiting:
        choice = input("Make a choice:\n0 - Rock\n1 - Paper \n2 - Scissors\n3 - Let AI take over\n")
        
        if choice != "0" and choice != "1" and choice != "2" and choice != "3":
            print("Please enter a number between 0 and 3")
        else:
            isWaiting = False
            return choice

def AIChoice():
    choice = random.randrange(0,3)
    return str(choice)

def checkResults(choice, opponentChoice):
    cResult = ""
    oResult = ""
    result = ""
    value = 10

    if (choice == "0"):
        cResult = "Rock"
        if (opponentChoice == "0"):
            oResult = "Rock"
            result = "it's a tie"
            value = 0 #A tie
        elif (opponentChoice == "1"):
            oResult = "Paper"
            result = "you lost"
            value = -1 #A loss
        else:
            oResult = "Scissors"
            result = "you won"
            value = 1 #A win

    elif (choice == "1"):
        cResult = "Paper"
        if (opponentChoice == "0"):
            oResult = "Rock"
            result = "you won"
            value = 1 #A win
        elif (opponentChoice == "1"):
            oResult = "Paper"
            result = "it's a tie"
            value = 0 #A tie
        else:
            oResult = "Scissors"
            result = "you lost"
            value = -1 #A loss

    else:
        cResult = "Scissors"
        if (opponentChoice == "0"):
            oResult = "Rock"
            result = "you lost"
            value = -1 #A loss
        elif (opponentChoice == "1"):
            oResult = "Paper"
            result = "you won"
            value = 1 #A win
        else:
            oResult = "Scissors"
            result = "it's a tie"
            value = 0 #A tie
    
    print(f'You choose {cResult}, and your opponent choose {oResult}. {result}!')
    return value

def askPlayAgain():
    isWaiting = True
    while isWaiting:
        choice = input("Play again? (Y/N): ").upper()
        if choice == "Y" or choice == "N":
            isWaiting = False
            return choice

def runServer():
    host = ""
    port = 5337

    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.bind((host, port))
    mySocket.listen(1)

    print("Waiting for opponent to connect...")
    conn, address = mySocket.accept()

    wins = 0
    losses = 0
    isStillPlaying = True
    isAI = False
    while isStillPlaying:
        choice = ""
        if not isAI:
            choice = makeChoice()
            if choice == "3":
                isAI = True
                continue
        else:
            choice = AIChoice()
            print(f"AI choose {choice}")

        print("Waiting for opponent...")
        opponentBytes = conn.recv(2000)
        opponentResult = opponentBytes.decode()
        
        if(opponentResult == "R"):
            #Opponent is ready then
            byteChoice = choice.encode()
            conn.send(byteChoice)
        
        opponentBytes = conn.recv(2000)
        opponentChoice = opponentBytes.decode()

        result = checkResults(choice, opponentChoice) #-1 for a loss, 0 for a tie, and 1 for a win
        if (result == 1):
            wins += 1
        elif (result == -1):
            losses += 1
        
        print(f'So far you have won {wins} games, and lost {losses} games.')
        again = ""
        if not isAI:
            again = askPlayAgain()
        else:
            print("AI will play again")
            again = "Y"

        print("Waiting for opponent...")
        opponentBytes = conn.recv(2000)
        opponentAgain = opponentBytes.decode()

        againBytes = again.encode()
        conn.send(againBytes)

        if(again == "N"):
            isStillPlaying = False
            print("You choose to end the game, have a nice day!")
        elif(opponentAgain == "N"):
            isStillPlaying = False
            print("Your opponent choose to end the game, have a nice day!")



def runClient():
    host = "127.0.0.1"
    port = 5337

    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((host, port))

    wins = 0
    losses = 0
    isStillPlaying = True
    isAI = False
    while isStillPlaying:
        choice = ""
        if not isAI:
            choice = makeChoice()
            if choice == "3":
                isAI = True
                continue
        else:
            choice = AIChoice()
            print(f"AI choose {choice}")
        
        string = "R"
        mySocket.send(string.encode())

        print("Waiting for opponent...")
        opponentBytes = mySocket.recv(2000)
        opponentChoice = opponentBytes.decode()

        byteChoice = choice.encode()
        mySocket.send(byteChoice)

        result = checkResults(choice, opponentChoice) #-1 for a loss, 0 for a tie, and 1 for a win
        if (result == 1):
            wins += 1
        elif (result == -1):
            losses += 1

        print(f'So far you have won {wins} games, and lost {losses} games.')
        again = ""
        if not isAI:
            again = askPlayAgain()
        else:
            print("AI will play again")
            again = "Y"

        againBytes = again.encode()
        mySocket.send(againBytes)

        print("Waiting for opponent...")
        opponentBytes = mySocket.recv(2000)
        opponentAgain = opponentBytes.decode()

        if(again == "N"):
            isStillPlaying = False
            print("You choose to end the game, have a nice day!")
        elif(opponentAgain == "N"):
            isStillPlaying = False
            print("Your opponent choose to end the game, have a nice day!")


        

player = "" # Player A is server, and player B is client
isWaiting = True
print("Welcome to Rock Paper Scissors")
while isWaiting:
    player = input("Are you player A or B: ")
    player = player.upper()
    print(player)
    if player == "A" or player == "B":
        isWaiting = False

if (player == "A"):
    runServer()
else:
    runClient()


