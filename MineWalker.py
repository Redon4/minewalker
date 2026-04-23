# imports:

import curses
from gen_mines import gen_mines
from perry import Perry


# main class

class MineWalker:
    def __init__(self, stdscr, width=10, height=10, density=0.2):
        self.p = Perry(stdscr)
        self.stdscr = stdscr
        self.x, self.y = 0, 0
        self.board = gen_mines(width, height, density)
        self.game = True
        self.discovered = {(0, 0)}
        self.died = False
        self.won = False

        curses.start_color()
        curses.use_default_colors()

    @classmethod # damit man keine instance machen muss
    def run(cls, stdscr, width=10, height=10, density=0.2):
        while True:
            clas = cls(stdscr, width, height, density)

            while clas.game:
                clas.board[clas.y][clas.x] = 3
                clas.draw()
                clas.get_input()
            msg = "You won! " if clas.won else "You quit! "
            if clas.died:
                clas.draw()
                msg = "Game Over! "
            clas.stdscr.move(len(clas.board)+2, 0)
            clas.stdscr.addstr(f"{msg}Press enter to exit or space to play again.")
            while True:
                key = clas.stdscr.getkey()
                if key == "\n": # enter
                    return # beende
                elif key == " ": # space
                    break # starte neu


    def draw(self):
        self.stdscr.erase()

        self.stdscr.addstr("Use WASD or arrow keys to move, space or enter to quit." + "\n")


        around_area = self.board[max(0, self.y-1):min(self.y+2, len(self.board))]
        around_cnt=0
        for row in around_area:
            around_cnt += row[max(0, self.x-1):min(self.x+2, len(row))].count(1)


        self.stdscr.addstr(f"Mines around: {around_cnt}" + "\n")


        # self.draw_board=[]
        for y in range(len(self.board)):
            # self.draw_board.append([])
            for x in range(len(self.board[0])):
                if (x, y) == (self.x, self.y):
                    self.stdscr.addstr("X ", self.p.color(-1)) # zeige den Spieler an


                elif (x, y) in self.discovered:
                    # self.draw_board[y].append(" ")
                    self.stdscr.addstr("  ")

                elif self.died and self.board[y][x] == 1: # wenn du durch eine Mine gestorben bist, zeige alle Minen an
                    # self.draw_board[y].append("*")
                    self.stdscr.addstr("* ", self.p.color("red"))

                else:
                    # self.draw_board[y].append("O")
                    self.stdscr.addstr("O ")
            self.stdscr.addstr("\n")

        self.stdscr.move(2, 0)
        #self.stdscr.addstr("-" * (len(self.board[0])*2-1) + "\n") # trennlinie
        #for row in self.draw_board:
        #    self.stdscr.addstr(" ".join(row) + "\n")
        #self.stdscr.addstr("-" * (len(self.board[0])*2-1) + "\n") # trennlinie

        #self.stdscr.move(self.y+1+1, self.x*2)
        #self.stdscr.addstr("X", self.p.color("green")) # zeige den Spieler an
        self.stdscr.move(self.y+1+1, self.x*2)

        self.stdscr.refresh()


    def get_input(self):
        inp = self.stdscr.get_wch()
        self.board[self.y][self.x] = 0

        match inp:
            case "w" | curses.KEY_UP:
                self.y -= 1
            case "s" | curses.KEY_DOWN:
                self.y += 1
            case "a" | curses.KEY_LEFT:
                self.x -= 1
            case "d" | curses.KEY_RIGHT:
                self.x += 1
            case " " | "\n": # beende das spiel
                self.game = False


        self.x = max(0, min(self.x, len(self.board[0])-1))
        self.y = max(0, min(self.y, len(self.board)-1))

        if self.board[self.y][self.x] == 1: # wenn du in einer Mine bist
            self.died = True
            self.game = False
            return

        self.board[self.y][self.x] = 3 # akutuelle position = spieler
        self.discovered.add((self.x, self.y)) # du warst hier, es ist ein set
