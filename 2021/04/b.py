#!/usr/bin/env python3

import sys

BOARD_SIZE=5

lines = [l.strip() for l in sys.stdin.readlines()]

numbers = lines[0].split(",")
numbers = [int(x.strip()) for x in numbers]

print(numbers)

boards = []

class Bingo:
    def __init__(self, raw_board):
        self.board = []
        self.checked = [ [False]*BOARD_SIZE for i in range(BOARD_SIZE)]

        for line in raw_board:
            boardline = [int(x.strip()) for x in line.split()]
            self.board.append(boardline)

    def checkNumber(self, number):
        for row in range(0, BOARD_SIZE):
            for col in range(0, BOARD_SIZE):
                if self.board[row][col] == number:
                    self.checked[row][col] = True
        self.lastNumber = number


    def checkBingo(self):
        for row in range(0, BOARD_SIZE):

            rowBingo = True
            for col in range(0, BOARD_SIZE):
                if not self.checked[row][col]:
                    rowBingo = False
                    break

            if rowBingo: return True

        for col in range(0, BOARD_SIZE):

            colBingo = True
            for row in range(0, BOARD_SIZE):
                if not self.checked[row][col]:
                    colBingo = False
                    break

            if colBingo: return True

        return False

    def bingoValue(self):
        sum = 0
        for row in range(0, BOARD_SIZE):
            for col in range(0, BOARD_SIZE):
                if not self.checked[row][col]:
                    sum += self.board[row][col]

        return sum*self.lastNumber


lines = lines[2:]

while len(lines)>0:
    board_raw = lines[0:5]
    lines = lines[6:]

    boards.append(Bingo(board_raw))

for num in numbers:
    wins = []
    print("Drawing", num)
    for i in range(len(boards)):
        board = boards[i]
        board.checkNumber(num)
        if board.checkBingo():
            print("Bingo on board", i)
            print("Bingovalue", board.bingoValue())
            wins.append(i)

    #Remove boards backwards for safety
    wins.reverse()

    for win in wins:
        print("Removing board", win)
        del boards[win]

    if len(boards) == 0:
        sys.exit(0)