import random # maybe, this is test stuff

def gen_mines(w, h):
    mines = [[random.choice([0, 0, 0, 0, 0, 1]) for _ in range(w)] for _ in range(h)] # damit die change for 1 kleiner ist
    mines[0][:2] = [0, 0] # spawn area
    mines[1][:2] = [0, 0]
    return mines


if __name__ == "__main__": # zum testen
    w, h = 10, 10
    mines = gen_mines(w, h)
    for row in mines:
        print(" ".join(str(x) for x in row))