using Backgammon;

namespace tests;

public class DicePairTest
{
    [Fact]
    public void DicePair_RollPair_ReturnTwoIntegersInRangeOneToSix()
    {
        // Arrange
        DicePair dicePair = new DicePair();
        List<int> expectedCounts = new List<int>() { 2, 4 };

        // Act
        dicePair.Roll();
        List<int> result = new List<int>() { dicePair.d1.value, dicePair.d2.value };

        // Assert
        Assert.Contains(result.Count, expectedCounts);
    }

    [Fact]
    public void DicePair_IsDoubleDice_ReturnsTrueOnDouble()
    {
        // Arrange
        DicePair dicePair = new DicePair();
        dicePair.d1.value = 2;
        dicePair.d2.value = 2;

        // Act
        Boolean result = dicePair.IsDoubleDice();

        // Assert
        Assert.True(result);
    }


}