'''
 * ClientGUI for blackjack game
 * handles the GUI and keeps track of player actions for the game
 * 
 * @author Matthew Mercado & Pratosh Brahmbhatt
 * @date December 6, 2021
'''

from tkinter import *
from tkinter import ttk
from socket import *
# (not currently using time)
import time

# initialize global variables
hand = []
handValue = 0
serverResponse = ""

# ask for server address and establish connection
serverName = 'localhost'
serverName = input("Enter server address: ")
serverPort = 6789
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# initializes the GUI
root = Tk()
root.title("Blackjack")
root.config(bg="#3A3B3C")
root.attributes('-fullscreen', True)
root.resizable(True,True)
#commented out because it is relative path
#root.iconbitmap('C:/Users/pbrah/Downloads\Project 3/BlackJack/src/blackjackicon.ico')

def disable_event():
    pass

# Opens popup to enter player name could be used for other things
name = Toplevel(root)
name.title("Enter player name")
name.config(bg="#3A3B3C")
window_width = 600
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
name.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
name.resizable(False,False)
name.protocol("WM_DELETE_WINDOW", disable_event)

inputBox = Text(name, height=1, width=20)
inputBox.place(relx=0.6, rely=0.5, anchor=E)

# gets player names from popup box
def getInputText(inp):
    gameLabel["text"]="Welcome to Blackjack, "+inp+"!"
    name.destroy()

enterButton = Button(name, text="Enter", fg="white", bg="#5A5B5C", command=lambda: getInputText((inputBox.get(1.0, "end-1c"))))
enterButton.place(relx=0.7, rely=0.5, anchor=W)
enterButton.config(width=10)

statusLabel = Label(root, text="Waiting to start...", fg="white", bg="#3A3B3C", font=20)
statusLabel.grid(row=0, column=0)
statusLabel.place(relx=0.5, rely=0.05, anchor=CENTER)

gameLabel = Label(root, text="Welcome to Blackjack!", fg="white", bg="#3A3B3C", font=("Papyrus", 60))
gameLabel.grid(row=1, column=0)
gameLabel.place(relx=0.5, rely=0.2, anchor=CENTER)

responseLabel = Label(root, text="", fg="white", bg="#3A3B3C",font=40)
responseLabel.grid(row=2, column=0)
responseLabel.place(relx=0.5, rely=0.3, anchor=CENTER)

# start button function, sends start message to server
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
            
        # Create popup window to choose value of ace
        popup = Toplevel(root)
        popup.title("Ace Value")
        popup.config(bg="#3A3B3C")
        window_width = 300
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        popup.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        popup.resizable(False,False)
        popup.protocol("WM_DELETE_WINDOW", disable_event)

        l = Label(popup, text="Would you like the Ace to be a 1 or 11?", 
                    fg="white", bg="#3A3B3C", font=25)
        l.grid(row=0, column=0)
        l.place(relx=0.5, rely=0.25, anchor=CENTER)

        b1 = Button(popup, text="1", fg="white", bg="#5A5B5C", command=lambda: setValue(1))
        b1.grid(row=1, column=0)
        b1.config(state=NORMAL, width=4)
        b1.place(relx=0.25, rely=0.5)

        b2 = Button(popup, text="11", fg="white", bg="#5A5B5C", command=lambda: setValue(11))
        b2.grid(row=2, column=0)
        b2.config(state=NORMAL, width=4)
        b2.place(relx=0.65, rely=0.5)

        # Limits to player can't go over 21 willingly or by accident
        if 11 + handValue > 21:
            b2.config(state=DISABLED, width=4)

        root.wait_window(popup)
    else:
        value = int(card[0])

    return value

# Formatting to display cards in GUI since server sends numbers
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

# Sends hit command to server, updates GUI
def hit():
    clientSocket.send("hit\n".encode())
    serverResponse = clientSocket.recv(1024)
    # If the server runs out of cards, the server needs to be restarted
    if serverResponse.decode() == "deck ran out\n":
        statusLabel.config(text="Deck ran out! Restart Server to continue.")
        hitButton.config(state=DISABLED)
        standButton.config(state=DISABLED)
        startButton.config(state=DISABLED)
        
    # Prints out the server response
    print("Server Response: " + serverResponse.decode())

    # Adds the card and the value to the hand
    hand.append(cardDisplay(serverResponse[:-2].decode()))
    value = cardValue(serverResponse.decode())
    global handValue
    handValue += value

    # if the player busts, the game ends
    if handValue > 21:
        gameLabel.config(text="Bust! You lose!")
        statusLabel.config(text="Waiting for your move...")
        hitButton.config(state=DISABLED)
        standButton.config(state=DISABLED)
        startButton.config(state=NORMAL)
        responseLabel.config(text=cardDisplay(serverResponse[:-2].decode()))

    # if the player has 21, turn over, and dealer plays
    elif handValue == 21:
        gameLabel.config(text="Blackjack!")
        statusLabel.config(text="Waiting for your move...")
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
        statusLabel.config(text="Waiting for your move...")
        # change display card here
        responseLabel.config(text=cardDisplay(serverResponse[:-2].decode()))

# Sends game over command and the hand value to server and receives winner from server
def stand():
    clientSocket.send("game over\n".encode())
    clientSocket.send((str(handValue)+"\n").encode())
    print(hand)
    winner = clientSocket.recv(1024)
    gameLabel.config(text="Winner: " + winner.decode())
    startButton.config(state=NORMAL)

# starts game for players
startButton = Button(root, text="Start", fg="white", bg="#5A5B5C", command=start)
startButton.grid(row=97, column=0)
startButton.place(relx=0.5, rely=0.5, anchor=CENTER)
startButton.config(width=30, height=5)

# button deals player a card
hitButton = Button(root, text="Hit", fg="white", bg="#5A5B5C", command=hit)
hitButton.grid(row=98, column=0)
hitButton.config(state=DISABLED, width=30, height=5)
hitButton.place(relx=0.5, rely=0.6, anchor=CENTER)

# button keeps your value
standButton = Button(root, text="Stand", fg="white", bg="#5A5B5C", command=stand)
standButton.grid(row=99, column=0)
standButton.config(state=DISABLED,width=30, height=5)
standButton.place(relx=0.5, rely=0.7, anchor=CENTER)

# button quits game
quitButton = Button(root, text="Quit", fg="white", bg="#5A5B5C", command=root.destroy)
quitButton.grid(row=100, column=0)
quitButton.place(relx=0.5, rely=0.8, anchor=CENTER)
quitButton.config(width=30, height=5)

root.mainloop()
clientSocket.close()
