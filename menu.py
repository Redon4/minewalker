from utils import *
import curses
from perry import Perry as P
import game_modes as game

class Menu:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.index = [0, 0] # main menu, sub menu


        self.size = [40, 40] # w, h
        self.time_limit = [40, 40] # Single-, Multiplayer
        self.time_active = [False, False]
        self.density = 0.25
        self.easy = True
        

        self.p = P(stdscr)

        curses.use_default_colors()
        curses.curs_set(0)

    @classmethod
    def run(cls, stdscr):
        clas = cls(stdscr)
        while True:
            clas.draw()
            
            clas.get_input()

    def build_list(self):
        self.menu_list = [
        ["Singleplayer", "Time limit", self.time_limit[0]], 
        ["Multiplayer", "Time limit", self.time_limit[1]], 
        ["Board size", self.size[0], self.size[1]],
        ["Settings"],
        ["Quit"],
        ]
        # return self.menu_list

    def get_input(self):
        inp = self.stdscr.get_wch()

        match inp:
            case "w" | curses.KEY_UP | "8":
                if self.index in ([0, 2], [1, 2]):
                    if self.time_limit[self.index[0]] >= 5:
                        self.time_limit[self.index[0]] -= 5
                elif self.index[1] == 0:
                    self.index[0] = (self.index[0] - 1) % len(self.menu_list)
                elif self.index in ([2, 1], [2, 2]):
                    if self.size[self.index[1] - 1] >= 4:
                        self.size[self.index[1] - 1] -= 2
            
            case "s" | curses.KEY_DOWN | "2":
                if self.index in ([0, 2], [1, 2]):
                    self.time_limit[self.index[0]] += 5
                elif self.index[1] == 0:
                    self.index[0] = (self.index[0] + 1) % len(self.menu_list)
                elif self.index in ([2, 1], [2, 2]):
                    self.size[self.index[1] - 1] += 2

            case "a" | curses.KEY_LEFT | "4":
                self.index[1] = (self.index[1] - 1) % len(self.menu_list[self.index[0]])

            case "d" | curses.KEY_RIGHT | "6":
                self.index[1] = (self.index[1] + 1) % len(self.menu_list[self.index[0]])

            case "\n" | " " | "5":
                if self.index == [0, 0]:
                    game.singleplayer(self.stdscr, self.size[0], self.size[1], self.density, playtime=self.time_limit[0] if self.time_active[0] else -1, easy_mode=self.easy)
                    self.stdscr.nodelay(False)
                    self.p = P(self.stdscr)
                elif self.index == [1, 0]:
                    # game.singleplayer(self.stdscr, self.size[0], self.size[1], self.density, timed=self.time_active[0], easy_mode=self.easy)
                    pass
                    # TODO Multiplayer
                
                elif self.index == [0, 1]:
                    self.time_active[0] = not self.time_active[0]
                elif self.index == [1, 1]:
                    self.time_active[1] = not self.time_active[1]


                elif self.menu_list[self.index[0]] == ["Quit"]:
                    exit()


    def draw(self):
        self.build_list()
        self.stdscr.erase()
        y=get_y_middle(self.stdscr, self.menu_list)

        self.stdscr.addstr(y - 3, get_middle(self.stdscr, "Minewalker"), "Minewalker" + "\n", self.p.color("Red"))
        for i, e in enumerate(self.menu_list):
            start = get_middle(self.stdscr, e[0])
            self.stdscr.addstr(y + i, start, e[0], self.p.color(0, rev=(True if [i, 0] == self.index else False)))
            
            if i == self.index[0]:
                # x_start = start + len(e[0]) + len(" ")
                # y_start = y + i
                # if i in (0, 1, 2):
                #     self.stdscr.addstr(f"\t| ")
                self.stdscr.addstr("\t")
                if i in (0, 1):
                    self.stdscr.addstr(str(e[1]), self.p.color("green" if self.time_active[i] else 0, rev=(True if self.index[1] == 1 else False)))
                    self.stdscr.addstr("  ")
                    self.stdscr.addstr(str(e[2]), self.p.color(0, rev=(True if self.index[1] == 2 else False)))
                    y1, x1 = self.stdscr.getyx()
                    for shift in (-1, 1):
                        if e[2] + shift * 5 >= 0:
                            self.stdscr.addstr(y1 + shift, x1 - len(str(e[2] + shift * 5)), str(e[2] + shift * 5))

                elif i == 2:
                    self.stdscr.addstr(str(e[1]), self.p.color(0, rev=(True if self.index[1] == 1 else False)))
                    self.stdscr.addstr(" ")
                    self.stdscr.addstr(str(e[2]), self.p.color(0, rev=(True if self.index[1] == 2 else False)))
    

        self.stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(Menu.run)