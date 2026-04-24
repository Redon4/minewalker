import curses
from Singleplayer import MineWalker

if __name__ == "__main__":
    width, height = 20, 20
    density = 0.2

    curses.wrapper(MineWalker.run, width, height, density, timed=True, easy_mode=True)