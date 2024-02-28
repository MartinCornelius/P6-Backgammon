namespace Backgammon;

public static class Helper
{
    public static void SetTextColor(ConsoleColor color)
    {
        Console.ForegroundColor = color;
    }

    public static void SetBackgroundColor(ConsoleColor color)
    {
        Console.BackgroundColor = color;
    }

    public static void ResetColor()
    {
        Console.ForegroundColor = ConsoleColor.White;
        Console.BackgroundColor = ConsoleColor.Black;
    }

    public static void WriteToCenter(string content)
    {
        Console.SetCursorPosition((Console.BufferWidth / 2) - (content.Length / 2), Console.CursorTop);
        Console.WriteLine($"{content}");
    }
}