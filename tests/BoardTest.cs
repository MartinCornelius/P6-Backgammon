using Backgammon;
using Microsoft.VisualStudio.TestPlatform.Utilities;
using Xunit.Abstractions;

namespace tests;

public class BoardTest
{
    private readonly ITestOutputHelper output;

    public BoardTest(ITestOutputHelper output)
    {
        this.output = output;
    }



    [Fact]
    public void Board_InitBoard_ReturnsStateArrayWithCorrectStartConfig()
    {
        // Arrange
        Board board = new Board();
        Board expectedBoard = new Board();

        List<Tuple<int, int, Color>> boardList = new List<Tuple<int, int, Color>>()
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

        expectedBoard.InitBoard(boardList);
        List<Piece>[] expectedResult = expectedBoard.GetBoardState();

        // Act
        board.InitBoard();
        List<Piece>[] result = board.GetBoardState();


        Assert.Equivalent(result, expectedResult);

    }

    [Fact]
    public void Board_GetBoardState_ReturnsArrayWith26Tiles()
    {
        // Arrange
        Board board = new Board();
        int expected_length = 26;

        // Act
        List<Piece>[] fullBoard = board.GetBoardState();

        // Assert
        Assert.Equal(fullBoard.Length, expected_length);
    }


    [Fact]
    public void Board_PieceMove_ReturnsPieceAtCorrectlyUpdatedPosition()
    {
        // Arrange
        Dice dice = new Dice();
        dice.value = 1;

        Board board = new Board();
        Board expectedBoard = new Board();

        // Act
        board.InitBoard(new List<Tuple<int, int, Color>>()
            {
            new (1, 1, Color.white)
            });

        List<Piece>[] result = board.GetBoardState();

        output.WriteLine("This is output from \n{0}", result[1][0].GetColor());

        board.UpdatePiecePosition(1, 1);
        
        output.WriteLine("This is output from \n{0}", result[0][0].GetColor());
        

        // Assert
        Assert.IsType<Piece>(result[0][0]);
        


    }
    [Fact]
    
}