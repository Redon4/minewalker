import curses
from collections import defaultdict


class Perry:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.colors = {}
        curses.use_default_colors()

    def color(self, NAME, BACK=0):
        pair_id = f"{str(NAME).upper()}_{str(BACK).upper()}"

        if not pair_id in self.colors and isinstance(NAME, str):
            try:
                self.colors[pair_id] = [len(self.colors) + 1, getattr(curses, f"COLOR_{NAME.upper()}"), -1 if not BACK else getattr(curses, f"COLOR_{str(BACK).upper()}")]
            except AttributeError:
                raise ValueError(f"!!!Not a curses color!!!:\t{NAME} or {BACK}")
            color = self.colors[pair_id]
            curses.init_pair(color[0], color[1], color[2])

        elif isinstance(NAME, int):
            return curses.color_pair(NAME)

        return curses.color_pair(self.colors[pair_id][0])
