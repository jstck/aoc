#!/usr/bin/env python3
from __future__ import annotations

import sys
sys.path.append("../..")
from lib.aoc import *
from lib.grid import Grid

def countxmas(input: str) -> int:
    return input.count("XMAS") + input[::-1].count("XMAS")

def part1(input: list[str]) -> int:
    grid = Grid(input)

    count = 0

    #Iterate over all rows and columns
    for r in range(grid.size_y):
        count += countxmas("".join(grid.row(r)))

    for c in range(grid.size_x):
        count += countxmas("".join(grid.col(c)))
    
    #All the diagonals
    #Along left edge and down
    for y0 in range(grid.size_y):
        d = []
        for x in range(grid.size_x):
            y = y0 + x
            if x>=grid.size_x or y>=grid.size_y or x<0 or y<0:
                break
            d.append(grid[x,y])
        count += countxmas("".join(d))

    #Along top edge and right (skip first, we've done that)
    for x0 in range(1, grid.size_x):
        d = []
        for y in range(grid.size_y):
            x = x0 + y
            if x>=grid.size_x or y>=grid.size_y or x<0 or y<0:
                break
            d.append(grid[x,y])
        count += countxmas("".join(d))
    

    #Along left edge and up
    for y0 in range(grid.size_y):
        d = []
        for x in range(grid.size_x):
            y = y0 - x
            if x>=grid.size_x or y>=grid.size_y or x<0 or y<0:
                break
            d.append(grid[x,y])
        count += countxmas("".join(d))

    #Along bottom edge and up  (skip first, we've done that)
    for x0 in range(1, grid.size_x):
        d = []
        for i in range(grid.size_y):
            x = x0 + i
            y = grid.size_y - i - 1
            if x>=grid.size_x or y>=grid.size_y or x<0 or y<0:
                break
            d.append(grid[x,y])
        count += countxmas("".join(d))


    return count

def part2(input: list[str]) -> int:

    grid = Grid(input)
    
    count = 0
    #Go through all positions that aren't edge, look for an "A"
    #
    # Then look at the corners:
    # a b
    #  A
    # c d
    # It's what we're looking for if abcd are all M and S, and a!=d and b!=c

    for y in range(1, grid.size_y-1):
        for x in range(1, grid.size_x-1):
            if grid[x,y] != "A":
                continue
            a = grid[x-1,y-1]
            if a not in ["M", "S"]:
                continue
            b = grid[x+1,y-1]
            if b not in ["M", "S"]:
                continue
            c = grid[x-1,y+1]
            if c not in ["M", "S"]:
                continue
            d = grid[x+1,y+1]
            if d not in ["M", "S"]:
                continue

            if a==d:
                continue

            if b==c:
                continue

            #print("hit at",x,y)
            count += 1

    return count
            

if __name__ == "__main__":

    for chunk in chunks(readinput()):
        
        p1 = part1(chunk)
        print("Part 1:", p1)
        print()


        p2 = part2(chunk)
        print("Part 2:", p2)
        print()