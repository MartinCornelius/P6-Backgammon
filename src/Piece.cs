namespace Backgammon;

public class Piece
{
    private string color;

    public Piece(string color)
    {
        this.color = color;
    }
    public string GetColor()
    {
        return this.color;
    }
}

