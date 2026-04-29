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


        self.max_score_len = len(str(len(self.board) * len(self.board[0])))

        # self.center = center




    def move_x(self, x):
        y1, x1 = self.stdscr.getmaxyx()
        self.stdscr.move(y1, x)


    def draw(self, rem_time=-1):
        self.stdscr.erase()

        if self.center:
            board_height = len(self.board)
            ABOVE_HEIGHT = 4
            total_height = board_height + ABOVE_HEIGHT

            y = (self.stdscr.getmaxyx()[0] - total_height) // 2
            x = (self.stdscr.getmaxyx()[1] - len(self.board[0]) * 2) // 2
        else:
            y = 0
            x = 0

        self.stdscr.addstr(y, x, f"Score: {len(self.discovered) - 1:{self.max_score_len}d}")
        # self.stdscr.addstr("\t| WASD or arrows: move; space, enter, \"q\": exit. \"m\" or \"e\" + direction to mark/unmark a cell.")
        y += 1



        around_area = self.board[max(0, self.y-1):min(self.y+2, len(self.board))]
        around_cnt=0
        for row in around_area:
            around_cnt += row[max(0, self.x-1):min(self.x+2, len(row))].count(1)


        self.stdscr.addstr(y, x, f"Mines around: {around_cnt}", self.p.color("green") if around_cnt == 0 else self.p.color("red"))
        # self.stdscr.addstr("\t| ")

        if rem_time != -1:
            msg = f"Time: {f"{rem_time:>{self.time_length}.1f}s":5s}"
            # if self.center:
            board_center = len(self.board[0]) #// 2 # comment because it would be * 2 // 2
            text_pos = x + board_center - len(msg) // 2
            self.stdscr.addstr(y, text_pos, msg)
            # else:
            #     self.stdscr.addstr(msg)


        msg = f"Highscore: {self.highscore if self.highscore > len(self.discovered) - 1 else len(self.discovered) - 1:{self.max_score_len}d}" + (" NEW HIGHSCORE!" if len(self.discovered) - 1 > self.highscore else "")
        self.stdscr.addstr(y, x + len(self.board[0]) * 2 - len(msg) - 1, msg, self.p.color("yellow"))

        y += 1
        
        for y1 in range(len(self.board)):
            self.stdscr.move(y, x)
            for x1 in range(len(self.board[0])):
                if (x1, y1) == (self.x, self.y) and not self.died:
                    self.stdscr.addstr("X", self.p.color("green")) # show the player
                    self.stdscr.addstr(" ")


                elif (x1, y1) in self.discovered:
                    # self.draw_board[y].append(" ")
                    self.stdscr.addstr("  ")

                elif not self.game and self.board[y1][x1] == 1: # if you died, show all mines
                    # self.draw_board[y].append("*")
                    if (x1, y1) == (self.x, self.y):
                        self.stdscr.addstr("X", self.p.color("red", rev=True))
                        self.stdscr.addstr(" ")
                    else:
                        self.stdscr.addstr("* ", self.p.color("red"))

                elif (x1, y1) in self.marked: # marked
                    self.stdscr.addstr("O ", self.p.color("red"))


                else:
                    # self.draw_board[y].append("O")
                    self.stdscr.addstr("O ")
            y += 1

        # self.stdscr.move(2, 0)
        # self.stdscr.move(self.y+1+1, self.x*2)


        self.stdscr.refresh()


    def get_input(self, x, y, discovered, mark, marked):

        if not mark: # normal movment
            try:
                inp = self.stdscr.get_wch()
            except:
                inp = None
            self.board[y][x] = 0

            move=[0, 0] # y, x
            match inp:
                case "w" | curses.KEY_UP | "8":
                    move[0] = -1
                case "s" | curses.KEY_DOWN | "2":
                    move[0] = 1
                case "a" | curses.KEY_LEFT | "4":
                    move[1] = -1
                case "d" | curses.KEY_RIGHT | "6":
                    move[1] = 1
                case "m" | "-" | "e" | "f" | "5": # mark
                    mark = True
                case " " | "\n" | "q" : # quit
                    self.game = False

            if inp:# self.x = max(0, min(self.x, len(self.board[0])-1))
                # self.y = max(0, min(self.y, len(self.board)-1))
                if (x + move[1], y + move[0]) in marked and self.easy_mode: # dont move into makred cells on easy mode
                    pass

                else:
                    x, y = utils.clamp_to_matrix(x + move[1], y + move[0], self.board)

                    if self.board[y][x] == 1: # if youre in a mine
                        self.died = True
                        self.game = False
                        #return
                    else: # if youre not dead
                        discovered.add((x, y))


        else: # marking
            try:
                inp2 = self.stdscr.get_wch()
            except:
                inp2 = None
            offset=[0, 0]
            match inp2:
                # straight
                case "w" | curses.KEY_UP | "8":
                    offset[0] = -1
                case "s" | curses.KEY_DOWN | "2":
                    offset[0] = 1
                case "a" | curses.KEY_LEFT | "4":
                    offset[1] = -1
                case "d" | curses.KEY_RIGHT | "6":
                    offset[1] = 1
                #diagonal
                case "e" | "9":
                    offset = [-1, 1]
                case "q" | "7":
                    offset = [-1, -1]
                case "c" | "3":
                    offset = [1, 1]
                case "y" | "z" | "1" | "<":
                    offset = [1, -1]

            if inp2:
                mark = False
                x1, y1 = utils.clamp_to_matrix(x + offset[1], y + offset[0], self.board)
                if (x1, y1) not in discovered:
                    if (x1, y1) in marked:
                        marked.remove((x1, y1))
                    else:
                        marked.add((x1, y1))

        return x, y, discovered, mark, marked
