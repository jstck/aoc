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

Body: TypeAlias = tuple[int,int,int,int,int,int]

def energy(system: tuple[Body,...]) -> int:
    e = 0

    for body in system:
        x,y,z,vx,vy,vz = map(abs,body)
        e += (x+y+z)*(vx+vy+vz)

    return e

def pull(p1: int, p2: int) -> int:
    if p2>p1:
        return 1
    if p2<p1:
        return -1
    return 0

def updatesystem(system: tuple[Body,...]) -> tuple[Body,...]:
    newsystem: list[Body] = []
    for i, b1 in enumerate(system):
        ddx,ddy,ddz=0,0,0
        x1,y1,z1,vx,vy,vz = b1
        for j, b2 in enumerate(system):
            if i==j: continue
            x2,y2,z2,_,_,_ = b2

            ddx += pull(x1,x2)
            ddy += pull(y1,y2)
            ddz += pull(z1,z2)

        #Update velocity
        vx += ddx
        vy += ddy
        vz += ddz

        #Move
        x1 += vx
        y1 += vy
        z1 += vz

        newbody: Body = (x1,y1,z1,vx,vy,vz)
        newsystem.append(newbody)
    
    return tuple(newsystem)

def str3d(x: int, y: int, z: int) -> str:
    return f"<x={x:3}, y={y:3}, z={z:3}>"

def printsystem(system: tuple[Body,...], iter: int):
    print(f"After {iter} steps:")
    for body in system:
        x,y,z,vx,vy,vz = body
        print(f"pos={str3d(x,y,z)}, vel={str3d(vx,vy,vz)}")
    print()


def part1(system: tuple[Body,...], iterations: int) -> int:
    i=0
    #printsteps = iterations//10
    #printsystem(system, i)

    while True:
        i += 1
        system = updatesystem(system)
        #if i%printsteps==0 or i==iterations:
        #    printsystem(system, i)

        if i>=iterations: break
        
    return energy(system)
    

def part2(system: tuple[Body,...]) -> int:

    i=0

    states: dict[tuple[Body,...],int] = {system: i}

    bodystates: list[dict[Body,int]] = []

    for b, body in enumerate(system):
        bodystates.append({body: i})

    found: set[int] = set()

    while True:
        system = updatesystem(system)
        i += 1

        for b, body in enumerate(system):
            if body in bodystates[b] and not b in found:
                found.add(b)
                print(f"Cycle for body {b} between {bodystates[b][body]} and {i}")
                if len(found) == len(system):
                    return i
            else:
                bodystates[b][body] = i
                

        #if system in states:
        #    print(f"Cycle between {states[system]} and {i}")
        #    return i


if __name__ == "__main__":
    system = []
    for chunk in chunks(readinput()):
        iterations = int(chunk[0])
        system: list[Body] = []
        for line in chunk[1:]:
            matches = re.match('<x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)>',line.strip())
            assert matches is not None
            x = int(matches.groups(0)[0])
            y = int(matches.groups(0)[1])
            z = int(matches.groups(0)[2])

            body: Body = (x,y,z,0,0,0)
            system.append(body)

        p1 = part1(tuple(system), iterations)
        print("Part 1:", p1)


        p2 = part2(tuple(system))
    #print("Part 2:", p2)