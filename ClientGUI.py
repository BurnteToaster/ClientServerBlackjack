from tkinter import *
from tkinter import ttk
from socket import *

hand = []
handValue = 0
serverResponse = ""

serverName = 'localhost'
serverPort = 6789
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

root = Tk()
root.title("Blackjack")

statusLabel = Label(root, text="Waiting for game to start...")
statusLabel.grid(row=0, column=0)

gameLabel = Label(root, text="Welcome to Blackjack!")
gameLabel.grid(row=1, column=0)

responseLabel = Label(root, text="")
responseLabel.grid(row=2, column=0)

# add hand label when game starts

# Player start function
def start():
    clientSocket.send("start round\n".encode())
    global hand
    hand = []
    global handValue
    handValue = 0
    statusLabel.config(text="New round started!")
    gameLabel.config(text="Your hand value is: " + str(handValue))
    hitButton.config(state=NORMAL)
    standButton.config(state=NORMAL)

# starts game for players
startButton = Button(root, text="Start", command=start)
startButton.grid(row=97, column=0)

# gets the value of a card from the server
# jack king queen and ace are all worth 10
def cardValue(card):
    value = 0
    if card[:2] == "10" or card[:2] == "11" or card[:2] == "12" or card[:2] == "13":
        value = 10
    elif card[0] == "1":
        value = str(input("Ace! Enter value 1 or 11: "))
    else:
        value = int(card[0])
    #later add aces to be worth 11
    return value

def cardDisplay(card):
    if card[:2] == "10":
        return "10" + card[2:]
    elif card[:2] == "11":
        return "Jack" + card[2:]
    elif card[:2] == "12":
        return "Queen" + card[2:]
    elif card[:2] == "13":
        return "King" + card[2:]
    else:
        return card[0] + " " + card[2:]

# Player hit function
def hit():
    clientSocket.send("hit\n".encode())
    serverResponse = clientSocket.recv(1024)
    print("Server Response: " + serverResponse.decode())
    hand.append(cardDisplay(serverResponse[:-2].decode()))
    value = cardValue(serverResponse.decode())
    
    global handValue
    handValue += value

    # check if handValue is over 21
    if handValue > 21:
        gameLabel.config(text="Bust! You lose!")
        statusLabel.config(text="Waiting for other player...")
        hitButton.config(state=DISABLED)
        standButton.config(state=DISABLED)

    elif handValue == 21:
        gameLabel.config(text="Blackjack!")
        statusLabel.config(text="Waiting for other player...")
        hitButton.config(state=DISABLED)
        standButton.config(state=DISABLED)
        clientSocket.send("game over\n".encode())
        clientSocket.send((str(handValue)+"\n").encode())
        print(hand)
        winner = clientSocket.recv(1024)
        gameLabel.config(text="Winner: " + winner.decode())

    else:
        gameLabel.config(text="Your hand value is: " + str(handValue))
        statusLabel.config(text="Waiting for other player...")
        # change display card here
        responseLabel.config(text=cardDisplay(serverResponse[:-2].decode()))

hitButton = Button(root, text="Hit", command=hit)
hitButton.grid(row=98, column=0)
hitButton.config(state=DISABLED)

# Player stand function
def stand():
    clientSocket.send("game over\n".encode())
    clientSocket.send((str(handValue)+"\n").encode())
    print(hand)
    winner = clientSocket.recv(1024)
    gameLabel.config(text="Winner: " + winner.decode())

standButton = Button(root, text="Stand", command=stand)
standButton.grid(row=99, column=0)
standButton.config(state=DISABLED)

# buttons quits game
quitButton = Button(root, text="Quit", command=root.destroy)
quitButton.grid(row=100, column=0)

root.mainloop()
clientSocket.close()
