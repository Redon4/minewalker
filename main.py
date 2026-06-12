import curses
from menu import Menu


if __name__ == "__main__":
    curses.wrapper(Menu.run)
