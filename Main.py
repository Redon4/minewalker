import curses
import game_modes as game


if __name__ == "__main__":
    width, height = 20, 20
    density = 0.26

    curses.wrapper(game.singleplayer, width, height, density, playtime=40, easy_mode=True)
