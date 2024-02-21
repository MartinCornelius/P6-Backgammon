using Backgammon;

namespace tests;

public class PlayerTest
{
    [Fact]
    public void Player_Constructor_ValidInitialization()
    {
        // Arrange
        string expectedName = "Dan";
        Color expectedColor = Color.white;
        int expectedScore = 0;
        bool expectedIsAllHome = false;

        // Act
        Player result = new Player(expectedName, expectedColor);

        // Assert
        Assert.Equal(expectedName, result.Name);
        Assert.Equal(expectedColor, result.Color);
        Assert.Equal(expectedScore, result.Score);
        Assert.Equal(expectedIsAllHome, result.IsAllHome);
    }
}