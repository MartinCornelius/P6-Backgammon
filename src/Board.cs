namespace Backgammon;

public class Board
{
    private List<Piece>[] state;
    public Board()
    {
        this.state = new List<Piece>[26];
        for (int i = 0; i < 26; i++)
        {
            this.state[i] = new List<Piece>();
        }
    }

    public List<Piece>[] GetBoardState()
    {
        List<Piece>[] output = (List<Piece>[])state.Clone();
        return output;
    }
    public void InitBoard()
    {
        List<Tuple<int, int, string>> defaultList = new List<Tuple<int, int, string>>()
        {
            new (1, 2, "Black"),
            new (6, 5, "White"),
            new (8, 3, "White"),
            new (12, 5, "Black"),
            new (13, 5, "White"),
            new (17, 3, "Black"),
            new (19, 5, "Black"),
            new (24, 2, "White")
        };
        foreach (Tuple<int, int, string> tuple in defaultList)
        {
            this.fillTile(tuple.Item1, tuple.Item2, tuple.Item3);
        }
    }

    public void InitBoard(List<Tuple<int, int, string>> configList)
    {
        foreach (Tuple<int, int, string> tuple in configList)
        {
            this.fillTile(tuple.Item1, tuple.Item2, tuple.Item3);
        }
    }
    private void fillTile(int index, int amount, string color)
    {
        for (int i = 0; i < amount; i++)
        {
            this.state[index].Add(new Piece(color));
        }
    }
}