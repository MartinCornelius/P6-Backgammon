namespace Backgammon;

public class Dice
{
    private Random random;
    public int value { get; set; }
    public Dice()
    {
        this.random = new Random();
    }
    public void Roll()
    {
        this.value = this.random.Next(1, 7);
    }
}