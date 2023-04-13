import itertools
import logging
import requests
import json

class Board:

    def __init__(self, width: int, height: int):
        self.board = [[" " for x in range(width)] for y in range(height)]

    @staticmethod
    def __print_border_row(length: int):
        for x in range(length):
            print("---", end="")
        print("--")

    def print(self):
        print(end=" ")
        for count in range(len(self.board[0])):
            print("|", count, end="")

        print("|")
        for count, row in enumerate(self.board):
            self.__print_border_row(len(self.board[0]))
            print(count, end="")

            for cell in row:
                print("|", cell, end="")
            print("|")

        self.__print_border_row(len(self.board[0]))
        print()

    def get_board(self) -> list:
        return self.board

    def insert_counter(self, position: int, counter: str) -> list:
        for idx, row in enumerate(reversed(self.board)):
            # Check if empty
            if row[position] == " ":
                row[position] = counter
                break
            # Check if top row
            if idx == len(self.board) - 1:
                raise ValueError("Max counters reached in column")

        return self.board

    def __check_row(self, length: int, counter: str, row_idx: int) -> bool:
        line = ''.join(self.board[row_idx])
        if counter * length in line:
            return True
        else:
            return False

    def __check_col(self, length: int, counter: str, position: int) -> bool:
        line = ''.join(row[position] for row in self.board)

        if counter * length in line:
            return True
        else:
            return False

    def __get_row_from_col(self, counter: str, col_idx: int) -> int:
        for row_idx, row in enumerate(self.board):
            if row[col_idx] == counter:
                return row_idx
        return -1

    def __check_ngtv_line(self, length: int, counter: str, col_idx: int, row_idx: int) -> bool:
        line = ""
        for n in range(-length, length, 1):
            if not (col_idx + n < 0 or col_idx + n >= len(self.board[0]) or
                    row_idx + n < 0 or row_idx + n >= len(self.board)):
                line += (self.board[row_idx + n][col_idx + n])

        if counter * length in line:
            return True
        else:
            return False

    def __check_pos_line(self, length: int, counter: str, col_idx: int, row_idx: int) -> bool:
        line = ""

        for n in range(-length, length, 1):
            if not (col_idx + n < 0 or col_idx + n >= len(self.board[0]) or
                    row_idx - n < 0 or row_idx - n >= len(self.board)):
                line += (self.board[row_idx - n][col_idx + n])

        if counter * length in line:
            return True
        else:
            return False

    def check_win(self, length: int, counter: str, col_idx: int) -> bool:
        row_idx = self.__get_row_from_col(counter, col_idx)

        if self.__check_col(length, counter, col_idx):
            return True
        elif self.__check_row(length, counter, row_idx):
            return True
        elif self.__check_ngtv_line(length, counter, col_idx, row_idx):
            return True
        elif self.__check_pos_line(length, counter, col_idx, row_idx):
            return True
        else:
            return False

    def check_draw(self) -> bool:
        line = ''.join(self.board[0])

        if " " in line:
            return False
        else:
            return True


def send_win(name: str):
    url = "https://2o3owjg2w7.execute-api.eu-west-2.amazonaws.com/prod/scoreboard"
    response = requests.post(
        url,
        json={"player": name.title()}
    )

    if response.status_code == 200:
        print("Win added to scoreboard")

def get_scoreboard() -> dict:
    url = "https://2o3owjg2w7.execute-api.eu-west-2.amazonaws.com/prod/scoreboard"
    response = requests.get(url)
    return json.loads(response.content)

def print_scoreboard(scoreboard: dict):

    print()
    print("-"*29)
    print (f"| Scoreboard                |")
    print("-"*29)
    print (f"| Player         | Score    |")
    print("-"*29)
    spc=" "
    for name, score in scoreboard.items():
        print (f"| {name}{spc*(15-len(name))}| {score}{spc*(9-len(score))}|")
        print ("-"*29)
    print()


def turn(board: Board, counter: str, win_length: int, player: str) -> bool:
    while True:
        try:
            counter_pos = int(input(f"{player.title()} ({counter}) enter column number: "))

            if counter_pos < 0:
                raise ValueError("Cant enter values below 0")

            print()
            board.insert_counter(counter_pos, counter)
            board.print()

            if board.check_win(win_length, counter, counter_pos):
                print(f"{player.title()} ({counter}) Wins!")

                return True
            else:
                return False

        except Exception as e:
            logging.warning("Invalid input")
            logging.warning(e)


def play_game():
    print_scoreboard(get_scoreboard())
    win_length = 4
    board = Board(2, 2)
    counters = itertools.cycle(["o", "x"])

    players = itertools.cycle([
        input(f"Player 1 ({next(counters)}) enter name: "),
        input(f"Player 2 ({next(counters)}) enter name: ")
    ])

    board.print()

    while True:
        player = next(players)
        if board.check_draw():
            print()
            print("It is a draw!")
            print()
            break
        if turn(board, next(counters), win_length, player):
            print()
            send_win(player)
            print()
            break

    print_scoreboard(get_scoreboard())

if __name__ == '__main__':
    play_game()
    # print_scoreboard(get_scoreboard())
