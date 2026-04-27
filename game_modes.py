from minewalker import MineWalker as mine
from score import save_score, load_score
import time


def singleplayer(stdscr, width=10, height=10, density=0.2, **kwargs): # defaults: playtime: -1; easy_mode: True
    mine.timed = True if kwargs.get("playtime", -1) != -1 else False
    mine.easy_mode = kwargs.get("easy_mode", False)
    stdscr.nodelay(mine.timed) # make it not stop when on timed mode
    if mine.timed:
        mine.time_length = len(str(int(kwargs.get("playtime", 0))))
    
    while True:
        clas = mine(stdscr, width, height, density)

        if clas.timed:
            start_time = time.time()

        while clas.game:
            if clas.timed:
                rem_time = kwargs["playtime"] - (time.time() - start_time)
                if rem_time <= 0:
                    timeout = True
                    clas.game = False
                    break
                else:
                    timeout = False
            clas.board[clas.y][clas.x] = 3
            clas.draw(rem_time if clas.timed else -1)

            # next part is because i am lazy in the most complicated way possible
            # I didnt want to write the attr twice
            to_change = ["x", "y", "discovered", "mark", "marked"]
            new = clas.get_input(*(getattr(clas, name) for name in to_change)) # * does unpacking, goes through every attr
            # /|\ these are the new values
            for attr, new_val in zip(to_change, new): # zip fused two lists
                setattr(clas, attr, new_val)

            time.sleep(0.001)

        if clas.won:
            msg = "You won! "
        elif clas.died:
            msg = "Game Over! "
        elif clas.timed and timeout:
            msg = "The time is up! "
        else:
            msg = "You quit! "
        clas.draw(rem_time if clas.timed else -1)
        clas.stdscr.move(len(clas.board) + 2, 0)
        clas.stdscr.addstr(f"{msg}Press \"q\" to exit, space or enter to play again.")
        save_score(max(clas.highscore, len(clas.discovered) - 1)) # save the highscore
        while True:
            try:
                key = clas.stdscr.getkey()
            except:
                time.sleep(0.01)
                continue
            if key in ("\n", " "): # enter
                break # restart
            elif key == "q": # space
                return # quit
