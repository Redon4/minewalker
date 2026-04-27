from minewalker import MineWalker as mine
from score import save_score, load_score
from time import sleep


def singleplayer(stdscr, width=10, height=10, density=0.2, **kwargs):
    stdscr.nodelay(kwargs.get("timed", False)) # make it not stop when on timed mode
    mine.easy_mode = kwargs.get("easy_mode", False)
    while True:
        clas = mine(stdscr, width, height, density)

        while clas.game:
            clas.board[clas.y][clas.x] = 3
            clas.draw()

            # next part is because i am lazy in the most complicated way possible
            # I didnt want to write the attr twice
            to_change = ["x", "y", "discovered", "mark", "marked"]
            new = clas.get_input(*(getattr(clas, name) for name in to_change)) # * does unpacking, goes through every attr
            # /|\ these are the new values
            for attr, new_val in zip(to_change, new): # zip fused two lists
                setattr(clas, attr, new_val)

            sleep(0.001)

        msg = "You won! " if clas.won else ("You quit! " if not clas.died else "Game Over! ")
        clas.draw()
        clas.stdscr.move(len(clas.board) + 2, 0)
        clas.stdscr.addstr(f"{msg}Press \"q\" to exit, space or enter to play again.")
        save_score(max(clas.highscore, len(clas.discovered) - 1)) # save the highscore
        while True:
            try:
                key = clas.stdscr.getkey()
            except:
                sleep(0.01)
                continue
            if key in ("\n", " "): # enter
                break # restart
            elif key == "q": # space
                return # quit
