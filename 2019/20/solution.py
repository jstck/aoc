#!/usr/bin/env python3
from __future__ import annotations

from functools import cache
from itertools import combinations, permutations
import collections
from queue import PriorityQueue, SimpleQueue
from collections import defaultdict, deque, Counter, OrderedDict
import heapq
from dataclasses import dataclass
import math
import re
import sys
from typing import TypeAlias, Optional

import math
import re
import sys


sys.path.append("../..")
from lib.aoc import *
from lib.grid import Grid

#Find the actual "target tile" for a label (a neighbouring ".")
def findtarget(grid, pos: tuple[int,int]) -> tuple[int,int]:
    x,y=pos
    for nx,ny,tile in grid.neighbours(x,y):
        if tile==".":
            return (nx,ny)

    assert False

#Check to see if a warpzone is close to the edge
def isEdgeWarp(grid, pos: tuple[int,int]) -> bool:
    size_x,size_y = grid.size_x,grid.size_y
    x,y=pos

    if x <=2: return True
    if x >= size_x-2: return True
    if y <=2: return True
    if y >= size_y-2: return True
    return False


def part1(input: list[str]):
    grid = Grid(input)
    
    warpzones: dict[str,list[tuple[int,int]]] = defaultdict(list)
    warps: dict[tuple[int,int],tuple[int,int]] = {}

    #Make a copy of original grid. Change all warpzone labels so both letters have the full label (for ease-of-traversing)
    for x,y,tile in grid.enumerate():
        if tile.isupper():
            label = None
            iswarpzone = False
            for nx,ny,n in grid.neighbours(x,y):
                
                if n.isupper():
                    dir = (x-nx) + (y-ny) #One is going to be zero, the other +/-1
                    if dir<0: #Neighbour is first letter
                        label = str(n[0]+tile)
                    else:   #Neighbour is second letter
                        label = str(tile+n[-1])
                if n==".":
                    iswarpzone = True
            
            if iswarpzone:
                assert label is not None
                warpzones[label].append((x,y))

    assert len(warpzones["AA"])==1
    assert len(warpzones["ZZ"])==1

    AA_pos = warpzones["AA"][0]
    startx,starty = findtarget(grid, AA_pos)
    finishpos = findtarget(grid, warpzones["ZZ"][0])

    del warpzones["AA"]
    del warpzones["ZZ"]

    for label, zones in warpzones.items():
        assert len(zones)==2, f"{label} has {len(zones)} positions: {str(zones)}"

        z1, z2 = zones

        warps[z1]=findtarget(grid,z2)
        warps[z2]=findtarget(grid,z1)

    #Queue on (distance,x,y)
    q: PriorityQueue[tuple[int,int,int]] = PriorityQueue()
    q.put((0,startx,starty))

    #Mark AA as visited to avoid going back there
    visited: set[tuple[int,int]] = set([AA_pos])

    while not q.empty():
        dist,x,y = q.get_nowait()
        if (x,y) in visited: continue
        visited.add((x,y))

        if (x,y) == finishpos:
            return dist
        
        for nx,ny,tile in grid.neighbours(x,y):
            if tile == "#":
                continue
            elif (nx,ny) in visited:
                continue
            elif tile == ".":
                q.put((dist+1,nx,ny))
            elif tile.isupper():
                #Warpzone
                assert (nx,ny) in warps, f"Warpzone not found for ({nx},{ny})"
                warpx,warpy = warps[(nx,ny)]
                q.put((dist+1,warpx,warpy))

    return -1










def part2(input: list[str]):
    grid = Grid(input)
    
    warpzones: dict[str,list[tuple[int,int]]] = defaultdict(list)
    warps: dict[tuple[int,int],tuple[int,int,int]] = {} #Third digit is "up/down in recursion"

    #Make a copy of original grid. Change all warpzone labels so both letters have the full label (for ease-of-traversing)
    for x,y,tile in grid.enumerate():
        if tile.isupper():
            label = None
            iswarpzone = False
            for nx,ny,n in grid.neighbours(x,y):
                
                if n.isupper():
                    dir = (x-nx) + (y-ny) #One is going to be zero, the other +/-1
                    if dir<0: #Neighbour is first letter
                        label = str(n[0]+tile)
                    else:   #Neighbour is second letter
                        label = str(tile+n[-1])
                if n==".":
                    iswarpzone = True
            
            if iswarpzone:
                assert label is not None
                warpzones[label].append((x,y))

    assert len(warpzones["AA"])==1
    assert len(warpzones["ZZ"])==1

    AA_pos = warpzones["AA"][0]
    startx,starty = findtarget(grid, AA_pos)
    startlevel = 0
    finishpos = findtarget(grid, warpzones["ZZ"][0]) + (0,)

    del warpzones["AA"]
    del warpzones["ZZ"]

    for label, zones in warpzones.items():
        assert len(zones)==2, f"{label} has {len(zones)} positions: {str(zones)}"

        z1, z2 = zones

        if isEdgeWarp(grid,z1):
            warps[z2]=findtarget(grid,z1) + (1,)  #Increase recursion level
            warps[z1]=findtarget(grid,z2) + (-1,) #Decrease recursion level
        elif isEdgeWarp(grid,z2):
            warps[z1]=findtarget(grid,z2) + (1,)  #Increase recursion level
            warps[z2]=findtarget(grid,z1) + (-1,) #Decrease recursion level
        else:
            assert False, f"Neither part of {str(z1)} and {str(z2)} are near the edge"

    #Queue on (metric,distance,recursion_level,x,y), metric being steps+level*10
    q: PriorityQueue[tuple[int,int,int,int,int]] = PriorityQueue()
    q.put((0,0,startlevel,startx,starty))

    visited: set[tuple[int,int,int]] = set()

    while not q.empty():
        _,dist,level,x,y = q.get_nowait()
        #print(f"Dist: {dist}, at {x},{y},{level}")
        if (x,y,level) in visited: continue
        visited.add((x,y,level))

        if (x,y,level) == finishpos:
            return dist
        
        for nx,ny,tile in grid.neighbours(x,y):
            if tile == "#":
                continue
            elif (nx,ny,level) in visited:
                continue
            elif tile == ".":
                q.put((dist+1+level*10,dist+1,level,nx,ny))
            elif tile.isupper():
                if tile=="AA" or tile=="A": continue #Don't go back into starting tile
                if tile=="ZZ" or tile=="Z":
                    print(f"Boop {tile} at {level}")
                    if level==0:
                        #Found goal!
                        return dist+1
                    else:
                        continue #Can't get into ZZ here
                
                #Warpzone
                assert (nx,ny) in warps, f"Warpzone not found for ({nx},{ny}), {tile}"
                warpx,warpy,warplevel = warps[(nx,ny)]
                nlevel=level+warplevel
                if nlevel<0: continue
                #if warplevel<0:
                #    print(f"Warping back to {nx},{ny},{level+warplevel}")
                if not (level+warplevel, warpx, warpy) in visited:
                    q.put((dist+1+nlevel*10,dist+1,nlevel,warpx,warpy))

    return -1



if __name__ == "__main__":
    input = [line.rstrip("\n") for line in sys.stdin.readlines()]

    p1 = part1(input)
    print("Part 1:", p1)

    p2 = part2(input)
    print("Part 2:", p2)