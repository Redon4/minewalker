import random # maybe, this is test stuff

def gen_mines(w, h):
    mines = [[random.choice([0, 0, 0, 0, 0, 1]) for _ in range(w)] for _ in range(h)]
    mines[0][:2] = [0, 0]
    mines[1][:2] = [0, 0]
    # mines[:2][:2] = [[0, 0], [0, 0]]
    return mines


if __name__ == "__main__":
    w, h = 10, 10
    mines = gen_mines(w, h)
    for row in mines:
        print(" ".join(str(x) for x in row))