#!/usr/bin/env python3

import itertools
import collections
from typing import Dict, List, Set, TypeAlias
import sys

sys.path.append("../..")
from lib.aoc import *
from lib.grid import Grid

Pos: TypeAlias = tuple[int,int]

def inbounds(p: Pos, sizeX: int, sizeY: int) -> bool:
    return p[0] >= 0 and p[1] >= 0 and p[0] < sizeX and p[1] < sizeY

def part1(ants: Dict[str,List[Pos]], sizeX: int, sizeY: int) -> int:
    antinodes: Set[Pos] = set()

    for f, positions in ants.items():
        #All pairs of antennas for a frequency
        for p1, p2 in itertools.combinations(positions, 2):
            dx, dy = p1[0]-p2[0],p1[1]-p2[1]

            #Two new positions one hop away in either direction
            n1: Pos = p1[0]+dx,p1[1]+dy
            n2: Pos = p2[0]-dx,p2[1]-dy

            if inbounds(n1, sizeX, sizeY) and not n1 in positions: antinodes.add(n1)
            if inbounds(n2, sizeX, sizeY) and not n1 in positions: antinodes.add(n2)

    return len(antinodes)

def part2(ants: Dict[str,List[Pos]], sizeX: int, sizeY: int) -> int:
    antinodes: Set[Pos] = set()

    for f, positions in ants.items():
        #All pairs of antennas for a frequency
        for p1, p2 in itertools.combinations(positions, 2):
            dx, dy = p1[0]-p2[0],p1[1]-p2[1]

            #Go in either direction direction (p1+, p2-)
            while inbounds(p1, sizeX, sizeY):
                antinodes.add(p1)
                p1 = p1[0]+dx,p1[1]+dy
            while inbounds(p2, sizeX, sizeY):
                antinodes.add(p2)
                p2 = p2[0]-dx,p2[1]-dy

    return len(antinodes)
if __name__ == "__main__":
    g: Grid[str] = Grid(readinput())

    ants: Dict[str,List[Pos]] = collections.defaultdict(list)

    for x,y, f in g.enumerate():
        if f != ".":
            ants[f].append((x,y))

    p1 = part1(ants, g.size_x, g.size_y)
    print("Part 1:", p1)

    p2 = part2(ants, g.size_x, g.size_y)
    print("Part 2:", p2)
