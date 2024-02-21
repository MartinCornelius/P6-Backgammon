using Backgammon;

namespace tests;

public class PieceTest
{
    [Fact]
    public void Piece_GetColor_ReturnsCorrectColor()
    {
        // Arrange
        string expectedWhite = "white";
        string expectedBlack = "black";

        // Act
        Piece piece = new Piece("white");
        Piece piece2 = new Piece("black");

        // Assert
        string actual = piece.GetColor();
        string actual2 = piece2.GetColor();
        Assert.Equal(expectedWhite, actual);
        Assert.Equal(expectedBlack, actual2);
    }
}