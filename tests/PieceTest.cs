using Backgammon;

namespace tests;

public class PieceTest
{
    [Theory]
    [InlineData(Color.white)]
    [InlineData(Color.black)]
    public void Piece_GetColor_ReturnsCorrectColor(Color color)
    {
        // Arrange
        Color expectedColor = color;
        Piece piece = new Piece(expectedColor);

        // Act
        Color actual = piece.GetColor();

        // Assert
        Assert.Equal(expectedColor, actual);
    }
}