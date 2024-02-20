namespace Backgammon;

public class DicePair
{
    public Dice d1;
    public Dice d2;
    public DicePair()
    {
        this.d1 = new Dice();
        this.d2 = new Dice();
    }
    public void Roll()
    {
        this.d1.Roll();
        this.d2.Roll();
    }

    public Boolean IsDoubleDice()
    {
        if (this.d1.value == this.d2.value)
            return true;

        return false;
    }
}