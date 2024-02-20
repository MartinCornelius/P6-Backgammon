using Backgammon;

namespace tests;

public class DiceTest
{
    [Fact]
    public void Dice_RollOneDice_ReturnIntInRangeOneToSix()
    {
        // Arrange
        Dice dice = new Dice();
        int expectedMin = 1;
        int expectedMax = 6;

        // Act
        dice.Roll();
        int result = dice.value;

        // Assert
        Assert.InRange<int>(result, expectedMin, expectedMax);
    }
}