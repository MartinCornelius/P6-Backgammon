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

        MainMenu menu = new MainMenu("Backgammon - P6 2024");
        menu.Add(new MenuItem("Start new game", board));
        menu.Add(new MenuItem("Quit"));
        menu.Start();
    }
}