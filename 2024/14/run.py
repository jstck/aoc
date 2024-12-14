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

@dataclass(frozen=True)
class Robot:
    px: int
    py: int
    vx: int
    vy: int
    sx: int
    sy: int

    def positionAt(self, t: int) -> tuple[int,int]:
        x = (self.px + self.vx*t) % self.sx
        y = (self.py + self.vy*t) % self.sy

        return (x,y)



sys.path.append("../..")
from lib.aoc import *

def quadrantScore(positions: list[tuple[int,int]], sx, sy) -> int:
    #Scores for each quadrant
    q1,q2,q3,q4 = 0,0,0,0

    #Midpoint is divided by two (the line on which bots don't count)
    midx = sx//2
    midy = sy//2

    for (x,y) in positions:
        if x>midx and y>midy:
            q1 += 1
        elif x<midx and y>midy:
            q2 += 1
        elif x<midx and y<midy:
            q3 += 1
        elif x>midx and y<midy:
            q4 += 1

    return q1*q2*q3*q4

def part1(bots: list[Robot]) -> int:

    positions = [bot.positionAt(100) for bot in bots]

    return quadrantScore(positions, bots[0].sx, bots[0].sy)

#A christmas tree is anything that is symmetric around the Y axis (at "mid X"). Turned ot not to be true.
def isChristmasTree(positions: list[tuple[int,int]], sizex: int, sizey: int) -> bool:
    #Sort positions into rows
    rows: dict[int,list[int]] = collections.defaultdict(list)

    midx = sizex//2

    for (x,y) in positions:
        rows[y].append(x)

    for y in range(sizey):
        row = set(rows[y])
        for x1 in range(midx):
            x2 = sizex-midx
            #A single cell of asymmetry detected = not a christmas tree
            if (x1 in row) != (x2 in row):
                return False

    return True


def printbots(positions: set[tuple[int,int]], sx, sy):
    for y in range(sy):
        row = []
        for x in range(sx):
            if (x,y) in positions:
                row.append("#")
            else:
                row.append(" ")
        print("".join(row))

def part2(bots: list[Robot]):
    t = 0

    sx = bots[0].sx
    sy = bots[1].sy

    while True:

        #Magic numbers determined by stepping through output and finding suspicious cyclic clumps of bots
        if (t-19)%103 != 0 or (t-70)%101 != 0:
            t+=1
            continue

        positions = [bot.positionAt(t) for bot in bots]

        printbots(set(positions), sx, sy)
        print()
        input(f"T={t}")
        t += 1
        if t%1000==0:
            print(t)


if __name__ == "__main__":
    fname = sys.argv[1]
    with open(fname, "r") as fp:
        data = readinput(fp)

    bots = []

    #Different sized grids for test and real deal
    if len(data) >= 100:
        size_x = 101
        size_y = 103
    else:
        size_x = 11
        size_y = 7


    for line in data:
        bits = re.findall(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
        px,py,vx,vy = map(int, bits[0])
        bot = Robot(px,py,vx,vy,size_x,size_y)
        bots.append(bot)

    p1 = part1(bots)
    print("Part 1:", p1)

    p2 = part2(bots)
    print("Part 2:", p2)
