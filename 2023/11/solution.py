#!/usr/bin/env python3

import itertools
import sys

grid = []
for line in sys.stdin.readlines():
    line = line.strip()
    row = list(line)
    grid.append(row)

size_y = len(grid)
size_x = len(grid[0])

#print(f"Grid {size_x} X {size_y}")

colcount = [0] * size_x
emptyrows = []
stars = []

for y, row in enumerate(grid):
    emptyrow = True
    for x, pixel in enumerate(row):
        if pixel == "#":
            colcount[x] += 1
            stars.append((x,y))
            emptyrow = False
    if emptyrow:
        emptyrows.append(y)

emptycols = [x for x,c in enumerate(colcount) if c==0]

#print(f"Empty rows: {emptyrows}")
#print(f"Empty cols: {emptycols}")
#print(f"Stars: {stars}")

distances1 = []
distances2 = []

for star1, star2 in itertools.combinations(stars, 2):
    xx = [star1[0], star2[0]]
    xx.sort()
    yy = [star1[1], star2[1]]
    yy.sort()

    (x1, x2) = xx
    (y1, y2) = yy

    dx = x2-x1
    dy = y2-y1

    exp = 0

    PART2_EXPANSION = 1000000

    for x in emptycols:
        if x1 <= x <= x2:
            exp += 1

    for y in emptyrows:
        if y1 <= y <= y2:
            exp += 1

    distance1 = dx+dy+exp
    distances1.append(distance1)

    distance2 = dx + dy + exp * (PART2_EXPANSION-1)
    distances2.append(distance2)

print("PART1:", sum(distances1))
print("PART2:", sum(distances2))