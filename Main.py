import curses
from MineWalker import MineWalker

if __name__ == "__main__":
    width, height = 10, 10

    curses.wrapper(MineWalker.run, width, height)
    