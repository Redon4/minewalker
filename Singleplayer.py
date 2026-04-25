# imports:

import curses
from gen_mines import gen_mines, clear_path
from perry import Perry
from score import save_score, load_score
import utils


# main class

class MineWalker:
    def __init__(self, stdscr, width=10, height=10, density=0.2):
        self.p = Perry(stdscr)
        self.stdscr = stdscr
        self.x, self.y = 0, 0
        self.board = clear_path(gen_mines(width, height, density))
        self.game = True
        self.discovered = {(0, 0)}
        self.died = False
        self.won = False

        self.marked = set()
        self.mark = False

        self.highscore = load_score()

        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)

    @classmethod
    def run(cls, stdscr, width=10, height=10, density=0.2, **kwargs):
        if kwargs.get("timed", False):
            stdscr.nodelay(True)
        cls.easy_mode = kwargs.get("easy_mode", False)
        while True:
            clas = cls(stdscr, width, height, density)

            while clas.game:
                clas.board[clas.y][clas.x] = 3
                clas.draw()
                clas.get_input()
            msg = "You won! " if clas.won else ("You quit! " if not clas.died else "Game Over! ")
            clas.draw()
            clas.stdscr.move(len(clas.board)+2, 0)
            clas.stdscr.addstr(f"{msg}Press \"q\" to exit, space or enter to play again.")
            while True:
                try:
                    key = clas.stdscr.getkey()
                except:
                    continue
                if key in ("\n", " "): # enter
                    break # restart
                elif key == "q": # space
                    return # quit
            save_score(max(clas.highscore, len(clas.discovered) - 1)) # save the highscore


    def draw(self):
        self.stdscr.erase()

        self.stdscr.addstr(f"Score: {len(self.discovered) - 1}")
        self.stdscr.addstr("\t| WASD or arrow keys to move; space, enter or \"q\" to exit. \"m\" or \"e\" + direction to mark/unmark a cell." + "\n")


        around_area = self.board[max(0, self.y-1):min(self.y+2, len(self.board))]
        around_cnt=0
        for row in around_area:
            around_cnt += row[max(0, self.x-1):min(self.x+2, len(row))].count(1)


        self.stdscr.addstr(f"Mines around: {around_cnt}", self.p.color("green") if around_cnt == 0 else self.p.color("red"))
        self.stdscr.addstr("\t| ")

        self.stdscr.addstr(f"Highscore: {self.highscore}" + "\n", self.p.color("yellow"))

        # self.draw_board=[]
        for y in range(len(self.board)):
            # self.draw_board.append([])
            for x in range(len(self.board[0])):
                if (x, y) == (self.x, self.y) and not self.died:
                    self.stdscr.addstr("X", self.p.color("green")) # show the player
                    self.stdscr.addstr(" ")


                elif (x, y) in self.discovered:
                    # self.draw_board[y].append(" ")
                    self.stdscr.addstr("  ")

                elif not self.game and self.board[y][x] == 1: # if you died, show all mines
                    # self.draw_board[y].append("*")
                    if (x, y) == (self.x, self.y):
                        self.stdscr.addstr("X", self.p.color("red", rev=True))
                        self.stdscr.addstr(" ")
                    else:
                        self.stdscr.addstr("* ", self.p.color("red"))

                elif (x, y) in self.marked: # marked
                    self.stdscr.addstr("O ", self.p.color("red"))


                else:
                    # self.draw_board[y].append("O")
                    self.stdscr.addstr("O ")
            self.stdscr.addstr("\n")

        # self.stdscr.move(2, 0)
        # self.stdscr.move(self.y+1+1, self.x*2)


        self.stdscr.refresh()


    def get_input(self):

        if not self.mark:
            try:
                inp = self.stdscr.get_wch()
            except:
                inp = None
            self.board[self.y][self.x] = 0

            move=[0, 0] # y, x
            match inp:
                case "w" | curses.KEY_UP:
                    move[0] = -1
                case "s" | curses.KEY_DOWN:
                    move[0] = 1
                case "a" | curses.KEY_LEFT:
                    move[1] = -1
                case "d" | curses.KEY_RIGHT:
                    move[1] = 1
                case "m" | "-" | "e" | "f": # mark
                    self.mark = True
                case " " | "\n" | "q" : # quit
                    self.game = False
                
            if inp:# self.x = max(0, min(self.x, len(self.board[0])-1))
                # self.y = max(0, min(self.y, len(self.board)-1))
                if (self.x + move[1], self.y + move[0]) in self.marked and self.easy_mode: # dont move into makred cells on easy mode
                    return
                self.x, self.y = utils.clamp_to_matrix(self.x + move[1], self.y + move[0], self.board)

                if self.board[self.y][self.x] == 1: # if youre in a mine
                    self.died = True
                    self.game = False
                    return

                self.discovered.add((self.x, self.y))


        else:
            try:
                inp2 = self.stdscr.get_wch()
            except:
                inp2 = None
            offset=[0, 0]
            match inp2:
                # straight
                case "w" | curses.KEY_UP:
                    offset[0] = -1
                case "s" | curses.KEY_DOWN:
                    offset[0] = 1
                case "a" | curses.KEY_LEFT:
                    offset[1] = -1
                case "d" | curses.KEY_RIGHT:
                    offset[1] = 1
                #diagonal
                case "e":
                    offset = [-1, 1]
                case "q":
                    offset = [-1, -1]
                case "c":
                    offset = [1, 1]
                case "y" | "z":
                    offset = [1, -1]
            
            if inp2:
                self.mark = False
                x, y = utils.clamp_to_matrix(self.x + offset[1], self.y + offset[0], self.board)
                if (x, y) not in self.discovered:
                    if (x, y) in self.marked:
                        self.marked.remove((x, y))
                    else:
                        self.marked.add((x, y))

        