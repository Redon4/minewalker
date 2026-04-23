import random # maybe, this is test stuff

def gen_mines(w, h, density=0.2):
    choice_list = [0] * int(1 / density - 1) + [1] # proper desity
    mines = [[random.choice(choice_list) for _ in range(w)] for _ in range(h)] # damit die change for 1 kleiner ist
    mines[0][:2] = [0, 0] # spawn area
    mines[1][:2] = [0, 0]

    mines[-1][-2:] = [0, 0] # goal area
    mines[-2][-2:] = [0, 0]
    return mines


if __name__ == "__main__": # zum testen
    w, h = 10, 10
    density = 1
    mines = gen_mines(w, h, density)
    for row in mines:
        print(" ".join(str(x) for x in row))