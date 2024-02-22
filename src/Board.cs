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

    public bool UpdatePiecePosition(int piecePosition, int roll, Player currentPlayer)
    {
        int dir = currentPlayer.Color == Color.white?-1:1;
        int targetPosition = piecePosition+roll*dir;

        bool isInsideBoard = IsInsideBoard(targetPosition, currentPlayer);
        TileAvailability availableTile = CheckedDst(targetPosition, currentPlayer);

        if(availableTile == TileAvailability.blocked)
            return false;
        if(isInsideBoard == false)
            return false;
        //if(availableTile == TileAvailability.onePiece)
            //HitHome(targetposition, currentPlayer)
        PieceMove(piecePosition, targetPosition, currentPlayer);
        return true;
    }

    private bool IsInsideBoard(int targetPosition, Player currentPlayer)
    {
        return true;
    }
    
    private TileAvailability CheckedDst(int targetPosition, Player currentPlayer)
    {

        List<Piece> destination = this.state[targetPosition];

        if(destination.Count == 0)
            return TileAvailability.free;
        else if(destination.Count == 1 && destination[0].GetColor() != currentPlayer.Color)
            return TileAvailability.onePiece;
        else if(destination.Count > 1 && destination[0].GetColor() != currentPlayer.Color)
            return TileAvailability.blocked;
        else
            return TileAvailability.free;
    }
    private void PieceMove(int piecePosition, int targetPosition, Player currentPlayer)
    {
        this.state[piecePosition].RemoveAt(0);
        this.state[targetPosition].Add(new Piece(currentPlayer.Color));
    }
        

    // public bool IsAllHome()
}