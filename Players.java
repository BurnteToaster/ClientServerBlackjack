public class Players {
    
    private String name;
    private boolean bust;

    public Players(String name, boolean bust) {
        this.name = name;
        this.bust = bust;
    }

    public String getName() {
        return name;
    }

    public boolean getBust() {
        return bust;
    }
}
