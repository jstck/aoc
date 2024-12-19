#!/usr/bin/env python3

import functools
from functools import cache
from itertools import combinations
import itertools
import collections
from queue import PriorityQueue
import heapq
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Union, Optional

import math
import re
import sys


sys.path.append("../..")
from lib.aoc import *
from lib.grid import Grid

def bfs(grid: Grid[str]) -> int:
    q: PriorityQueue[tuple[int,int,int]] = PriorityQueue()
    q.put_nowait((0,0,0))

    visited: set[tuple[int,int]] = set()

    while not q.empty():
        steps,x,y = q.get_nowait()
        if (x,y) in visited:
            continue

        visited.add((x,y))

        if (x,y) == (grid.size_x-1,grid.size_y-1):
            return steps

        if grid[x,y] == "#":
            continue

        for (x1,y1,s) in grid.neighbours(x,y):
            if s==".":
                q.put_nowait((steps+1,x1,y1))

    return -1

#Plain old BFS
def part1(input: list[tuple[int,...]]) -> int:
    if len(input) < 100:
        size = 6
        limit = 12
    else:
        size = 70
        limit = 1024

    c = 0

    grid: Grid[str] = Grid([["." for _ in range(size+1)] for _ in range(size+1)])

    for line in input:
        x,y = line
        grid[x,y] = "#"

        c+=1

        if c >= limit:
            break

    print(grid)
    return bfs(grid)

#Something not bfs (A* or dijkstra or something) would work better here since
#there are a lot of equal ways to get to every cell that have to be searched
#and it is rather slow
def part2(input: list[tuple[int,...]]) -> tuple[int,int]:
    if len(input) < 100:
        size = 6
    else:
        size = 70

    c = 0

    grid: Grid[str] = Grid([["." for _ in range(size+1)] for _ in range(size+1)])

    for line in input:
        #Just add one cell at a time until bfs fails
        x,y = line
        grid[x,y] = "#"

        c+=1

        path = bfs(grid)
        if path < 0:
            return (x,y)
        
        #print(f"Added ({x},{y}) -> {path} steps, {c} cells")

    return (-1,-1)

if __name__ == "__main__":
    input = list([tuple(map(int, line.split(",",2))) for line in readinput()])

    p1 = part1(input)
    p2 = part2(input)
    print("Part 1:", p1)
    print("Part 2:", ",".join(map(str,p2)))
