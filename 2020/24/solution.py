#!/usr/bin/env python3

import sys
import re
from collections import defaultdict

def hexstep(x: int, y: int, step: str) -> tuple[int,int]:
    if step == "w":
        (x,y) = (x-1,y)
    elif step == "e":
        (x,y) = (x+1,y)
    elif step == "nw":
        (x,y) = (x-1,y+1)
    elif step == "ne":
        (x,y) = (x,y+1)
    elif step == "sw":
        (x,y) = (x,y-1)
    elif step == "se":
        (x,y) = (x+1,y-1)
    else:
        print(f"INVALID STEP: {step}")
        sys.exit(1)

    return (x,y)

def allneighbours(x,y) -> list[tuple[int,int]]:
    neighbours = []
    for step in ["e","ne","nw","w","sw","se"]:
        neighbours.append(hexstep(x,y,step))
    return neighbours


def part1(paths: list[list[str]]):

    tiles: defaultdict[tuple[int,int], int] = defaultdict(lambda: 0)

    for path in paths:
        (x,y) = (0,0)

        for step in path:
            (x,y) = hexstep(x,y,step)
        tiles[(x,y)] += 1
            
                
    white = black = 0

    for (x,y), c in tiles.items():
        #print(f"X{x:2} Y{y:2} : {c}")
        if c%2==1:
            black +=1
        else:
            white += 1

    print(f"Black: {black}, white: {white}")

    return black, tiles


def part2(tiles: dict) -> int:

    blacks = 0

    for day in range(100):

        makeblack= set()
        makewhite = set()
        newneighbours = set()

        for (x,y), c in tiles.items():
            #Count black neighbours, and make sure they exist in dict
            count = 0
            for n in allneighbours(x,y):
                if n in tiles:
                    count += tiles[n]%2
                else:
                    newneighbours.add(n)

            if c%2 == 1:
                if count == 0 or count > 2:
                    makewhite.add((x,y))
            else:
                if count == 2:
                    makeblack.add((x,y))

        #Go through all "new neighbours". These are all white to begin with
        for t in newneighbours:
            (x,y) = t
            count = 0
            for n in allneighbours(x,y):
                if n in tiles:
                    count += tiles[n]%2

            if count == 2:
                makeblack.add(t)

        for t in makeblack:
            tiles[t] = 1

        for t in makewhite:
            tiles[t] = 0

        blacks = 0
        whites = 0
        for t,c in tiles.items():
            if c%2==1:
                blacks += 1
            else:
                whites += 1

        if day < 10 or (day+1)%10==0:
            print(f"Day {day+1}: {blacks} black, {whites} white")

    return blacks



if __name__ == "__main__":
    paths = []
    for line in sys.stdin.readlines():
        line = line.strip()

        path = re.findall("([ns]?[ew])", line)
        assert(len(path)>0)

        paths.append(path)

    part1_black, state = part1(paths)

    #Copy all the tiles to a normal dict because easier
    p2_tiles = {k:(c%2) for k, c in state.items()}

    part2_black = part2(p2_tiles)

    print("Part1: ",part1_black)

    print("Part2:", part2_black)