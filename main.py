import curses
from menu import Menu


if __name__ == "__main__":
    width, height = 20, 20
    density = 25

    curses.wrapper(Menu.run)