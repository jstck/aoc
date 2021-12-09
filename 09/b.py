#!/usr/bin/env python3

import sys


grid = [[int(x) for x in list(line.strip())] for line in sys.stdin.readlines()]

#All lines are equally long, right?

xmax = len(grid[0])
ymax = len(grid)

visited = [[False]*xmax for y in range(0,ymax)]

lows = []

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
            lows.append((x, y))

basins = []


for x0, y0 in lows:

    if visited[y0][x0]:
        #Mistakes were made
        continue
    
    size = 0

    queue = [(x0, y0)]
    
    while len(queue) > 0:

        (x, y) = queue.pop(0)

        #Don't revisit nodes
        if visited[y][x]:
            continue

        
        visited[y][x] = True
        if grid[y][x] == 9:
            continue

        size += 1

        if (x > 0):
            queue.append((x-1, y))
        if (x < xmax - 1):
            queue.append((x+1, y))

        if (y > 0):
            queue.append((x, y-1))
        if (y < ymax - 1):
            queue.append((x, y+1))

    basins.append(size)


basins.sort(reverse=True)
print(basins)

print(basins[0]*basins[1]*basins[2])