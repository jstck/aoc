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


#Find two grid squares and return their manhattan distance
def manhattan(grid: Grid[str], a: str, b: str) -> int:
    x1,y1 = grid.findvalue(a).__next__()
    x2,y2 = grid.findvalue(b).__next__()

    return abs(x1-x2)+abs(y1-y2)

def part1(input: list[str]):

    keypad = Grid(["123", "456", "789", " 0A"])

    cur = "A"

    for line in input:
        seq = list(line.strip())
    return ""

def part2(input: list[str]):
    return ""


if __name__ == "__main__":
    input = readinput()

    p1 = part1(input)
    print("Part 1:", p1)

    p2 = part2(input)
    print("Part 2:", p2)
