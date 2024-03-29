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
        if (this.d1.Value == this.d2.Value)
            return true;

        return false;
    }

    public (int d1, int d2) GetDiceValues()
    {
        return (this.d1.Value, this.d2.Value);
    }
}