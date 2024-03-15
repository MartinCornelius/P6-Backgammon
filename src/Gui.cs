using System.Numerics;
using Raylib_cs;

namespace Backgammon;

public class Gui
{
    private const int WIDTH = 900;
    private const int HEIGHT = 600;
    private const int tileWidth = 64;
    private const int tileHeight = 256;
    private const int pieceRadius = 24;

    public Player currentPlayer;
    private Player player1;
    private Player player2;
    public DicePair dice;

    private int selectedTileX = -1;
    private int selectedTileY = -1;

    private Board board;

    public Gui()
    {
        Console.WriteLine("[STARTING] a new game has been started...");

        this.player1 = new Player("Player1", Color.black);
        this.player2 = new Player("Player2", Color.white);

        this.currentPlayer = player1;
        this.dice = new DicePair();
        this.dice.Roll();

        this.board = new Board();
        this.board.Print();

        this.Run();
    }

    public void Run()
    {
        Raylib.InitWindow(WIDTH, HEIGHT, "P6 - Backgammon");
        Raylib.SetTargetFPS(10);

        while (!Raylib.WindowShouldClose())
        {
            if (Raylib.IsMouseButtonPressed(Raylib_cs.MouseButton.Left))
            {
                Vector2 mousePosition = Raylib.GetMousePosition();

                int selectedTileX = (int)(mousePosition.X / tileWidth);
                int selectedTileY = (int)(mousePosition.Y / tileHeight);

                Console.WriteLine("Selected Tile: (" + selectedTileX + ", " + selectedTileY + ")");

                HandleTileSelection(selectedTileX, selectedTileY);
            }

            Raylib.BeginDrawing();
            Raylib.ClearBackground(Raylib_cs.Color.Gray);

            this.DrawTiles();
            this.DrawPieces();
            this.DrawDice(new Vector2(200, 260));

            Raylib.EndDrawing();
        }

        Raylib.CloseWindow();
    }

    private void DrawTiles()
    {
        Raylib_cs.Color c1 = Raylib_cs.Color.Red;
        Raylib_cs.Color c2 = Raylib_cs.Color.White;

        Raylib_cs.Color currentColor = c2;

        for (int i = 0; i < 12; i++)
        {
            Raylib.DrawTriangle(new Vector2(i * tileWidth, 0),
                                new Vector2(i * tileWidth + tileWidth / 2, tileHeight),
                                new Vector2(i * tileWidth + tileWidth, 0),
                                currentColor);
            currentColor = currentColor.Equals(c1) ? c2 : c1;
        }
        currentColor = currentColor.Equals(c1) ? c2 : c1;
        for (int i = 0; i < 12; i++)
        {
            Raylib.DrawTriangle(new Vector2(i * tileWidth + tileWidth / 2, tileHeight + 30),
                                new Vector2(i * tileWidth, 2 * tileHeight + 30),
                                new Vector2(i * tileWidth + tileWidth, tileHeight * 2 + 30),
                                currentColor);
            currentColor = currentColor.Equals(c1) ? c2 : c1;
        }

        if (selectedTileX != -1 && selectedTileY != -1)
        {
            Raylib.DrawRectangleLines(selectedTileX * tileWidth, selectedTileY * tileHeight + 15, tileWidth, tileHeight, Raylib_cs.Color.Red);
        }

    }

    private void DrawPieces()
    {
        List<Piece>[] state = board.GetBoardState();
        Raylib_cs.Color currentColor;

        for (int j = state.Length / 2 - 1; j >= 0; j--)
        {
            for (int i = 0; i < state[j].Count; i++)
            {
                currentColor = state[j].First().GetColor() == Color.white ? Raylib_cs.Color.White : Raylib_cs.Color.Black;
                Raylib.DrawCircleLines((state.Length / 2 - j) * tileWidth - (tileWidth / 2), pieceRadius * 2 * i + pieceRadius, pieceRadius + 1, Raylib_cs.Color.Black);
                Raylib.DrawCircle((state.Length / 2 - j) * tileWidth - (tileWidth / 2), pieceRadius * 2 * i + pieceRadius, pieceRadius, currentColor);
            }
        }

        for (int j = 13; j < state.Length; j++)
        {
            for (int i = 0; i < state[j].Count; i++)
            {
                currentColor = state[j].First().GetColor() == Color.white ? Raylib_cs.Color.White : Raylib_cs.Color.Black;
                Raylib.DrawCircleLines((j - 12) * tileWidth - (tileWidth / 2), 2 * tileHeight - i * pieceRadius * 2, pieceRadius + 1, Raylib_cs.Color.Black);
                Raylib.DrawCircle((j - 12) * tileWidth - (tileWidth / 2), 2 * tileHeight - i * pieceRadius * 2, pieceRadius, currentColor);
            }
        }
    }

    public void DrawDice(Vector2 position)
    {
        int diceSize = 30;

        Raylib.DrawRectangleRec(new Rectangle(position.X, position.Y, diceSize, diceSize), Raylib_cs.Color.White);
        Raylib.DrawText(dice.d1.Value.ToString(), (int)(position.X + diceSize * 0.4), (int)(position.Y + diceSize * 0.4), 20, Raylib_cs.Color.Black);

        Raylib.DrawRectangleRec(new Rectangle(position.X + diceSize + 10, position.Y, diceSize, diceSize), Raylib_cs.Color.White);
        Raylib.DrawText(dice.d2.Value.ToString(), (int)(position.X + diceSize * 1.4 + 10), (int)(position.Y + diceSize * 0.4), 20, Raylib_cs.Color.Black);
    }

    private void HandleTileSelection(int selectedTileX, int selectedTileY)
    {
        int index = -1;

        if (selectedTileY == 0)
        {
            index = selectedTileX + 1;
        }
        else if (selectedTileY == 1)
        {
            index = 13 + (11 - selectedTileX) + 1;
        }

        if (index != -1)
        {
            Console.WriteLine("Selected Tile Index: " + index);
        }

        this.selectedTileX = selectedTileX;
        this.selectedTileY = selectedTileY;
    }

}