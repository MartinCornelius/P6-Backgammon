namespace Backgammon;

public class MenuItem : MainMenu
{
    public bool Highlighted { get; set; } = false;
    private Board _board;

    public MenuItem(string title, Board b = null) : base(title)
    {
        this.Title = title;
        this._board = b;
    }

    public virtual void Select()
    {
        Console.Clear();
        Helper.WriteToCenter(this.Title);

        this._board.Print(); // Change this

        Console.WriteLine("Press any key to go back to menu...");
        Console.ReadKey();
    }
}