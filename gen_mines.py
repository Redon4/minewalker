import random
from utils import clamp, clamp_to_matrix


def gen_mines(w, h, density):
    if density > 0:
        choice_list = [0] * int(1 / density - 1) + [1] # proper desity
    else:
        choice_list = [0]
    mines = [[random.choice(choice_list) for _ in range(w)] for _ in range(h)]
    mines[0][:2] = [0, 0] # spawn area
    mines[1][:2] = [0, 0]

    mines[-1][-2:] = [0, 0] # goal area
    mines[-2][-2:] = [0, 0]
    return mines

def clear_path(stdscr, mines=[], randomness=3, delay=None):
    if not mines: # if not testing
        mines = stdscr
        testing = False
    else:
        testing = True

    if testing:
        curses.use_default_colors()

    current_pos=[0, 0] # x, y
    cnt=0
    goalx = len(mines[0]) - 1
    goaly = len(mines) - 1
    while (current_pos[0] != goalx or current_pos[1] != goaly): # when not in goal
        if cnt % randomness == 0 if randomness != 0 else True: # if randomness is 0, theres no randomness
            fastest=[-1, (0, 0)] # tracks the fastest of the 4 ways
            l = [(0, 1), (1, 0), (-1, 0), (0, -1)] # all 4 directions
            random.shuffle(l) # for no bias
            for i in l: # x, y
                new_pos = [current_pos[o] + i[o] for o in range(len(current_pos))] # gen a new pos for every direction in l

                new_pos = [clamp(0, new_pos[0], goalx), clamp(0, new_pos[1], goaly)] # clampe the new pos

                # check the 4 squares around new_pos if they are already "surrounded" by at least 2
                # then dont go there, pass instead >:)

                found=0
                cnt1=0
                for j in new_pos:
                    lenmines = [goalx, goaly]
                    if mines[min(j + 1, lenmines[cnt1])] == 2 or mines[max(0, j - 1)] == 2:
                        found += 1
                        cnt1 += 1

                current_distance = (goalx - new_pos[0]) + (goaly - new_pos[1])

                if found > 2:
                    current_distance += 1000

                if fastest[0] == -1: # if its the first
                    fastest = [current_distance, i]

                elif current_distance < fastest[0]: # if its faster
                    fastest = [current_distance, i]

            # go the fastest way
            current_pos[0] += fastest[1][0]
            current_pos[1] += fastest[1][1]

        else: # random
            direction = random.choice([-1, 1])
            x_or_y = random.choice([0, 1])
            current_pos[x_or_y] += direction
            current_pos[0], current_pos[1] = clamp_to_matrix(current_pos[0], current_pos[1], mines) # clamp the random

        if not testing:
            mines[current_pos[0]][current_pos[1]] = 2

        else:
            mines[current_pos[0]][current_pos[1]] = " "
            time.sleep(delay)
            stdscr.erase()
            for y, row in enumerate(mines):
                stdscr.addstr(y, 0, " ".join(map(str, row)))
                stdscr.move(current_pos[0], current_pos[1] * 2)
            stdscr.refresh()

        cnt += 1

    mines = [[0 if cell == 2 else cell for cell in row] for row in mines] # goes through every cell and replaces 2 with 0
    if testing:
        stdscr.addstr("\n" + "-" * stdscr.getmaxyx()[1] + "Press any button to quit")
        stdscr.getch()
    return mines


if __name__ == "__main__":
    import curses
    import time

    w, h = 50, 50
    density = 0.25
    curses.wrapper(clear_path, gen_mines(w, h, density), randomness=int(input("How random shall it be?\n:")), delay=0.01)
    # for row in mines:
    #     print(" ".join(str(x) for x in row))
