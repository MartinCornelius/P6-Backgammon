namespace Backgammon;

public class Player
{
    public string Name { get; set; }
    public Color Color { get; set; }
    public int Score { get; set; }
    public bool IsAllHome { get; set; }
    
    public Player(string name, Color color)
    {
        this.Name = name;
        this.Color = color;
        this.Score = 0;
        this.IsAllHome = false;
    }    
}