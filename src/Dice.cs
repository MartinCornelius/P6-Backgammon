namespace Backgammon;

public class Dice
{
    private Random random;
    public int Value { get; set; }
    public Dice()
    {
        this.random = new Random();
    }
    public void Roll()
    {
        this.Value = this.random.Next(1, 7);
    }
}