#!/usr/bin/env python3

import sys

sys.path.append("../..")
from lib.aoc import *


def getcol(grid: list[str], i) -> str:
    assert(i < len(grid[0]))

    return "".join([row[i] for row in grid])

def transpose(grid: list[str]) -> list[str]:
    size_x = len(grid[0])
    return [getcol(grid, i) for i in range(size_x)]
    

def findmirror(grid: list[str], ignorescore: int=0) -> int:
    size = len(grid)

    #print("\n".join(grid))
    #print(size)
    #print()

    #Try mirroring at this row (rather "after grid[m]")
    for m in range(1, size):

        #Skip a specific reflection line (ignore part1 solution in part2)
        if m==ignorescore:
            continue

        tophalf = grid[:m]
        bottomhalf = grid[m:]
        tophalf.reverse()

        mirrorsize = min(len(tophalf), len(bottomhalf))
        assert(mirrorsize>0)
        tophalf = tophalf[:mirrorsize]
        bottomhalf = bottomhalf[:mirrorsize]

        assert(len(tophalf) == len(bottomhalf))

        match = True
        for i in range(len(tophalf)):
            if tophalf[i] != bottomhalf[i]:
                match = False
                break

        if match:
            return m

    #No reflection line found (in this direction at least)
    return 0

#Return a copy of a grid with one position flipped
def smudge(grid: list[str], x: int, y: int) -> list[str]:
    newgrid = []
    for iy, row in enumerate(grid):
        if iy == y:
            s = list(row)
            if s[x] == ".":
                s[x] = "#"
            elif s[x] == "#":
                s[x] = "."
            else:
                assert(False)
            newgrid.append("".join(s))
        else:
            newgrid.append(row)
    return newgrid

if __name__ == "__main__":
    input = chunks(readinput())

    sum = 0
    scores = []

    print(len(input), "grids")

    for grid in input:
        #size_x, size_y = len(grid[0]), len(grid)
        
        #print(f"{size_x} X {size_y}")

        m1 = findmirror(grid)
        m2 = findmirror(transpose(grid))

        score = 100*m1 + m2

        print(m1,m2,score)
        assert(score>0)
        assert(m1==0 or m2==0)

        sum += score
        scores.append(score)

    print("Part 1:", sum)



    sum = 0

    for i, grid in enumerate(input):
        oldscore = scores[i]
        
        size_x, size_y = len(grid[0]), len(grid)
        match = False

        for x in range(size_x):
            if match:
                break
            for y in range(size_y):
                newgrid = smudge(grid, x, y)

                ignore1 = oldscore // 100
                ignore2 = oldscore % 100
                m1 = findmirror(newgrid, ignore1)
                m2 = findmirror(transpose(newgrid), ignore2)

                if m1*100 == oldscore:
                    m1 = 0
                if m2 == oldscore:
                    m2 = 0

                newscore = 100*m1 + m2

                if newscore > 0 and newscore != oldscore:
                    #print(f"{i}: smudge at {x} {y} -> {newscore} (was {oldscore})")
                    assert(m1==0 or m2==0)
                    match = True
                    sum += newscore
                    break

        if not match:
            #This is not supposed to happen unless you make your own crappy input data.
            print(f"BROKEN MIRROR {i}, was {oldscore} ({size_x} X {size_y})")
            print("\n".join(grid))
            print()
            print("\n".join(transpose(grid)))

    print("Part 2:", sum)
