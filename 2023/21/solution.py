#!/usr/bin/env python3

import functools
from functools import cache
from itertools import combinations
import itertools
import collections
from queue import PriorityQueue
import heapq
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

import math
import re
import sys


sys.path.append("../..")
from lib.aoc import *


def part1(grid: list[str], steps) -> int:
    rocks: set[tuple[int,int]] = set()
    startpos = (-5,-5)

    size_x = len(grid[0])
    size_y = len(grid)

    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            pos = (x,y)
            if tile == "#":
                rocks.add(pos)
            elif tile == "S":
                startpos = pos

    print(f"Grid is {size_x} X {size_y}, {len(rocks)} rocks, doing {steps} steps from {str(startpos)}")

    positions = set([startpos])

    for step in range(steps):
        newpositions = set()

        for pos in positions:
            for (dx,dy) in [(-1,0), (1,0), (0,-1), (0,1)]:
                x1,y1 = (pos[0]+dx,pos[1]+dy)
                if x1 < 0 or x1 >= size_x:
                    continue
                if y1 < 0 or y1 >= size_y:
                    continue
                
                newpos = (x1,y1)
                if not newpos in rocks:
                    newpositions.add(newpos)
        positions = newpositions
        print(f"{step+1} steps: {len(positions)}")

    return len(positions)


def part2(input: list[str]):
    return ""


if __name__ == "__main__":
    grid = readinput()

    if len(grid) < 20:
        steps = 6
    else:
        steps = 64

    p1 = part1(grid, steps)
    print("Part 1:", p1)

    p2 = part2(input)
    print("Part 2:", p2)