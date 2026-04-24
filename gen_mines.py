import random # maybe, this is test stuff
from utils import clamp

def gen_mines(w, h, density):
    choice_list = [0] * int(1 / density - 1) + [1] # proper desity
    mines = [[random.choice(choice_list) for _ in range(w)] for _ in range(h)]
    mines[0][:2] = [0, 0] # spawn area
    mines[1][:2] = [0, 0]

    mines[-1][-2:] = [0, 0] # goal area
    mines[-2][-2:] = [0, 0]
    return mines

def clear_path(mines):
    current_pos=[0, 0] # x, y
    cnt=0
    while (current_pos[0] != len(mines[0]) - 1 or current_pos[1] != len(mines) - 1):
        if cnt % 3 == 0:
            fastest=[-1, (0, 0)]
            l = [(0, 1), (1, 0), (-1, 0), (0, -1)]
            random.shuffle(l)
            for i in l: # x, y
                new_pos = [current_pos[o] + i[o] for o in range(len(current_pos))]
                
                new_pos = [clamp(0, len(mines[0]) - 1, new_pos[0]), clamp(0, len(mines) - 1, new_pos[1])]
                
                goalx = len(mines[0]) - 1
                goaly = len(mines) - 1

                # check the 4 squares around new_pos if they are already "surrounded" by at least 2
                # then dont go there, pass instead >:)
                
                current_fastest = (goalx - new_pos[0]) + (goaly - new_pos[1])
                found=0
                cnt=0
                for j in new_pos:
                    lenmines = [len(mines[0]) - 1, len(mines) - 1]
                    if mines[min(j + 1, lenmines[cnt])] == 2 or mines[max(0, j - 1)] == 2:
                        found += 1
                        cnt += 1
                
                if found > 2:
                    current_fastest += 1000

                if fastest[0] == -1:
                    fastest = [current_fastest, i]
                elif current_fastest < fastest[0]:
                    fastest = [current_fastest, i]
            current_pos[0] += fastest[1][0]
            current_pos[1] += fastest[1][1]

        else:
            direction = random.choice([-1, 1])
            x_or_y = random.choice([0, 1])
            current_pos[x_or_y] += direction
            current_pos[0] = max(0, min(len(mines[0]) - 1, current_pos[0]))
            current_pos[1] = max(0, min(len(mines) - 1, current_pos[1]))

        mines[current_pos[0]][current_pos[1]] = 2
        cnt += 1
    mines = [[0 if cell == 2 else cell for cell in row] for row in mines] # goes through every cell and replaces 2 with 0
    return mines



if __name__ == "__main__":
    w, h = 10, 10
    density = 0.25
    mines = clear_path(gen_mines(w, h, density))
    for row in mines:
        print(" ".join(str(x) for x in row))
