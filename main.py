# imports:

import curses
from gen_mines import gen_mines


# main class

class MineWalker:
    def __init__(self, stdscr, width=10, height=10):
        self.stdscr = stdscr
        self.x, self.y = 0, 0
        self.board = gen_mines(width, height)
        self.game = True
        self.discovered = set()
        self.died = False

    @classmethod
    def start(cls, stdscr, width=10, height=10):
        clas = cls(stdscr, width, height)

        while clas.game:
            clas.draw()
            clas.get_input()
        if clas.died:
            clas.draw()
            clas.stdscr.addstr("Game Over! Press any key to exit.")
            clas.stdscr.getch()

    def draw(self):
        self.stdscr.clear()

        
        self.draw_board=[]
        for y in range(len(self.board)):
            self.draw_board.append([])
            for x in range(len(self.board[0])):
                if self.board[y][x] == 3:
                    self.draw_board[y].append("X")
                elif (x, y) in self.discovered:
                    self.draw_board[y].append(" ")
                else:
                    self.draw_board[y].append("O")
            
             
        
        for row in self.draw_board:
            self.stdscr.addstr(" ".join(row) + "\n")
        
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
            case " " | "\n":
                self.game = False


        self.x = max(0, min(self.x, len(self.board[0])-1))
        self.y = max(0, min(self.y, len(self.board)-1))

        if self.board[self.y][self.x] == 1:
            self.died = True
            self.game = False
            return
        
        self.board[self.y][self.x] = 3
        self.discovered.add((self.x, self.y))

        

def main(stdscr):
    MineWalker.start(stdscr, width=10, height=10)




curses.wrapper(main) 