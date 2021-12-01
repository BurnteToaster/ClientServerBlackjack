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


# gets the value of a card from the server
# jack king queen and ace are all worth 10
def cardValue(card):
    value = 0
    if card[:2] == "10" or card[:2] == "11" or card[:2] == "12" or card[:2] == "13":
        value = 10
    else:
        value = int(card[0])
    #later add aces to be worth 11
    return value

# Player hit function
def hit():
    clientSocket.send("hit\n".encode())
    serverResponse = clientSocket.recv(1024)
    print("Server Response: " + serverResponse.decode())
    hand.append(serverResponse[:-3].decode())
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
        winner = clientSocket.recv(1024)
        gameLabel.config(text="Winner: " + winner.decode())

    else:
        gameLabel.config(text="Your hand is: " + str(handValue))
        statusLabel.config(text="Waiting for other player...")
        responseLabel.config(text=serverResponse[:-3].decode())


hitButton = Button(root, text="Hit", command=hit)
hitButton.grid(row=4, column=0)

# Player stand function
def stand():
    clientSocket.send("stand\n".encode())
    clientSocket.send(str(handValue).encode())
    print(hand)

standButton = Button(root, text="Stand", command=stand)
standButton.grid(row=5, column=0)

# buttons quits game
quitButton = Button(root, text="Quit", command=root.destroy)
quitButton.grid(row=100, column=0)

root.mainloop()
clientSocket.close()