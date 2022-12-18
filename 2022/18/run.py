#!/usr/bin/env python3

import sys
import argparse
import re
import functools
import itertools
import collections
from queue import PriorityQueue, Queue
import heapq
from dataclasses import dataclass
import math

match = re.search(r'aoc/?(\d+)/(\d+)', __file__)
if match:
    descr = "Advent of Code " + match.group(1) + ":" + match.group(2)
else:
    descr = "Advent of some kind of Code"

parser = argparse.ArgumentParser(description = descr)

parser.add_argument('-1', action='store_true', help="Do part 1")
parser.add_argument('-2', action='store_true', help="Do part 2")
parser.add_argument('-t', action='store_true', help="Run tests")
parser.add_argument('-f', '--input-file', default='input.txt')
parser.add_argument('--verbose', '-v', action='count', default=0, help="Increase verbosity")

args = parser.parse_args()

tests = vars(args)["t"]
run2 = vars(args)["2"]
run1 = vars(args)["1"] or not run2 #Do part 1 if nothing else specified
verbosity = vars(args)["verbose"]
input_file = vars(args)["input_file"]


#Print controlled by verbosity level
def vprint(*args) -> None:
    if args[0]<= verbosity:
        print(*args[1:])

def chunks(input: list[str], ints: bool=False) -> list[list[str]]:
    chunk = []
    chunky = []
    for line in input:
        if len(line) == 0:
            chunky.append(chunk)
            chunk = []
        else:
            if ints:
                chunk.append(int(line))
            else:
                chunk.append(line)

    if len(chunk)>0:
        chunky.append(chunk)
    return chunky



test_cases = [
    {
        "input": """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""",
        "output": 64,
        "output2": 58
    }
]


def parse(input) -> set:
    s = set()

    for p in input:
        t = tuple([int(x) for x in p.strip().split(",")])
        s.add(t)

    return s


def allneighbours(p):
    (x, y, z) = p

    deltas = [
        [-1, 0, 0],
        [1, 0, 0],
        [0, -1, 0],
        [0, 1, 0],
        [0, 0, -1],
        [0, 0, 1],
    ]

    for (dx, dy, dz) in deltas:
        yield (x+dx, y+dy, z+dz)

def countneighbours(p, points):

    neighbours = 0

    for pn in allneighbours(p):
        if pn in points:
            neighbours += 1

    return neighbours

def part1(input: list[str]):
    points = parse(input)
    
    area = 0

    for p in points:
        a = 6 - countneighbours(p, points)
        print(p, a)
        area += a

    return area

def part2t(input: list[str]):
    points = parse(input)
    
    area = 0

    for p in points:
        a = 6 - countneighbours(p, points)
        print(p, a)
        area += a

    surfaces = set()

    for p in points:
        for pn in allneighbours(p):
            if pn not in points:
                surfaces.add(pn)

    for pn in surfaces:
        if countneighbours(pn, points) == 6:
            print("Air bubble at",pn)
            area -= 6

    return area


def part2(input: list[str]):
    cubes = parse(input)
    
    #Find bounds
    xmin, ymin, zmin, xmax, ymax, zmax = None, None, None, None, None, None

    for p in cubes:
        (x,y,z) = p
        if xmin is None or xmin>x: xmin = x
        if ymin is None or ymin>y: ymin = y
        if zmin is None or zmin>z: zmin = z
        if xmax is None or xmax<x: xmax = x
        if ymax is None or ymax<y: ymax = y
        if zmax is None or zmax<z: zmax = z

    #Go one step outside so leave room to fill outside all surfaces
    xmin -=1
    ymin -=1
    zmin -=1
    xmax += 1
    ymax += 1
    zmax += 1

    spaaace = set()

    q = Queue(0)

    p0 = (xmin, ymin, zmin)

    q.put(p0)

    print("BOUNDS: ",xmin, xmax, ymin, ymax, zmin, zmax)

    while not q.empty():
        p = q.get()

        #Throw away points out of bounds
        (x,y,z) = p
        if x<xmin or x>xmax or y<ymin or y>ymax or z<zmin or z>zmax: continue

        #Skip duplicates
        if p in spaaace: continue

        spaaace.add(p)

        for pn in allneighbours(p):
            if pn not in cubes:
                q.put(pn)

    area = 0
    for p in cubes:
        assert p not in spaaace
        a = countneighbours(p, spaaace)
        area += a

    return area



def fixInput(raw: str) -> list[str]:
    lines = [x.strip() for x in raw.split("\n")]

    #Remove trailing blank lines
    while len(lines[-1])==0:
        lines.pop()
    return lines

if tests:

    success = True

    for case in test_cases:
        rawinput = case["input"]

        match = re.search(r'^FILE:([\S]+)$', rawinput.strip())
        if match:
            filename = match.group(1)
            print("Loading", filename)
            with open(filename, "r") as fp:
                rawinput = fp.read()

        input = fixInput(rawinput.strip())
        

        if run1 and "output" in case and case["output"] is not None:
            output = part1(input)
            if output != case["output"]:
                print(f"Test part 1failed for input:\n====\n{case['input'].strip()}\n====\n.\n\nGot:\n{output}\n\nExpected:\n{case['output']}\n")
                success = False

        if run2 and "output2" in case and case["output2"] is not None:
            output = part2(input)
            if output != case["output2"]:
                print(f"Test part 2 failed for input:\n====\n{case['input'].strip()}\n====\nGot:\n{output}\n\nExpected:\n{case['output2']}\n")
                success = False

    if success:
        print("All tests passed successfully!")

else:
    try:
        fp = open(input_file, "r")
    except FileNotFoundError:
        print("Input file not found, using stdin")
        fp = sys.stdin
    
    input = fixInput(fp.read())

    if run1:
        print("Running part 1")
        result1 = part1(input)
    if run2:
        print("Running part 2")
        result2 = part2(input)

    print()

    if run1:
        print("PART 1")
        print("======")
        print(result1)

    if run1 and run2:
        print()

    if run2:
        print("PART 2")
        print("======")
        print(result2)