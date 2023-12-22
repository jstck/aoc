#!/usr/bin/env python3
from __future__ import annotations

from functools import cache
from itertools import combinations
import itertools
from collections import defaultdict, deque, Counter, OrderedDict
from queue import PriorityQueue, SimpleQueue
import heapq
from dataclasses import dataclass
from typing import TypeAlias

import math
import re
import sys

sys.path.append("../..")
from lib.aoc import *

def sortints(a,b):
    a = int(a)
    b = int(b)
    if a<=b:
        return (a,b)
    else:
        return (b,a)

class Brick:

    def __init__(self, label: str, data: str):
        self.label = label

        p1,p2 = data.strip().split("~")
        x1,y1,z1 = p1.split(",")
        x2,y2,z2 = p2.split(",")

        self.x1, self.x2 = sortints(x1,x2)
        self.y1, self.y2 = sortints(y1,y2)
        self.z1, self.z2 = sortints(z1,z2)

        assert self.x1 <= self.x2
        assert self.y1 <= self.y2
        assert self.z1 <= self.z2
        
    def space(self)->set[tuple[int,int,int]]:
        myspace = set()
        for x in range(self.x1, self.x2+1):
            for y in range(self.y1, self.y2+1):
                for z in range(self.z1, self.z2+1):
                    myspace.add((x,y,z))
        return myspace
    
    def bottom(self)->set[tuple[int,int]]:
        surface = set()
        for x in range(self.x1, self.x2+1):
            for y in range(self.y1, self.y2+1):
                surface.add((x,y))
        return surface
    
    def _sortscore(self) -> tuple[int,...]:
        return (self.z1, self.z2, self.x1, self.y1, self.x2, self.y2)
    
    def __lt__(self, other):
        return self._sortscore() < other._sortscore()
    
    def __str__(self):
        return f"{self.label}: Z {self.z1}-{self.z2}, X {self.x1}-{self.x2}, Y {self.y1}-{self.y2}"
    
    def __repr__(self):
        return str(self)

cascache: dict[str,set[str]] = {}
def cascade(bricks, brick: str, below: dict[str,set[str]], above: dict[str,set[str]]) -> set[str]:

    #if brick in cascache:
    #    return cascache[brick]

    fallen_bricks: set[str] = set([brick])

    q: PriorityQueue[tuple[int,str]] = PriorityQueue()
    q.put_nowait((bricks[brick].z2, brick))

    while not q.empty():
        _, b = q.get_nowait()

        candidates = above[b]
        for c, belows in below.items():
            #Bricks touching something that has fallen (but not fallen themselves yet)
            if c in candidates and c not in fallen_bricks:
                if len(belows.difference(fallen_bricks)) == 0: #No remaining supports
                    fallen_bricks.add(c)
                    if c in cascache:
                        fallen_bricks.update(cascache[c])
                    q.put_nowait((bricks[c].z2, c))

    #Start brick is not to be counted.
    fallen_bricks.remove(brick)

    cascache[brick] = fallen_bricks

    return fallen_bricks
    
#Return
def fallingbricks(bricks: list[Brick]) -> tuple[int,int]:

    allbricks = set()
    for brick in bricks:
        assert len(allbricks.intersection(brick.space())) == 0
        allbricks.update(brick.space())

    #Sort by z1, to start lowest first when packing
    bricks.sort()

    #for b in bricks:
    #    print(b)
    
    xmin = min([b.x1 for b in bricks])
    xmax = max([b.x2 for b in bricks])
    ymin = min([b.y1 for b in bricks])
    ymax = max([b.y2 for b in bricks])
    zmin = min([b.z1 for b in bricks])
    zmax = max([b.z2 for b in bricks])
    #print(f"X {xmin}-{xmax}, Y {ymin}-{ymax}, Z {zmin}-{zmax}")

    
    #For each brick, what stuff is above and below?
    bricks_above: defaultdict[str,set[str]] = defaultdict(set)
    bricks_below: defaultdict[str,set[str]] = defaultdict(set)

    #What is the "top brick" and height of each spot
    brickmap: dict[tuple[int,int],str] = {}
    heightmap: dict[tuple[int,int],int] = {}

    #Init maps because we need to iterate over all points in them
    for x in range(xmin,xmax+1):
        for y in range(ymin,ymax+1):
            heightmap[(x,y)] = 0
            brickmap[(x,y)] = "Ground"
    
    for brick in bricks:
        surface = brick.bottom()

        #Highest point of bricks under this one
        maxheight = max([height for pos, height in heightmap.items() if pos in surface])

        z1_new = maxheight+1

        #print(f"{brick.label} lands at {z1_new}")

        assert z1_new <= brick.z1
        dz = brick.z1 - z1_new
        brick.z1 = z1_new
        brick.z2 -= dz

        #All points where this brick is resting on something
        supports = { pos for pos, height in heightmap.items() if pos in surface and height==maxheight}
        #print("Points of support:", ", ".join([f"({p[0]}, {p[1]})" for p in supports]))
        
        #Bricks in those touching points
        supportbricks = { label for pos, label in brickmap.items() if pos in supports}

        #print(f"Bricks below {brick.label}: {', '.join(supportbricks)}")

        bricks_below[brick.label] = supportbricks

        #Mark all touching bricks this one is above it
        for s in supportbricks:
            bricks_above[s].add(brick.label)

        #Mark new height and top brick
        for pos in surface:
            heightmap[pos] = brick.z2
            brickmap[pos] = brick.label

    #Sort again, since some things can have fallen past others (matters for part2 speed if caching)
    bricks.sort()

    #print()
    #print("After packing:")
    #for b in bricks:
    #    print(f"{b}, above: {', '.join(bricks_above[b.label])}, below: {', '.join(bricks_below[b.label])}")

    disintegrate = 0

    for brick in bricks:
        can_disintegrate = True
        for above in bricks_above[brick.label]:
            if len(bricks_below[above])<2:
                can_disintegrate = False
                break

        if can_disintegrate:
            disintegrate += 1
            #print(f"Can disintegrate {brick.label}")

    totalfalling = 0

    #Reverse sort order and start from the top
    bricks.reverse()

    brickdict = {b.label: b for b in bricks}

    for b in bricks:
        fallen = cascade(brickdict, b.label, bricks_below, bricks_above)
        
        #print(f"Removing {b} cascades to {', '.join(fallen)}")

        totalfalling += len(fallen)


    return disintegrate, totalfalling

if __name__ == "__main__":
    input = readinput()

    bricks = []

    nbricks = len(input)

    for i, line in enumerate(input):
        if nbricks < 26: #Label bricks with letter if less than 26 in total
            label = chr(ord("A")+i)
        else: #Label with number
            label = str(i+1)
        brick = Brick(label, line)
        bricks.append(brick)

    p1, p2 = fallingbricks(bricks)
    print("Part 1:", p1)
    print("Part 2:", p2)