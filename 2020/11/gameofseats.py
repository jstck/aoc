#!/usr/bin/env python3

import sys
import re

board = [list(x.strip()) for x in sys.stdin.readlines()]

board_width = len(board[0]) #All lines are assumed to be equal
board_height = len(board)

def count_neighbours(board, x, y):
    count = 0

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:

            #Don't count self
            if dx==0 and dy==0:
                continue

            xn = x+dx
            yn = y+dy
            
            #Stop "wrap-around"
            if xn<0 or xn >= board_width:
                continue
            if yn<0 or yn >= board_height:
                continue

            if board[y+dy][x+dx] == '#':
                count += 1

    return count

def count_visible_neighbours(board, x, y):
    count = 0

    #Each directions, in x/y-steps
    directions = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]

    for (dx,dy) in directions:
        for distance in range(1,max(board_width,board_height)): #Max range is max of width/height
            
            xn = x+distance*dx
            yn = y+distance*dy

            #Stop "wrap-around" when we reach edge of board
            if xn<0 or xn >= board_width:
                break
            if yn<0 or yn >= board_height:
                break

            neighbour = board[yn][xn]

            if neighbour == '#':
                count += 1
                break
            if neighbour == 'L':
                break

    return count

def update_board(board, mode=1):
    changed = False
    newboard = []

    for y in range(0, board_height):
        newrow = []
        for x in range(0, board_width):
            current = board[y][x]
            
            if current==".":
                new = "." #Floor is floor

            if mode == 1:
                n = count_neighbours(board, x, y)
                occupation_limit=4
            elif mode == 2:
                n = count_visible_neighbours(board, x, y)
                occupation_limit=5

            if current == "L":
                if n ==0:
                    new = "#" #Fill seat
                    changed = True
                else:
                    new = "L" #Stays empty
            elif current == "#":
                if n >= occupation_limit:
                    new = "L" #Leave seat
                    changed = True
                else:
                    new = "#" #Stays filled
            

            newrow.append(new)
        newboard.append(newrow)
    
    return (changed, newboard)


def printboard(board):
    print("\n".join(["".join(row) for row in board]))
    print()


changed = True

rounds = 0
maxrounds = 200

if len(sys.argv) >= 2 and sys.argv[1] == '2':
    task = 2
else:
    task = 1

while changed:
    (changed, board) = update_board(board, task)
    #printboard(board)
    rounds += 1
    if rounds >= maxrounds:
        break


printboard(board)

print(rounds, "rounds")

people = sum([r.count("#") for r in board])

print(people, "people")