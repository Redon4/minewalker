import random # maybe, this is test stuff

def gen_mines(w, h):
    mines = [[random.randint(0, 1) for _ in range(w)] for _ in range(h)]
    return mines


if __name__ == "__main__":
    w, h = 10, 10
    mines = gen_mines(w, h)
    for row in mines:
        print(" ".join(str(x) for x in row))