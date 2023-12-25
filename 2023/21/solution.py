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
import numpy as np


sys.path.append("../..")
from lib.aoc import *

def traversegrid(grid: list[str], startpos: Optional[tuple[int,int]]=None, maxsteps: int=-1, tiling=False) -> dict[tuple[int,int],int]:
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

    distances: dict[tuple[int,int],int] = {}

    #We are already here
    #distances[startpos[1]][startpos[0]] = 0

    #Queue of positions for which to add neighbours for
    q = PriorityQueue()
    q.put((0, startpos))

    while not q.empty():
        dist, pos = q.get()

        (x,y) = pos

        #Someone has already been here
        if pos in distances and distances[pos] <= dist:
            continue

        #My score!
        distances[pos] = dist

        #Enqueue all the valid neighbours
        newdist = dist+1
        if newdist > maxsteps:
            continue

        for (dx,dy) in [(-1,0), (1,0), (0,-1), (0,1)]:
            x1,y1 = (pos[0]+dx,pos[1]+dy)
            newpos = (x1,y1)
            
            if not tiling:
                #Don't go outside grid
                if x1 < 0 or x1 >= size_x: continue
                if y1 < 0 or y1 >= size_y: continue
                rockpos = (x1,y1)
            else:
                #Wrap around
                mapx = x1 % size_x
                mapy = y1 % size_y
                rockpos = (mapx,mapy)

            #Skip rocks
            if rockpos in rocks: continue

            #Don't go to visited nodes
            if newpos in distances and distances[newpos] <= newdist: continue

            q.put((newdist, newpos))

    return distances

def countreachable(grid: list[str], n: int, startpos: Optional[tuple[int,int]]=None, tiling=False) -> int:
    result = traversegrid(grid, startpos, n, tiling)

    #All squares that can be reached in <=n steps, and is same modulo 2, are reachable.
    valids = [d for d in result.values() if d is not None and d<=n and d%2==n%2]

    return len(valids)

def polyval(x: int,z: np.ndarray):
    return z[0] * x**2 + z[1]*x + z[2]


if __name__ == "__main__":
    grid = readinput()

    if len(grid) < 20:
        p1_steps = 6
        total_steps = 5000
    else:
        p1_steps = 64
        total_steps = 26501365

    p1 = countreachable(grid, p1_steps)
    print(f"Part 1 ({p1_steps} steps):", p1)
    print()


    tile_size = len(grid)
    assert tile_size%2==1 #We only comprehend odd grid sizes today

    steps_to_edge = tile_size//2

    #Do two tiles per cycle, since they're alternating "odd/even" (uneven-length checkerboard pattern)
    cycle_length = tile_size*2

    final_steps = (total_steps-steps_to_edge)%cycle_length

    cycles = (total_steps-steps_to_edge) // cycle_length

    print("Initial steps:", steps_to_edge)
    print(f"Cycles @ {cycle_length} steps: {cycles}")
    print("Final steps:", final_steps)
    assert steps_to_edge + cycles*cycle_length + final_steps == total_steps

    p2_steps = []
    x = []
    y = []
    nsteps = []
    for count in [2, 3, 4]:
        steps = steps_to_edge + count*cycle_length + final_steps
        result = countreachable(grid, steps, None, True)
        print(steps,result)
        x.append(steps)
        y.append(result)

    #Difference between the steps
    d1 = [y[1]-y[0],y[2]-y[1]]

    #Increase in difference each step. This is a constant number.
    diff = d1[1]-d1[0]

    print("2nd order difference: ", diff)

    #Just count our way up, less math. Start at the "4 cycles" point
    tiles = y[2]
    steps = x[2]
    delta = d1[1]
    cycles = 4

    while True:
        delta += diff
        tiles += delta
        steps += cycle_length
        cycles += 1
        if steps >= total_steps:
            break

    print("Cycles:", cycles)
    print("Steps:", steps)
    print("Tiles:", tiles, " <-------")


    z = np.polyfit(x, y, 2)
    poly = np.poly1d(z)

    for steps, tiles in zip(x,y):
        print(steps, poly(steps), tiles)

    print("Polynomial thing:", poly(total_steps))



