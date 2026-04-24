import random # maybe, this is test stuff

def gen_mines(w, h, density):
    choice_list = [0] * int(1 / density - 1) + [1] # proper desity
    mines = [[random.choice(choice_list) for _ in range(w)] for _ in range(h)]
    mines[0][:2] = [0, 0] # spawn area
    mines[1][:2] = [0, 0]

    mines[-1][-2:] = [0, 0] # goal area
    mines[-2][-2:] = [0, 0]
    return mines

def clear_path(mines):
    current_pos = [0, 0] # x, y
    c=0
    while (current_pos[0] != len(mines[0]) - 1 or current_pos[1] != len(mines) - 1):
        if c % 2 == 0:
            direction = random.choice([-1, 1])
            x_or_y = random.choice([0, 1])
            current_pos[x_or_y] += direction
            current_pos[0] = max(0, min(len(mines[0]) - 1, current_pos[0]))
            current_pos[1] = max(0, min(len(mines) - 1, current_pos[1]))
        else:
            # TODO: Paul i have a misson for you, 
            # Do real pathfinding here, its not that hard
            # But keep the random part, then the path leads to the goal but its not a straight line
            pass


        # temp_pos = random.randint(0, 3)
        # match temp_pos:
        #     case 0:
        #         if current_pos[1] - 1 >= 0:
        #             current_pos[1] -= 1
        #     case 1:
        #         if current_pos[0] + 1 <= len(mines[0]) - 1:
        #             current_pos[0] += 1
        #     case 2:
        #         if current_pos[1] + 1 <= len(mines) - 1:
        #             current_pos[1] += 1
        #     case 3:
        #         if current_pos[0] - 1 >= 0:
        #             current_pos[0] -= 1
        mines[current_pos[0]][current_pos[1]] = 2
        c += 1
    return mines



if __name__ == "__main__":
    w, h = 10, 10
    density = 1
    mines = clear_path(gen_mines(w, h, density))
    for row in mines:
        print(" ".join(str(x) for x in row))
