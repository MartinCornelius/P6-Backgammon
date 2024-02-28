namespace Backgammon;

public class MainMenu
{
    public string Title { get; set; }

    private bool _running = true;
    private int _selectedIndex = 0;
    private List<MenuItem> _menuItems = new List<MenuItem>();

    public MainMenu(string title)
    {
        this.Title = title;
    }

    public void Add(MenuItem menuItem)
    {
        _menuItems.Add(menuItem);
    }

    public virtual void Start()
    {
        _running = true;
        if (_menuItems.ElementAt(0) != null)
            _menuItems.ElementAt(0).Highlighted = true;

        do
        {
            DrawMenu();
            HandleInput();
        } while (_running);
    }

    public virtual void DrawMenu()
    {
        Console.Clear();
        PrintTitle();

        foreach (MenuItem menuItem in _menuItems)
        {
            Helper.ResetColor();

            if (menuItem.Highlighted)
                Helper.SetBackgroundColor(ConsoleColor.Green);

            Helper.WriteToCenter(menuItem.Title);
        }
    }

    public void PrintTitle()
    {
        Helper.SetTextColor(ConsoleColor.Cyan);
        Helper.WriteToCenter(this.Title + "\n");
    }

    public void HandleInput()
    {
        Helper.ResetColor();
        ConsoleKeyInfo cki = Console.ReadKey();

        switch (cki.Key)
        {
            case ConsoleKey.Backspace:
            case ConsoleKey.Q:
            case ConsoleKey.Escape:
                _running = false;
                break;
            case ConsoleKey.K:
            case ConsoleKey.UpArrow:
                MoveUp();
                break;
            case ConsoleKey.J:
            case ConsoleKey.DownArrow:
                MoveDown();
                break;
            case ConsoleKey.Spacebar:
            case ConsoleKey.Enter:
                _menuItems.ElementAt(_selectedIndex).Select();
                break;
            default:
                break;
        }
    }

    public void MoveUp()
    {
        _menuItems.ElementAt(_selectedIndex).Highlighted = false;
        _selectedIndex--;
        if (_selectedIndex < 0)
            _selectedIndex = 0;
        _menuItems.ElementAt(_selectedIndex).Highlighted = true;
    }

    public void MoveDown()
    {
        _menuItems.ElementAt(_selectedIndex).Highlighted = false;
        _selectedIndex++;
        if (_selectedIndex > _menuItems.Count - 1)
            _selectedIndex = _menuItems.Count - 1;
        _menuItems.ElementAt(_selectedIndex).Highlighted = true;
    }
}