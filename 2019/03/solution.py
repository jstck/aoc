#!/usr/bin/env python3

import sys


sys.path.append("../..")
from lib.aoc import *

#sys.path.append("..")
#from intcode_vm import *


def parse_wire(wire: str) -> list[tuple[str,int]]:
    segments = []

    for seg in wire.strip().split(","):
        dir = seg[0]
        dist = int(seg[1:])
        segments.append((dir,dist))

    return segments


def trace_wire(wire: str) -> tuple[set,dict]:
    segments = parse_wire(wire)

    #Starting point
    x,y = 0,0

    #Set of x,y-tuples the wire passes through. Add initial point (as it isn't otherwise)
    points: set[tuple[int,int]] = set([(x,y)])

    #minimum number of steps to reach a certain point
    steps: dict[tuple[int,int],int] = {}

    nsteps = 0

    for (direction, distance) in segments:
        if direction == "U":
            for y1 in range(y+1,y+distance+1):
                p = (x,y1)
                points.add(p)
                nsteps += 1
                if not p in steps:
                    steps[p]=nsteps
            y = y + distance
        elif direction == "D":
            for y1 in range(y-1,y-distance-1,-1):
                p = (x,y1)
                points.add(p)
                nsteps += 1
                if not p in steps:
                    steps[p]=nsteps
            y = y - distance
        elif direction == "R":
            for x1 in range(x+1,x+distance+1):
                p = (x1,y)
                points.add(p)
                nsteps += 1
                if not p in steps:
                    steps[p]=nsteps
            x = x + distance
        elif direction == "L":
            for x1 in range(x-1,x-distance-1,-1):
                p = (x1,y)
                points.add(p)
                nsteps += 1
                if not p in steps:
                    steps[p]=nsteps
            x = x - distance
        else:
            print("INVALID DIRECTION:", direction)
            assert(False)

    return points, steps


def crosswires(wire1: str, wire2: str) -> tuple[int,int]:

    w1, steps1 = trace_wire(wire1)
    w2, steps2 = trace_wire(wire2)

    crossings = set.intersection(w1,w2)

    closest_crossing = 1000000
    fewest_steps = 1000000

    for c in crossings:
        #SKip the obvious starting point
        if c==(0,0):
            continue

        x,y = c
        manhattan = abs(x)+abs(y)

        closest_crossing = min(closest_crossing,manhattan)

        wire_length = steps1[c]+steps2[c]



        fewest_steps = min(fewest_steps,wire_length)

    return closest_crossing, fewest_steps


if __name__ == "__main__":
    input = readinput()

    for i in range(0, len(input), 2):
        wire1 = input[i]
        wire2 = input[i+1]

        p1,p2 = crosswires(wire1, wire2)
        print("Part 1: ",p1)
        print("Part 2: ",p2)
        print()
