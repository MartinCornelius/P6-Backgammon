namespace Backgammon;

public class Program
{
    public static void Main(string[] args)
    {
        Console.Clear();

        // Handle new players
        Player player1 = new Player("Player1", Color.black);
        Player player2 = new Player("Player2", Color.white);

        // Create new game
        //Game game = new Game(player1, player2);
        Gui g = new Gui();
    }
}