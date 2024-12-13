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
from lib.sparsegrid import SparseGrid

#Simple recursive floodfill
def floodfill(grid: Grid[str],x: int, y: int, visited: set[tuple[int,int]]) -> set[tuple[int,int]]:
    visited.add((x,y))
    c = grid[x,y]
    for x1,y1,c1 in grid.neighbours(x,y):
        if c1==c and (x1,y1) not in visited:
            visited.update(floodfill(grid,x1,y1,visited))

    return visited

#Turn it into a SparseGrid just because of the neighbours function...
def makeRegion(grid: Grid[str], x: int, y: int) -> SparseGrid[str]:
    c = grid[x,y]
    result = SparseGrid([((x,y),grid[x,y])])

    points = floodfill(grid,x,y,set())
    result.data.update([((x1,y1),c) for (x1,y1) in points])    

    return result

#To find the perimeter length of a contiguous area, go through all points in that area and count how
#many neighbours there are not part of the area. A neighbour cell can be counted multiple times,
#since it can border many cells in the area.
def perimeter(region: SparseGrid[str]) -> int:
    p=0
    for pos in region.keys():
        for pos1 in region.neighbourPos(pos):
            if pos1 not in region:
                p+=1
    return p

def edges(region: SparseGrid[str], sx: int, sy: int) -> int:

    edges = 0

    prevrow = [0] * (sx+1) #From -1 to sx, cells are actually 0 to sx-1 but we need "one more"
    for y in range(0, sy+1): #One extra row
        rowness = []
        for x in range(-1, sx+1):
            rowness.append(1 if (x,y) in region else 0)
        diff = [a-b for (a,b) in zip (prevrow, rowness)]

        #Dedup diff
        transitions = [0]
        prev = 0
        for i in diff:
            if i != prev:
                transitions.append(i)
            prev = i
        transitions = [i for i in transitions if i != 0]

        e = len(transitions)
        #if e > 0:
        #    print(f"Region has {e} edges above row {y}")
        #    print(diff)
        #    print(transitions)

        edges += e
        prevrow = rowness

    prevcol = [0] * (sy+1) #From -1 to sx, cells are actually 0 to sx-1 but we need "one more"
    for x in range(0, sx+1): #One extra row
        colness = []
        for y in range(-1, sy+1):
            colness.append(1 if (x,y) in region else 0)
        diff = [a-b for (a,b) in zip (prevcol, colness)]

        #Dedup diff
        transitions = []
        prev = 0
        for i in diff:
            if i != prev:
                transitions.append(i)
            prev = i
        transitions = [i for i in transitions if i != 0]

        e = len(transitions)
        #if e > 0:
        #    print(f"Region has {e} edges to the left of col {x}")
        #    print(diff)
        #    print(transitions)

        edges += e
        prevcol = colness


    return edges

        




    return edges

def part1(grid: Grid[str]):
    #All nodes visited so far
    visited: Set[tuple[int,int]] = set()

    sum = 0
    sum2 = 0
    for x,y,c in grid.enumerate():
        if (x,y) not in visited:
            region = makeRegion(grid,x,y)
            visited.update(region.keys())

            p = perimeter(region)
            
            area = len(region.data)
            cost = p*area
            
            e = edges(region, grid.size_x, grid.size_y)
            cost2 = e*area
            
            print(f"Area with {c} at {x},{y}: size {area} perimeter {p} cost1 {cost} edges {e} cost2 {cost2}")
            sum += cost
            sum2 += cost2    

    return (sum,sum2)

def part2(input: list[str]):
    return ""


if __name__ == "__main__":
    g = Grid(readinput())

    p1 = part1(g)
    print("Part 1:", p1)

    p2 = part2(input)
    print("Part 2:", p2)
