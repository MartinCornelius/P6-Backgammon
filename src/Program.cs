namespace Backgammon;

public class Program
{
    public static void Main(string[] args)
    {
        Console.Clear();

        Player player1 = new Player("Martim", Color.black);
        Player player2 = new Player("Martin", Color.white);

        Board board = new Board();
        board.InitBoard();
        board.Print();

        board.MovePiece(1, 4, player1);
        board.Print();
    }
}