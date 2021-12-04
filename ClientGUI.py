from tkinter import *
from tkinter import ttk
from socket import *
import time

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

# start button function
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
    startButton.config(state=DISABLED)

# starts game for players
startButton = Button(root, text="Start", command=start)
startButton.grid(row=97, column=0)

# gets the value of a card from the server
# jack king queen are all worth 10
def cardValue(card):
    value = 0
    if card[:2] == "10" or card[:2] == "11" or card[:2] == "12" or card[:2] == "13":
        value = 10
    #We need to fix this somehow
    elif card[0] == "1":
        value = str(input("Ace! Enter value 1 or 11: "))
    else:
        value = int(card[0])
    
    return value

# formatting to display cards
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

# hit button function
def hit():
    clientSocket.send("hit\n".encode())
    serverResponse = clientSocket.recv(1024)
    print("Server Response: " + serverResponse.decode())
    hand.append(cardDisplay(serverResponse[:-2].decode()))
    value = cardValue(serverResponse.decode())
    
    global handValue
    handValue += value

    # if the player busts, the game ends
    if handValue > 21:
        gameLabel.config(text="Bust! You lose!")
        statusLabel.config(text="Waiting for other player...")
        hitButton.config(state=DISABLED)
        standButton.config(state=DISABLED)
        startButton.config(state=NORMAL)

    # if the player has 21, turn over, and dealer plays
    elif handValue == 21:
        gameLabel.config(text="Blackjack!")
        statusLabel.config(text="Waiting for other player...")
        hitButton.config(state=DISABLED)
        standButton.config(state=DISABLED)
        time.sleep(1.5)
        clientSocket.send("game over\n".encode())
        clientSocket.send((str(handValue)+"\n").encode())
        print(hand)
        winner = clientSocket.recv(1024)
        gameLabel.config(text="Winner: " + winner.decode())
        startButton.config(state=NORMAL)

    # if the player has not busted, the player can hit again
    else:
        gameLabel.config(text="Your hand value is: " + str(handValue))
        statusLabel.config(text="Waiting for other player...")
        # change display card here
        responseLabel.config(text=cardDisplay(serverResponse[:-2].decode()))

hitButton = Button(root, text="Hit", command=hit)
hitButton.grid(row=98, column=0)
hitButton.config(state=DISABLED)

# stand button function
def stand():
    clientSocket.send("game over\n".encode())
    clientSocket.send((str(handValue)+"\n").encode())
    print(hand)
    winner = clientSocket.recv(1024)
    gameLabel.config(text="Winner: " + winner.decode())
    startButton.config(state=NORMAL)

standButton = Button(root, text="Stand", command=stand)
standButton.grid(row=99, column=0)
standButton.config(state=DISABLED)

# buttons quits game
quitButton = Button(root, text="Quit", command=root.destroy)
quitButton.grid(row=100, column=0)

root.mainloop()
clientSocket.close()
