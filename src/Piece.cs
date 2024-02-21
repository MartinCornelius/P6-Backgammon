namespace Backgammon;

public class Piece
{
    private Color _color;

    public Piece(Color color)
    {
        this._color = color;
    }
    public Color GetColor()
    {
        return this._color;
    }
}

