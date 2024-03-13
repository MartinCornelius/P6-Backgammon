using System.ComponentModel.DataAnnotations;

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
        this.InitBoard();
    }

    public List<Piece>[] GetBoardState()
    {
        List<Piece>[] output = (List<Piece>[])state.Clone();
        return output;
    }
    public void InitBoard()
    {
        List<Tuple<int, int, Color>> defaultList = new List<Tuple<int, int, Color>>()
        {
            new (1, 2, Color.black),
            new (6, 5, Color.white),
            new (8, 3, Color.white),
            new (12, 5, Color.black),
            new (13, 5, Color.white),
            new (17, 3, Color.black),
            new (19, 5, Color.black),
            new (24, 2, Color.white)
        };
        foreach (Tuple<int, int, Color> tuple in defaultList)
        {
            this.fillTile(tuple.Item1, tuple.Item2, tuple.Item3);
        }
    }

    public void InitBoard(List<Tuple<int, int, Color>> configList)
    {
        foreach (Tuple<int, int, Color> tuple in configList)
        {
            this.fillTile(tuple.Item1, tuple.Item2, tuple.Item3);
        }
    }
    private void fillTile(int index, int amount, Color color)
    {
        for (int i = 0; i < amount; i++)
        {
            this.state[index].Add(new Piece(color));
        }
    }

    public bool MovePiece(int piecePosition, int roll, Player currentPlayer)
    {
        int dir = currentPlayer.Color == Color.white ? -1 : 1;
        int targetPosition = piecePosition + roll * dir;

        bool isInsideBoard = IsInsideBoard(targetPosition, currentPlayer);
        bool correctPieceAtPosition = CorrectPieceAtPosition(piecePosition, currentPlayer);

        if (isInsideBoard == false || correctPieceAtPosition == false)
            return false;

        TileAvailability availableTile = CheckedDst(targetPosition, currentPlayer);

        if (availableTile == TileAvailability.blocked)
            return false;
        //if(availableTile == TileAvailability.onePiece)
        //HitHome(targetposition, currentPlayer)
        changePiecePositions(piecePosition, targetPosition, currentPlayer);
        return true;
    }
    // Should change the current players IsAllHome value so it can be used to schmove later
    private void allAreHome(Player currentPlayer)
    {
        if(currentPlayer.Color == Color.black)
        {
            currentPlayer.IsAllHome = true;
        }
    }

    // Checks if there are pieces at the target position and if the piece is the correct color
    private bool CorrectPieceAtPosition(int piecePosition, Player currentPlayer)
    {   
        
        if(piecePosition <= 0 || piecePosition >= 25)
        {
            Console.WriteLine("Target piece is outside of the board");
            return false;
        }
        else if(this.state[piecePosition].Count  == 0){
            Console.WriteLine("No pieces at position: ", piecePosition);
            return false;
        }
        else if(this.state[piecePosition][0].GetColor() != currentPlayer.Color){
            Console.WriteLine("Wrong piece color");
            return false;
        }
           

        return true;
    }

    // Checks if the piece to move will be moved out of the board
    private bool IsInsideBoard(int targetPosition, Player currentPlayer)
    {   
        int lower = 1;
        int higher = 24;
        if(currentPlayer.IsAllHome)
        {
            lower = 0;
            higher = 25;
        }
        if(currentPlayer.Color == Color.white && targetPosition < lower)
        {   
            Console.WriteLine("All pieces are not home yet");
            return false;
        }else if(currentPlayer.Color == Color.black && targetPosition > higher)
        {  
            Console.WriteLine("All pieces are not home yet");
            return false;
        }
        
        
        return true;
    }

    private TileAvailability CheckedDst(int targetPosition, Player currentPlayer)
    {

        List<Piece> destination = this.state[targetPosition];

        if (destination.Count == 0)
            return TileAvailability.free;
        else if (destination.Count == 1 && destination[0].GetColor() != currentPlayer.Color)
            return TileAvailability.onePiece;
        else if (destination.Count > 1 && destination[0].GetColor() != currentPlayer.Color)
            return TileAvailability.blocked;
        else
            return TileAvailability.free;
    }

    private void changePiecePositions(int piecePosition, int targetPosition, Player currentPlayer)
    {
        this.state[piecePosition].RemoveAt(0);
        this.state[targetPosition].Add(new Piece(currentPlayer.Color));
    }

    public void Print()
    {
        Console.WriteLine(" 13 14 15 16 17 18  19 20 21 22 23 24");
        Console.WriteLine("+--+--+--+--+--+--++--+--+--+--+--+--+--+");
        int maxPieces = state.Max(tile => tile.Count);

        // Printing upper part
        for (int row = 0; row < maxPieces; row++)
        {
            for (int tile = 13; tile <= 25; tile++)
            {
                if (tile == 19)
                    Console.Write("||");
                else
                    Console.Write("|");

                List<Piece> pieces = state[tile];
                if (pieces.Count > row)
                {
                    Console.Write(pieces[row].GetColor() == Color.black ? "B" : "W");
                }
                else
                {
                    Console.Write(" ");
                }
                Console.Write(" ");
            }
            Console.WriteLine("|");
        }
        Console.WriteLine("+--+--+--+--+--+--++--+--+--+--+--+--+--+");

        // Printing lower part
        Console.WriteLine("+--+--+--+--+--+--++--+--+--+--+--+--+--+");
        for (int row = maxPieces - 1; row >= 0; row--)
        {
            for (int tile = 12; tile >= 0; tile--)
            {
                if (tile == 6)
                    Console.Write("||");
                else
                    Console.Write("|");

                List<Piece> pieces = state[tile];
                if (pieces.Count > row)
                {
                    Console.Write(pieces[row].GetColor() == Color.black ? "B" : "W");
                }
                else
                {
                    Console.Write(" ");
                }
                Console.Write(" ");
            }
            Console.WriteLine("|");
        }
        Console.WriteLine("+--+--+--+--+--+--++--+--+--+--+--+--+--+");
        Console.WriteLine(" 12 11 10 9  8  7    6  5  4  3  2  1");
    }

    public bool HasWon()
    {
        return false;
    }
}
