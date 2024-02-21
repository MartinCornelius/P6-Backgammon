using Backgammon;

namespace tests;

public class BoardTest
{
    [Fact]
    public void Board_InitBoard_ReturnsStateArrayWithCorrectStartConfig()
    {
        // Arrange
        Board board = new Board();
        Board expectedBoard = new Board();

        List<Tuple<int, int, string>> boardList = new List<Tuple<int, int, string>>()
        {
            new (1, 2, "Black"),
            new (6, 5, "White"),
            new (8, 3, "White"),
            new (12, 5, "Black"),
            new (13, 5, "White"),
            new (17, 3, "Black"),
            new (19, 5, "Black"),
            new (24, 2, "White")
        };

        expectedBoard.InitBoard(boardList);
        List<Piece>[] expectedResult = expectedBoard.GetBoardState();

        // Act
        board.InitBoard();
        List<Piece>[] result = board.GetBoardState();

        // Assert
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
}