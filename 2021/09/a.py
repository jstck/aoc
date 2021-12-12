#!/usr/bin/env python3

import sys


grid = [[int(x) for x in list(line.strip())] for line in sys.stdin.readlines()]

#All lines are equally long, right?

xmax = len(grid[0])
ymax = len(grid)


dangerlevel = 0

for y in range(0,ymax):
    for x in range(0,xmax):
        cell = grid[y][x]

        isLow = True

        #Check left
        isLow = isLow and ((x == 0) or (cell < grid[y][x-1]))

        #Right
        isLow = isLow and ((x == xmax-1) or (cell < grid[y][x+1]))

        #Up
        isLow = isLow and ((y == 0) or (cell < grid[y-1][x]))

        #Down
        isLow = isLow and ((y == ymax-1) or (cell < grid[y+1][x]))

        if isLow:
            print("Low spot at",x,y)
            dangerlevel += cell + 1

print("Total danger:", dangerlevel)