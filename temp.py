import random # maybe, this is test stuff

def gen_mines(w, h):
    mines = [[random.randint(0, 1) for _ in range(w)] for _ in range(h)]
    for i in mines:
        print(i)

gen_mines(5, 5)