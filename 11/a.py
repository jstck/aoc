#!/usr/bin/env python3

import sys


grid = []

for line in sys.stdin.readlines():
    grid.append([int(x) for x in list(line.strip())])


def printgrid(grid):
    for row in grid:
        print("".join(map(str, row)))

printgrid(grid)
print()

def cycle(grid):
    #Increase all the things by 1
    flashed = []

    xmax = len(grid[0])
    ymax = len(grid)
    for y in range(ymax):
        flashed.append([False] * xmax)
        for x in range(xmax):
            grid[y][x] += 1

    #Repeat until no more flashes
    newflash = True
    flashes = 0

    while newflash:
        newflash = False

        for y in range(0, ymax):
            for x in range(0, xmax):
                if grid[y][x]>9:

                    #I FLASH
                    flashes += 1
                    flashed[y][x] = True
                    newflash = True
                    grid[y][x] = 0

                    #Increase neighbours that haven't yet flashed
                    for dy in [-1, 0, 1]:
                        y1 = y+dy
                        if y1<0 or y1>=ymax:
                            continue
                        for dx in [-1, 0, 1]:
                            x1 = x+dx
                            if x1<0 or x1>=xmax:
                                continue
                            if dx==0 and dy==0:
                                continue

                            if not flashed[y1][x1]:
                                grid[y1][x1] += 1

    return flashes

flashes = 0

for step in range(100):
    flashes += cycle(grid)

print()
printgrid(grid)
print(flashes)