namespace Backgammon;

public class Program
{
    public static void Main(string[] args)
    {
        Player player1 = new Player("Martim", Color.black);
        Player player2 = new Player("Martin", Color.white);

        Board board = new Board();
        board.InitBoard();

        foreach(var item in board.GetBoardState())
        {
            foreach(var dingle in item){
                Console.Write("{0} ", dingle.GetColor());
            }
            Console.Write("\n");
        }
        Console.WriteLine("_______________________");
        board.UpdatePiecePosition(1, 1, player1);

        foreach(var item in board.GetBoardState())
        {
            foreach(var dingle in item){
                Console.Write("{0} ", dingle.GetColor());
            }
            Console.Write("\n");
        }
    }
}