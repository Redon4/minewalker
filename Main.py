import curses
from MineWalker import MineWalker

if __name__ == "__main__":
    width, height = 20, 20
    density = 0.1

    curses.wrapper(MineWalker.run, width, height, density)