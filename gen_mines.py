import random # maybe, this is test stuff

def gen_mines(w, h):
    mines = [[random.randint(0, 1) for _ in range(w)] for _ in range(h)]
    return mines