import curses
from collections import defaultdict


class Perry:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.colors = {}
        curses.use_default_colors()

    def color(self, NAME, BACK=0, reverse=False, rev=False):
        pair_id = f"{str(NAME).upper()}_{str(BACK).upper()}"

        if not pair_id in self.colors and isinstance(NAME, str):
            try:
                self.colors[pair_id] = [len(self.colors) + 1]
                self.colors[pair_id].append(getattr(curses, f"COLOR_{NAME.upper()}"))
                self.colors[pair_id].append(-1 if not BACK else getattr(curses, f"COLOR_{str(BACK).upper()}"))
            except AttributeError:
                raise ValueError(f"!!!Not a curses color!!!:\t{NAME} or {BACK}")
            
            color = self.colors[pair_id]
            curses.init_pair(color[0], color[1], color[2])

        elif isinstance(NAME, int) and not BACK:
            return curses.color_pair(NAME)

        if reverse or rev:
            return curses.color_pair(self.colors[pair_id][0]) | curses.A_REVERSE
        return curses.color_pair(self.colors[pair_id][0])
