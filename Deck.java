
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

// old code
// public Deck(){

// cardList=new ArrayList<>();

// cardList.add(new Card("Ace","Spades"));
// cardList.add(new Card("2","Spades")); cardList.get(1).setValue(2);
// cardList.add(new Card("3","Spades")); cardList.get(2).setValue(3);
// cardList.add(new Card("4","Spades")); cardList.get(3).setValue(4);
// cardList.add(new Card("5","Spades")); cardList.get(4).setValue(5);
// cardList.add(new Card("6","Spades")); cardList.get(5).setValue(6);
// cardList.add(new Card("7","Spades")); cardList.get(6).setValue(7);
// cardList.add(new Card("8","Spades")); cardList.get(7).setValue(8);
// cardList.add(new Card("9","Spades")); cardList.get(8).setValue(9);
// cardList.add(new Card("10","Spades")); cardList.get(9).setValue(10);
// cardList.add(new Card("Jack","Spades")); cardList.get(10).setValue(10);
// cardList.add(new Card("Queen","Spades")); cardList.get(11).setValue(10);
// cardList.add(new Card("King","Spades")); cardList.get(12).setValue(10);

// cardList.add(new Card("Ace","Hearts"));
// cardList.add(new Card("2","Hearts")); cardList.get(14).setValue(2);
// cardList.add(new Card("3","Hearts")); cardList.get(15).setValue(3);
// cardList.add(new Card("4","Hearts")); cardList.get(16).setValue(4);
// cardList.add(new Card("5","Hearts")); cardList.get(17).setValue(5);
// cardList.add(new Card("6","Hearts")); cardList.get(18).setValue(6);
// cardList.add(new Card("7","Hearts")); cardList.get(19).setValue(7);
// cardList.add(new Card("8","Hearts")); cardList.get(20).setValue(8);
// cardList.add(new Card("9","Hearts")); cardList.get(21).setValue(9);
// cardList.add(new Card("10","Hearts")); cardList.get(22).setValue(10);
// cardList.add(new Card("Jack","Hearts")); cardList.get(23).setValue(10);
// cardList.add(new Card("Queen","Hearts")); cardList.get(24).setValue(10);
// cardList.add(new Card("King","Hearts")); cardList.get(25).setValue(10);

// cardList.add(new Card("Ace","Diamonds"));
// cardList.add(new Card("2","Diamonds")); cardList.get(27).setValue(2);
// cardList.add(new Card("3","Diamonds")); cardList.get(28).setValue(3);
// cardList.add(new Card("4","Diamonds")); cardList.get(29).setValue(4);
// cardList.add(new Card("5","Diamonds")); cardList.get(30).setValue(5);
// cardList.add(new Card("6","Diamonds")); cardList.get(31).setValue(6);
// cardList.add(new Card("7","Diamonds")); cardList.get(32).setValue(7);
// cardList.add(new Card("8","Diamonds")); cardList.get(33).setValue(8);
// cardList.add(new Card("9","Diamonds")); cardList.get(34).setValue(9);
// cardList.add(new Card("10","Diamonds")); cardList.get(35).setValue(10);
// cardList.add(new Card("Jack","Diamonds")); cardList.get(36).setValue(10);
// cardList.add(new Card("Queen","Diamonds")); cardList.get(37).setValue(10);
// cardList.add(new Card("King","Diamonds")); cardList.get(38).setValue(10);

// cardList.add(new Card("Ace","Clubs"));
// cardList.add(new Card("2","Clubs")); cardList.get(40).setValue(2);
// cardList.add(new Card("3","Clubs")); cardList.get(41).setValue(3);
// cardList.add(new Card("4","Clubs")); cardList.get(42).setValue(4);
// cardList.add(new Card("5","Clubs")); cardList.get(43).setValue(5);
// cardList.add(new Card("6","Clubs")); cardList.get(44).setValue(6);
// cardList.add(new Card("7","Clubs")); cardList.get(45).setValue(7);
// cardList.add(new Card("8","Clubs")); cardList.get(46).setValue(8);
// cardList.add(new Card("9","Clubs")); cardList.get(47).setValue(9);
// cardList.add(new Card("10","Clubs")); cardList.get(48).setValue(10);
// cardList.add(new Card("Jack","Clubs")); cardList.get(49).setValue(10);
// cardList.add(new Card("Queen","Clubs")); cardList.get(50).setValue(10);
// cardList.add(new Card("King","Clubs")); cardList.get(51).setValue(10);

// Collections.shuffle(cardList);
// }
