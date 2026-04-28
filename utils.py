def clamp(start, value, end):
    return max(start, min(value, end))

def clamp_to_matrix(x, y, matrix): # matrix width has to be the same for every row
    r=[0, 0]
    r[0] = clamp(0, x, len(matrix[0]) - 1)
    r[1] = clamp(0, y, len(matrix) - 1)

    return [r[0], r[1]]


def get_middle(stdscr, text):
    width = stdscr.getmaxyx()[1]
    middle = width // 2 - (len(text) // 2)
    return middle

def get_y_middle(stdscr, list):
    height = stdscr.getmaxyx()[0]
    middle = height // 2 - (len(list) // 2)
    return middle