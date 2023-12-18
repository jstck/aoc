#!/usr/bin/env python3

import sys


sys.path.append("../..")
from lib.aoc import *

def floodfill(grid: list[list[str]]) -> list[list[str]]:
    #make a copy
    result = []
    for row in grid:
        result.append(row.copy())

    #Pick a line, any line:
    y = len(result)//2

    #Find position of first wall
    x = result[y].index("#")+1
    x = result[y].index(".", x)

    assert result[y][x]=="."

    stack = [ (x,y) ]

    while len(stack) > 0:
        (x,y) = stack.pop()
        result[y][x] = "#"

        for dx,dy in [ (-1,0), (1,0), (0,-1), (0,1) ]:
            if result[y+dy][x+dx] == ".":
                stack.append((x+dx,y+dy))

    return result


def part1(input: list[tuple[str,int,str]]):
    x,y=0,0

    diggy = set()
    #diggy.add((x,y))

    xmin,xmax,ymin,ymax = 0,0,0,0

    for (dir,dist,color) in input:
        match dir:
            case "U":
                delta = [ (0, i) for i in range(-1,-dist-1,-1) ]
            case "D":
                delta = [ (0, i) for i in range(1,dist+1) ]
            case "L":
                delta = [ (i, 0) for i in range(-1,-dist-1,-1) ]
            case "R":
                delta = [ (i, 0) for i in range(1,dist+1) ]
            case _:
                assert False, f"INVALID INPUT: dir: {dir} dist: {dist} color: {color}"

        for dx,dy in delta:
            digx,digy = x+dx,y+dy

            diggy.add((digx,digy))
        x,y = x+delta[-1][0], y+delta[-1][1]

        xmin = min(x,xmin)
        xmax = max(x,xmax)
        ymin = min(y,ymin)
        ymax = max(y,ymax)

    assert (0,0) in diggy

    #print(xmin,xmax,ymin,ymax)

    x_size = xmax-xmin+1
    y_size = ymax-ymin+1

    #Translate and make a grid
    grid = []
    for y in range(y_size):
        row = []
        for x in range(x_size):
            if (x+xmin,y+ymin) in diggy:
                c="#"
            else:
                c="."
            row.append(c)
        #print("".join(row))
        grid.append(row)

    #print()

    grid = floodfill(grid)

    #for row in grid:
    #    print("".join(row))

    #Count all filled
    sum = 0
    for row in grid:
        sum += row.count("#")

    return sum


def part2(input: list[tuple[str,int,str]], part2=False):
    dirs = {0: "R", 1: "D", 2: "L", 3: "U"}

    corners: list[tuple[int,int]] = [(0,0)]

    x,y=0,0

    length = 0

    for dir, dist, code in input:
        if part2:
            dist = int(code[0:5], 16)
            dir = dirs[int(code[5])]

        #print(f"#{code} = {dir} {dist}")

        length += dist

        match dir:
            case "U":
                y -= dist
            case "D":
                y += dist
            case "L":
                x -= dist
            case "R":
                x += dist
            case _:
                assert False

        corners.append((x,y))

    #print(length//2)

    #print(corners)

    #Do the weird area formula
    v1,v2 = 0,0
    for i in range(1, len(corners)):
        x0,y0 = corners[i-1]
        x1,y1 = corners[i]

        v1 += y1*x0
        v2 += y0*x1

    #Add length/2+1 to include the extra area of the circumference
    return (v1-v2)//2 + length//2 + 1


if __name__ == "__main__":
    input = readinput()

    data = []

    for row in input:
        (dir, dist, color) = row.split()

        dist = int(dist)
        color = color[2:-1]

        datta = (dir, dist, color)
        #print(datta)
        data.append(datta)

    p1 = part1(data)
    #p1 = part2(date) <- this alwo works
    print("Part 1:", p1)

    p2 = part2(data, True)
    print("Part 2:", p2)