from utils import get_middle, get_y_middle, clamp
import curses
from perry import Perry as P
import game_modes as game

class Menu:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.index = [0, 0] # main menu, sub menu


        self.size = [20, 20] # w, h
        self.time_limit = [40, 40] # Single-, Multiplayer
        self.time_active = [False, False]
        self.density = 25
        self.easy = True


        self.p = P(stdscr)

        curses.use_default_colors()
        curses.curs_set(0)

    @classmethod
    def run(cls, stdscr):
        clas = cls(stdscr)
        clas.game = True
        while clas.game:
            clas.draw()

            clas.get_input()


    def build_list(self):
        # self.menu_list = [
        # ["Singleplayer", "Time limit", self.time_limit[0]],
        # ["Multiplayer", "Time limit", self.time_limit[1]],
        # ["Board size", self.size[0], self.size[1]],
        # ["Settings"],
        # ["Quit"],
        # ]round(min(100, self.density + 5), 2)
        self.menu_list = [
            {
                "label": "Singleplayer",
                "type": "time",
                "limit": self.time_limit[0],
                "idx": 0,
                "fields": ["start", "toggle", "value"],
                "width":3,
            },

            {
                "label": "Multiplayer",
                "type": "time",
                "limit": self.time_limit[1],
                "idx": 1,
                "fields": ["start", "toggle", "value"],
                "width":3,
            },

            {
                "label": "Board size",
                "type": "size",
                "value": self.size,
                "fields": ["none", "value", "value"],
                "width":3,
            },

            {
                "label": "Density",
                "type": "density",
                "value": self.density,
                "fields": ["none", "value"],
                "width": 2,
            },

            {
                "label": "Easy mode",
                "type": "setting",
                "value": self.easy,
                "fields": ["toogle"],
                "width":1,
            },

            # {
            #     "label": "Settings",
            #     "type": "submenu",
            #     "fields": ["submenu"],
            #     "width":1,
            # },

            {
                "label": "Quit",
                "type": "action",
                "fields": ["quit"],
                "width":1,
            },
        ]
        # return self.menu_list

    def get_input(self):
        item = self.menu_list[self.index[0]]
        field = item["fields"][self.index[1]]

        inp = self.stdscr.get_wch()

        match inp:
            case "w" | curses.KEY_UP | "8":
                if field == "value":
                    if item["type"] == "time":
                        idx = item["idx"]
                        if self.time_limit[idx] >= 5:
                            self.time_limit[idx] -= 5

                    elif item["type"] == "size":
                        idx = self.index[1] - 1
                        if self.size[idx] >= 4:
                            self.size[idx] -= 2

                    elif item["type"] == "density":
                        self.density = clamp(0, self.density - 5, 100)


                elif self.index[1] == 0:
                        self.index[0] = (self.index[0] - 1) % len(self.menu_list)



            case "s" | curses.KEY_DOWN | "2":
                if field == "value":
                    if item["type"] == "time":
                        self.time_limit[item["idx"]] += 5

                    elif item["type"] == "size":
                        self.size[self.index[1] - 1] += 2

                    elif item["type"] == "density":
                        self.density = clamp(0, self.density + 5, 100)
                elif self.index[1] == 0:
                    self.index[0] = (self.index[0] + 1) % len(self.menu_list)


            case "a" | curses.KEY_LEFT | "4":
                self.index[1] = (self.index[1] - 1) % item["width"]



            case "d" | curses.KEY_RIGHT | "6":
                self.index[1] = (self.index[1] + 1) % item["width"]

            case "\n" | " " | "5":
                if item["label"] == "Singleplayer" and field == "start":
                    game.singleplayer(
                        self.stdscr,
                        self.size[0], self.size[1],
                        self.density,
                        playtime=self.time_limit[0] if self.time_active[0] else -1,
                        easy_mode=self.easy
                    )

                    self.stdscr.nodelay(False)
                    self.p = P(self.stdscr)

                elif item["label"] == "Multiplayer" and field == "start":
                    # game.singleplayer(self.stdscr, self.size[0], self.size[1], self.density, timed=self.time_active[0], easy_mode=self.easy)
                    pass
                    # TODO Multiplayer

                elif item["type"] == "time" and field == "toggle":
                    self.time_active[item["idx"]] = not self.time_active[item["idx"]]

                elif item["label"] == "Easy mode":
                    self.easy = not self.easy

                elif item["label"] == "Quit":
                    self.game = False

            case "q":
                self.game = False


    def draw(self):
        self.build_list()
        self.stdscr.erase()
        y=get_y_middle(self.stdscr, self.menu_list)

        self.stdscr.addstr(y - 3, get_middle(self.stdscr, "Minewalker"), "Minewalker" + "\n", self.p.color("Red"))
        for i, item in enumerate(self.menu_list):
            label = item["label"]


            start = get_middle(self.stdscr, label)
            if label == "Easy mode":
                # self.stdscr.addstr(y + i, start, label, self.p.color("green" if self.easy else 0, rev=(True if ...)))
                color = "green" if self.easy else 0
            else:
                color = 0
            self.stdscr.addstr(y + i, start, label, self.p.color(color, rev=(True if [i, 0] == self.index else False)))

            if i == self.index[0]:

                field = item["fields"][self.index[1]]
                # x_start = start + len(e[0]) + len(" ")
                # y_start = y + i
                # if i in (0, 1, 2):
                #     self.stdscr.addstr(f"\t| ")
                self.stdscr.addstr("\t")
                if item["type"] == "time":
                    idx = item["idx"]

                    self.stdscr.addstr("Time limit", #i +
                        self.p.color("green" if self.time_active[idx] else 0,
                            rev=(True if self.index[1] == 1 else False)
                        )
                    )
                    self.stdscr.addstr("  ")
                    self.stdscr.addstr(str(item["limit"]),
                        self.p.color(0,
                            rev=(True if self.index[1] == 2 else False) # cant use field because there are more than 1 "value" things
                        )
                    )
                    self.stdscr.addstr("s")

                    # this code is prob. unstable, i only did it once and then copied it
                    y1, x1 = self.stdscr.getyx()
                    for shift in (-1, 1):
                        if item["limit"] + shift * 5 >= 0:
                            self.stdscr.addstr(y1 + shift, x1 - len(str(item["limit"] + shift * 5) + "s"), str(item["limit"] + shift * 5) + "s")

                elif item["type"] == "size":
                    self.stdscr.addstr("w: ")
                    self.stdscr.addstr(str(self.size[0]),
                        self.p.color(0,
                            rev=(True if self.index[1] == 1 else False)
                        )
                    )
                    y1, x1 = self.stdscr.getyx()
                    for shift in (-1, 1):
                        if self.size[0] + shift * 2 >= 2:
                            self.stdscr.addstr(y1 + shift, x1 - len(str(self.size[0] + shift * 2)), str(self.size[0] + shift * 2))
                    y1, x1 = self.stdscr.getyx()
                    self.stdscr.move(y1 - 1, x1)
                    self.stdscr.addstr(" h: ")
                    self.stdscr.addstr(str(self.size[1]),
                        self.p.color(0,
                            rev=(True if self.index[1] == 2 else False)
                        )
                    )

                    y1, x1 = self.stdscr.getyx()
                    for shift in (-1, 1):
                        if self.size[1] + shift * 2 >= 2:
                            self.stdscr.addstr(y1 + shift, x1 - len(str(self.size[1] + shift * 2)), str(self.size[1] + shift * 2))


                elif item["type"] == "density":
                    placeholder = " " * (3 - len(str(self.density)))
                    self.stdscr.addstr(placeholder)
                    self.stdscr.addstr(f"{self.density:d}",
                        self.p.color(0,
                            rev=(True if field == "value" else False)
                        )
                    )
                    self.stdscr.addstr(" %")

                    y1, x1 = self.stdscr.getyx()
                    for shift in (-1, 1):
                        val = self.density + shift * 5
                        if 0 <= val <= 95:
                            self.stdscr.addstr(
                                y1 + shift,
                                x1 - len(f"{val:>3d} %"),
                                f"{val:>3d} %"
                            )
                    # y1, x1 = self.stdscr.getyx()
                    # self.stdscr.move(y1 - 1, x1)
                    # self.stdscr.addstr(" %")


        self.stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(Menu.run)