# imports:

import curses

# main class

class MineWalker:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.x, self.y = 0, 0
        self.board = []

    @classmethod
    def start(cls):
        clas = cls()
        # will start the game
        pass


    def get_input(self):
        inp = self.stdscr.get_wch()
        
        match inp:
            case "w" | curses.KEY_UP:
                self.y -= 1
            case "s" | curses.KEY_DOWN:
                self.y += 1
            case "a" | curses.KEY_LEFT:
                self.x -= 1
            case "d" | curses.KEY_RIGHT:
                self.x += 1


        self.x = max(0, min(self.x, len(self.board)))

def main(stdscr):
    MineWalker.start(stdscr)




curses.wrap(main) 