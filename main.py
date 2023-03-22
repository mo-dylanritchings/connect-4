def create_board(w: int, h: int):
    return [[" " for x in range(w)] for y in range(h)]


def print_border_row(length: int):
    for x in range(length):
        print("---", end="")
    print("-")


def print_board(board: list):
    for row in board:
        print_border_row(len(board[0]))

        for cell in row:
            print("|", cell, end="")
        print("|")

    print_border_row(len(board[0]))


def insert_counter(board: list, position: int, counter: str):
    for idx, row in enumerate(reversed(board)):
        # Check if empty
        if row[position] == " ":
            row[position] = counter
            break
        # Check if top row
        if idx == len(board)-1:
            # do something
            print("error")

    return board



if __name__ == '__main__':
    board = create_board(7, 5)
    print_board(board)
    board = insert_counter(board, 2, "x")
    board = insert_counter(board, 2, "x")
    print_board(board)
