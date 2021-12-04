
import java.util.*;

public class Deck {
    List<String> cardList;

    public static int index = 0;

    public Deck() {
        cardList = new ArrayList<String>();
        for (int i = 0; i < 4; i++) {
            for (int j = 1; j < 14; j++) {
                if (i == 0) {
                    cardList.add(j + " of Spades");
                } else if (i == 1) {
                    cardList.add(j + " of Hearts");
                } else if (i == 2) {
                    cardList.add(j + " of Diamonds");
                } else if (i == 3) {
                    cardList.add(j + " of Clubs");
                }
            }
        }
        Collections.shuffle(cardList);
    }
}
