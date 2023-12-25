#!/usr/bin/env python3

import functools
from functools import cache
from itertools import combinations
import itertools
import collections
from queue import PriorityQueue, SimpleQueue
import heapq
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Optional, Union

import math
import re
import sys


sys.path.append("../..")
from lib.aoc import *

def traversegrid(grid: list[str], startpos: Optional[tuple[int,int]]=None, maxsteps: int=-1) -> list[list[Union[int,None]]]:
    rocks: set[tuple[int,int]] = set()
    
    size_x = len(grid[0])
    size_y = len(grid)

    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            pos = (x,y)
            if tile == "#":
                rocks.add(pos)
            elif tile == "S" and startpos is None:
                startpos = pos

    assert startpos is not None

    distances: list[list[Union[int,None]]] = [ [None]*size_x for _ in range(size_y)]

    #We are already here
    #distances[startpos[1]][startpos[0]] = 0

    #Queue of positions for which to add neighbours for
    q = PriorityQueue()
    q.put((0, startpos))

    while not q.empty():
        dist, pos = q.get()

        (x,y) = pos

        #Someone has already been here
        if distances[y][x] is not None and distances[y][x] <= dist:
            continue

        #My score!
        distances[y][x] = dist

        #Enqueue all the valid neighbours
        newdist = dist+1
        if newdist > maxsteps:
            continue

        for (dx,dy) in [(-1,0), (1,0), (0,-1), (0,1)]:
            x1,y1 = (pos[0]+dx,pos[1]+dy)
            newpos = (x1,y1)

            #Skip rocks
            if newpos in rocks: continue
            
            #Don't go outside grid
            if x1 < 0 or x1 >= size_x: continue
            if y1 < 0 or y1 >= size_y: continue

            #Don't go to visited nodes
            if distances[y1][x1] is not None and distances[y1][x1] <= newdist: continue

            q.put((newdist, newpos))

    return distances

def countreachable(grid: list[str], n: int, startpos: Optional[tuple[int,int]]=None) -> int:
    result = traversegrid(grid, startpos, n)

    #Flatten list
    result = [d for row in result for d in row]

    #All squares that can be reached in <=n steps, and is same modulo 2, are reachable.
    valids = [d for d in result if d is not None and d<=n and d%2==n%2]

    return len(valids)

def part2(grid: list[str], steps):

    #Figure out how many reachable squares there are in a tile
    return ""


if __name__ == "__main__":
    grid = readinput()

    if len(grid) < 20:
        steps = 6
        p2_steps = [6, 10, 50, 100, 500, 1000, 5000]
    else:
        steps = 64
        p2_steps = [26501365]

    if len(sys.argv) >= 2:
        p2_steps = [int(sys.argv[1])]

    p1 = countreachable(grid, steps)
    print(f"Part 1 ({steps} steps):", p1)


    for steps in p2_steps:
        p2 = part2(grid, steps)
        print(f"Part 2 ({steps} steps):", p2)