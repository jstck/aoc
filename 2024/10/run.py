#!/usr/bin/env python3

from typing import Optional

import sys


sys.path.append("../..")
from lib.aoc import *
from lib.grid import Grid

#Part 1 only checks "number of reachable 9:s", so don't check any square more than once
#Part 2 checks for "number of different paths to 9:s", so just skip the "visited" check

def score(x: int, y: int, g: Grid[int], visited: Optional[set[tuple[int,int]]]) -> int:
    if visited is not None:
        if (x,y) in visited:
            return 0
        visited.add((x,y))

    c = g[x,y]    
    if c==9:
        return 1
    s=0
    for x1, y1, c1 in g.neighbours(x,y):
        if c1 == c+1:
            s += score(x1,y1,g, visited)
    return s


def part1(input: Grid):

    sum = 0

    for x, y in input.findvalue(0):
        visited = set()
        s = score(x,y,input, visited)
        sum += s
        print(x,y,s)

    return sum

def part2(input: Grid):

    sum = 0

    for x, y in input.findvalue(0):
        s = score(x,y,input, None)
        sum += s
        print(x,y,s)

    return sum

def intalize(input: list[str]):
    for row in input:
        yield map(int, list(row))

if __name__ == "__main__":
    input: Grid[int] = Grid(intalize(readinput()))

    print(input)

    p1 = part1(input)
    print("Part 1:", p1)

    p2 = part2(input)
    print("Part 2:", p2)
