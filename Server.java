
import java.io.*;
import java.net.*;
import java.util.*;

public class Server {
    static Deck deck = new Deck();

    public static void main(String[] args) throws IOException, ClassNotFoundException {
        System.out.println("Waiting for Connection...");

        try {
            ServerSocket socket = new ServerSocket(6789);
            Socket clientSocket = socket.accept();
            System.out.println("Connection Recived From Client!");

            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);

            String clientResponse;

            while (true) {
                // Read a string from client
                clientResponse = in.readLine();
                System.out.println("Client: " + clientResponse);

                // check value of card

                if (clientResponse.matches("hit")) {
                    System.out.println("Sending a new card");
                    System.out.println(deck.cardList.get(Deck.index));
                    out.println(deck.cardList.get(Deck.index) + "\n");
                    Deck.index++;
                }

                if (clientResponse.matches("stand")) {
                    System.out.println("Reciving hand from Client");
                    String value = in.readLine();
                    System.out.println("Total Value: " + value);
                }

                /**
                 * only if all players are done
                 */

                // player turn over
                // checks if player beats dealer
                if (clientResponse.matches("game over")) {
                    int dValue = dealerValue();
                    System.out.println("Reciving hand from Client");
                    String value = in.readLine();
                    int pValue = Integer.parseInt(value);

                    if (dValue > 21) {
                        System.out.println("Dealer Busts");
                        out.println("Dealer Busts");
                    } else if (dValue > pValue) {
                        System.out.println("Dealer Wins");
                        out.println("Dealer Wins");
                    } else if (dValue < pValue) {
                        System.out.println("Player Wins");
                        out.println("Player Wins");
                    } else {
                        System.out.println("Push");
                        out.println("Push");
                    }
                }

                if (Deck.index == 52) {
                    System.out.println("Error! no more cards, restart server");
                    break;
                }
            }
            socket.close();
        } catch (IOException e) {

        }
    }

    public static int dealerValue() {
        int total = 0;
        while (total < 17) {
            total += cardValue(deck.cardList.get(Deck.index));
            Deck.index++;
        }
        return total;
    }

    public static int cardValue(String card) {
        int value = 0;
        if (card.contains("10") || card.contains("11") || card.contains("12") || card.contains("13")) {
            value = 10;
        } else {
            value = Integer.parseInt(card);
        }
        return value;
    }
}
