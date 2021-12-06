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

# popup window for ace value


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
    global value
    value = 0
    if card[:2] == "10" or card[:2] == "11" or card[:2] == "12" or card[:2] == "13":
        value = 10
    # Choose Ace value here
    elif card[0] == "1":    
        # Set the value for the ace
        def setValue(num):
            global value
            if num == 1:
                value = 1
            else:
                value = 11 
            popup.destroy()
    
        popup = Toplevel(root)
        popup.title("Ace Value")

        l = Label(popup, text="Would you like the Ace to be a 1 or 11?")
        l.grid(row=0, column=0)

        b1 = Button(popup, text="1", command=lambda: setValue(1))
        b1.grid(row=1, column=0)
        b1.config(state=NORMAL)

        b2 = Button(popup, text="11", command=lambda: setValue(11))
        b2.grid(row=2, column=0)
        b2.config(state=NORMAL)

        if 11 + handValue > 21:
            b2.config(state=DISABLED)

        root.wait_window(popup)
    else:
        value = int(card[0])

    return value

# formatting to display cards in GUI
def cardDisplay(card):
    if card[:2] == "10":
        return "10" + card[2:]
    elif card[:2] == "11":
        return "Jack" + card[2:]
    elif card[:2] == "12":
        return "Queen" + card[2:]
    elif card[:2] == "13":
        return "King" + card[2:]
    elif card[0] == "1":
        return "Ace" + card[1:]
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
