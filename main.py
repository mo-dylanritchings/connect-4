def create_board(w, h):
    return [[" " for x in range(w)] for y in range(h)]


def print_border_row(length):
    for x in range(length + 1):
        print("---", end="")
    print("-")


def print_board(board):
    for row in board:
        print_border_row(len(board))

        for cell in row:
            print("|", cell, end="")
        print("|")

    print_border_row(len(board))


if __name__ == '__main__':
    board = create_board(7, 6)
    print_board(board)
