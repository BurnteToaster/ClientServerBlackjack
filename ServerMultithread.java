import java.io.*;
import java.net.*;
import java.util.*;

/**
 * ServerMultithread class for blackjack game
 * handles all the server side logic for the game
 * 
 * @author Matthew Mercado & Pratosh Brahmbhatt
 * @date December 6, 2021
 */
public class ServerMultithread {

    public static void main(String[] args) throws Exception {
        ServerSocket welcomeSocket = new ServerSocket(6789);
        // Prints out the IP address of the server
        System.out.println(InetAddress.getLocalHost());

        // Establishes connections with clients
        while (true) {
            System.out.println("Waiting for connections");
            Socket connectionSocket = welcomeSocket.accept();
            System.out.println("Connection Recived From Client!");

            new ClientHandler(connectionSocket);
        }
    }
}

/**
 * ClientHandler class handles the client requests per thread
 */
class ClientHandler extends Thread {
    private Socket connectionSocket;
    // somehow get number of clients (not used in this project)
    private int playerNum;

    /**
     * Constructor for the ClientHandler class
     * 
     * @param connectionSocket
     */
    public ClientHandler(Socket connectionSocket) {
        this.connectionSocket = connectionSocket;
        this.start();
    }

    /**
     * This method is called when the thread is started.
     */
    public void run() {

        try {
            Deck deck = new Deck();

            BufferedReader in = new BufferedReader(new InputStreamReader(connectionSocket.getInputStream()));
            PrintWriter out = new PrintWriter(connectionSocket.getOutputStream(), true);

            // Starts rounds with same deck
            while (true) {
                if (in.readLine().equals("start round")) {
                    System.out.println("Starting Game");
                    // call game state
                    blackjackGame(in, out, deck);
                }
            }
        } catch (IOException e) {

        }
    }

    /**
     * Starts a game of blackjack
     * 
     * @param in
     * @param out
     * @throws IOException
     */
    public void blackjackGame(BufferedReader in, PrintWriter out, Deck deck) throws IOException {
        while (true) {
            // Gets client command
            String clientResponse = in.readLine();
            System.out.println("Client: " + clientResponse);

            // send a card on hit
            if (clientResponse.matches("hit")) {
                // if the cards run out print the statement and end the game
                if (Deck.index == 52) {
                    System.out.println("Error! no more cards, restart server");
                    out.println("deck ran out");
                    break;
                } else {
                    // send a card and increment index of cards
                    System.out.println("Sending: " + deck.cardList.get(Deck.index));
                    out.println(deck.cardList.get(Deck.index));
                    Deck.index++;
                }
            }

            // player turn over
            if (clientResponse.matches("game over")) {
                System.out.println("Receiving hand from Client");
                String value = in.readLine();
                System.out.println("Client: " + value);
                // player value
                int pValue = Integer.parseInt(value);
                // dealer value
                int dValue = dealerValue(deck, pValue);

                // check for winners and send to client
                String winner = decideWinner(pValue, dValue);
                System.out.println("Winner: " + winner);
                out.println(winner);
            }

        }
    }

    /**
     * Checks for winner of the game
     * 
     * @param pValue player value
     * @param dValue dealer value
     * @return game winner
     */
    public String decideWinner(int pValue, int dValue) {
        String winner = "";
        if (dValue > 21) {
            System.out.println("Dealer Busts");
            winner += "Dealer Busts with " + dValue;
        } else if (dValue >= pValue) {
            System.out.println("Dealer Wins");
            winner += "Dealer Wins with " + dValue;
        } else if (dValue < pValue) {
            System.out.println("Player Wins");
            winner += "Player Wins, Dealer has " + dValue;
        }
        return winner;
    }

    /**
     * Gets the hand value for the dealer
     * Standard house rules, if the dealer has a value less than 17, he hits
     * or hits until busts or has a greater value than the player
     * 
     * @param deck deck of cards
     * @return dealer value
     */
    public static int dealerValue(Deck deck, int pValue) {
        int total = 0;
        while (total < pValue && total < 17) {
            total += cardValue(deck.cardList.get(Deck.index));
            Deck.index++;
        }
        return total;
    }

    /**
     * Gets the value of the card
     * 
     * @param card card string
     * @return value of the card
     */
    public static int cardValue(String card) {
        int value = 0;
        if (card.contains("10") || card.contains("11") || card.contains("12") || card.contains("13")) {
            value = 10;
        } else {
            value = Integer.parseInt(card.substring(0, 1));
        }
        return value;
    }
}
