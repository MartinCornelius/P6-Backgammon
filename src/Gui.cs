using System.Data;
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

    private Board board;

    public Gui()
    {
        this.board = new Board();
        this.board.InitBoard();
        this.Run();
    }

    public void Run()
    {
        Raylib.InitWindow(WIDTH, HEIGHT, "P6 - Backgammon");
        Raylib.SetTargetFPS(10);

        while (!Raylib.WindowShouldClose())
        {
            Raylib.BeginDrawing();
            Raylib.ClearBackground(Raylib_cs.Color.Gray);

            this.DrawTiles();
            this.DrawPieces();

            Raylib.EndDrawing();
        }

        Raylib.CloseWindow();
    }

    private void DrawTiles()
    {
        Raylib_cs.Color currentColor = Raylib_cs.Color.Red;

        for (int i = 0; i < 12; i++)
        {
            Raylib.DrawTriangle(new Vector2(i * tileWidth, 0),
                                new Vector2(i * tileWidth + tileWidth / 2, tileHeight),
                                new Vector2(i * tileWidth + tileWidth, 0),
                                currentColor);
            currentColor = currentColor.Equals(Raylib_cs.Color.Red) ? Raylib_cs.Color.SkyBlue : Raylib_cs.Color.Red;
        }
        currentColor = currentColor.Equals(Raylib_cs.Color.Red) ? Raylib_cs.Color.SkyBlue : Raylib_cs.Color.Red;
        for (int i = 0; i < 12; i++)
        {
            Raylib.DrawTriangle(new Vector2(i * tileWidth + tileWidth / 2, tileHeight + 30),
                                new Vector2(i * tileWidth, 2 * tileHeight + 30),
                                new Vector2(i * tileWidth + tileWidth, tileHeight * 2 + 30),
                                currentColor);
            currentColor = currentColor.Equals(Raylib_cs.Color.Red) ? Raylib_cs.Color.SkyBlue : Raylib_cs.Color.Red;
        }
    }

    private void DrawPieces()
    {
        List<Piece>[] state = board.GetBoardState();
        int counter = 0;
        for (int j = 0; j < state.Length / 2; j++)
        {
            for (int i = 0; i < state[j].Count; i++)
            {
                Raylib.DrawCircle(j * tileWidth + (tileWidth / 2), (pieceRadius * 2) * i + pieceRadius, pieceRadius, Raylib_cs.Color.Beige);
                counter++;
            }
        }
        Console.WriteLine("drawing " + counter);
    }
}