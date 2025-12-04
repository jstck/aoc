#!/usr/bin/env python3

import functools
from functools import cache
from itertools import combinations
import itertools
import collections
from queue import PriorityQueue
import heapq
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Union, Optional, TypeAlias, Iterator

import sys

sys.path.append("../..")
from lib.aoc import *
from lib.grid import Grid

Pos: TypeAlias = tuple[int,int]

def bfs(grid: Grid[str], start: Pos, end: Pos, limit=20000) -> int:
    q: PriorityQueue[tuple[int,Pos]] = PriorityQueue()
    q.put_nowait((0,start))

    visited: set[Pos] = set()

    while not q.empty():
        steps,pos = q.get_nowait()
        if pos in visited:
            continue

        if pos == end:
            return steps
        
        #If at limit (and not found the finish), don't bother going further
        if steps >= limit:
            return -1

        visited.add(pos)

        if grid[pos] == "#":
            continue

        for (x1,y1,s) in grid.neighbours(pos[0],pos[1]):
            if s!="#":
                q.put_nowait((steps+1,(x1,y1)))

    return -1

def neighdots(grid: Grid[str], x, y) -> int:
    c=0
    for _,_,s in grid.neighbours(x,y):
        if s != "#":
            c+=1
    return c

#For a cheat to be useful:
#   a single grid square not at the edge that is a # and has two or three non-# neighbours
# or
#   two adjacent grid squares (either not at edge) that are a #, each has at least one non-# neighbour
#   and those two neighbour .'s are not adjacent

def makecheats(grid: Grid[str]) -> Iterator[Grid[str]]:
    for x in range(1,grid.size_x-1):
        for y in range(1,grid.size_x-1):
            if grid[x,y] != "#":
                continue
            nd = neighdots(grid, x,y)
            if nd >=2 and nd <= 3:
                #Single-square cheat
                

def part1(grid: Grid[str]):
    startpos = list(grid.findvalue("S"))
    assert(len(startpos)==1)
    startpos = startpos[0]
    endpos = list(grid.findvalue("E"))
    assert(len(endpos)==1)
    endpos = endpos[0]

    baseline = bfs(grid,startpos,endpos)
    print("Baseline:", baseline)


    #Try all 1ps cheats
    for x in range(1,grid.size_x-1):
        for y in range(1,grid.size_x-1):
            if grid[x,y] == "#":
                newgrid = grid.copy()
                newgrid[x,y] = "."
                score = bfs(newgrid, startpos, endpos, baseline-100)
                if score > 0:
                    print(x,y,score)

    return ""

def part2(input: list[str]):
    return ""


if __name__ == "__main__":
    input = readinput()

    grid: Grid[str] = Grid(input)

    print(grid)

    p1 = part1(grid)
    print("Part 1:", p1)

    #p2 = part2(input)
    #print("Part 2:", p2)
