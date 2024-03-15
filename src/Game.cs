namespace Backgammon;

public class Game
{
    private Board board;
    private Player currentPlayer;
    private Player player1;
    private Player enemyPlayer;
    private Player player2;
    private DicePair dice;

    public Game(Player p1, Player p2)
    {
        Console.WriteLine("[STARTING] a new game has been started...");

        this.player1 = p1;
        this.player2 = p2;

        this.currentPlayer = player1;
        this.enemyPlayer = player2;
        this.dice = new DicePair();

        this.board = new Board();
        this.board.Print();

        do
        {
            this.Turn();
            this.currentPlayer = this.currentPlayer == this.player1 ? this.player2 : this.player1;
        } while (!board.HasWon());
    }

    private void Turn()
    {
        Console.WriteLine("\n----------------------------------------------");
        Console.WriteLine("\tCurrent player: " + this.currentPlayer.Name + " with the " + (currentPlayer.Color == Color.white ? "W" : "B") + " pieces.");
        Console.WriteLine("----------------------------------------------");

        Console.WriteLine("[ROLLING] rolling the dice...");
        this.dice.Roll();

        // Values of the dice
        // TODO: check for double dice
        (int d1, int d2) = this.dice.GetDiceValues();

        int currentDice = -1;
        int positionToMove = -1;
        do
        {
            Console.WriteLine("You have rolled: (1)" + d1 + " and (2)" + d2);
            Console.WriteLine("Please pick a dice (1) or (2):");

            switch (Console.ReadKey().Key)
            {
                case ConsoleKey.D1:
                    currentDice = d1;
                    break;
                case ConsoleKey.D2: // 2 on the keyboard
                    currentDice = d2;
                    break;
            }

            Console.WriteLine("\nPlease pick a piece to move:");
            positionToMove = Int32.Parse(Console.ReadLine()!);
        } while (!board.MovePiece(positionToMove, currentDice, this.currentPlayer, this.enemyPlayer));
        this.board.Print();

        currentDice = currentDice == d1 ? d2 : d1;
        do
        {
            // Change currentDice
            Console.WriteLine("\nPlease pick a piece to move " + currentDice + " moves:");
            positionToMove = Int32.Parse(Console.ReadLine()!);
        } while (!board.MovePiece(positionToMove, currentDice, this.currentPlayer, this.enemyPlayer));
        this.board.Print();
    }
}