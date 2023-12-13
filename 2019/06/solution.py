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

#sys.path.append("..")
#from intcode_vm import *

def part1(input: list[str]):
    return ""

def part2(input: list[str]):
    return ""

#Recursively calculate all depths of sub-satellites
def calcsats(depths, satellites, thing):
    mydepth = depths[thing]
    for sat in satellites[thing]:
        depths[sat] = mydepth+1
        calcsats(depths, satellites, sat)

#Get ordered list of parent objects
def parentlist(parents, thing):
    if not thing in parents:
        return []
    
    p = parents[thing]

    return [p] + parentlist(parents, p)


if __name__ == "__main__":
    input = readinput()

    satellites = collections.defaultdict(list)
    parents = {}

    for orbit in input:
        a,b = orbit.split(")")
        satellites[a].append(b)
        parents[b] = a

    depths = {"COM": 0}
    calcsats(depths, satellites, "COM")

    p1 = sum(depths.values())

    print("Part 1:", p1)

    if not "YOU" in satellites or not "SAN" in satellites:
        print("No part 2 in this data")
        sys.exit(0)

    you = parentlist(parents, "YOU")
    san = parentlist(parents, "SAN")

    #print(you)
    #print(san)

    while len(you)>0 and len(san)>0 and you[-1] == san[-1]:
        a = you.pop()
        b = san.pop()
        #print(f"{a}=={b}")

    #print(you)
    #print(san)

    p2 = len(you)+len(san) #Their last common object (last thing popped) is +1, but you's current parent is -1
    print("Part 2:", p2)
