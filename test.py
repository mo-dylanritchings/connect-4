
from main import *

def test_board_add_counter(board):
    board.insert_counter(0, "o")
    assert board.get_board()[-1][0] == "o"


def test_check_win_horizontal(board):
    board.insert_counter(0, "o")
    board.insert_counter(1, "o")
    board.insert_counter(2, "o")
    board.insert_counter(3, "o")

    assert board.check_win(4, "o", 2) is True

def test_check_win_vertical(board):
    board.insert_counter(0, "o")
    board.insert_counter(0, "o")
    board.insert_counter(0, "o")
    board.insert_counter(0, "o")
    assert board.check_win(4, "o", 0) is True


def test_check_win_negative_gradient(board):
    board.insert_counter(2, "x")
    board.insert_counter(1, "x")
    board.insert_counter(1, "x")
    board.insert_counter(0, "x")
    board.insert_counter(0, "x")
    board.insert_counter(0, "x")
    board.insert_counter(0, "o")
    board.insert_counter(1, "o")
    board.insert_counter(2, "o")
    board.insert_counter(3, "o")
    board.print()
    assert board.check_win(4, "o", 1) is True

def test_check_win_positive_gradient(board):
    board.insert_counter(1, "x")
    board.insert_counter(2, "x")
    board.insert_counter(2, "x")
    board.insert_counter(3, "x")
    board.insert_counter(3, "x")
    board.insert_counter(3, "x")
    board.insert_counter(0, "o")
    board.insert_counter(1, "o")
    board.insert_counter(2, "o")
    board.insert_counter(3, "o")

    assert board.check_win(4, "o", 1) is True


def test_check_win_positive_gradient2():
    board = Board(7, 6)
    board.insert_counter(1, "x")
    board.insert_counter(2, "x")
    board.insert_counter(2, "x")
    board.insert_counter(3, "x")
    board.insert_counter(3, "x")
    board.insert_counter(3, "x")
    board.insert_counter(0, "o")
    board.insert_counter(1, "o")
    board.insert_counter(2, "o")
    board.insert_counter(3, "o")

    assert board.check_win(4, "o", 1) is True



if __name__ == '__main__':

    board = Board(7, 6)
    test_board_add_counter(board)
    board = Board(7, 6)
    test_check_win_horizontal(board)
    board = Board(7, 6)
    test_check_win_vertical(board)
    board = Board(7, 6)
    test_check_win_negative_gradient(board)
    board = Board(7, 6)
    test_check_win_positive_gradient(board)
    board = Board(7, 6)

    # cProfile.run("test_check_win_positive_gradient(board)", )

