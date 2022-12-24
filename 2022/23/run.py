#!/usr/bin/env python3

import sys
import argparse
import re
import functools
import itertools
import collections
from queue import PriorityQueue
import heapq
from dataclasses import dataclass
import math
from grid import Grid

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
..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............""",
        "output": 110,
        "output2": 20
    }
]

def parsemap(input: list[str], buffer: int=10) -> Grid:
    sizeX = len(input[0])
    sizeY = len(input)

    print(f"Initial state is {sizeX} X {sizeY}")

    map = Grid(sizeX+2*buffer, sizeY+2*buffer, ".")

    print(f"Map state is {map.sizeX} X {map.sizeY}")

    for (y, row) in enumerate(input):
        for (x, c) in enumerate(row):
            map[x+buffer, y+buffer] = c

    return map


def proposeMove(map: Grid, x: int, y:int, dirs="NSEW"):
    """ Get neighbours of # indexed thusly
012
3#4
567    
    """
    neighbours = [
        map[x-1,y-1],
        map[x,y-1],
        map[x+1,y-1],

        map[x-1,y],
        map[x+1,y],

        map[x-1,y+1],
        map[x,y+1],
        map[x+1,y+1],
    ]


    if not "#" in neighbours:
        #Alone and happy
        return None

    for dir in dirs:
        if dir=="N":
            north = neighbours[:3]
            if not "#" in north:
                return (x, y-1)

        elif dir=="S":
            south = neighbours[-3:]
            if not "#" in south:
                return (x, y+1)

        elif dir=="W":
            west = [ neighbours[0], neighbours[3], neighbours[5] ]
            if not "#" in west:
                return (x-1, y)

        elif dir=="E":
            east = [ neighbours[2], neighbours[4], neighbours[7] ]
            if not "#" in east:
                return (x+1, y)

    #Can't move
    return None

def moveRound(map: Grid, round:int=0) -> bool:

    proposals = set()
    collisions = set()
    moves = {}

    #Which directions to do in what order
    round = round % 4
    dirs = "NSWENSW"[round:round+4]
    #print(dirs)

    #First half, propose moves
    for (x, y, c) in map:
        if c != "#":
            continue

        prop = proposeMove(map, x, y, dirs)
        if prop is None:
            continue

        if prop in proposals:
            collisions.add(prop)
        else:
            proposals.add(prop)
            moves[(x,y)] = prop

    #Second half, move
    movesDone = False
    for (a, b) in moves.items():
        if b not in collisions:
            map[a[0],a[1]] = "."
            map[b[0],b[1]] = "#"
            movesDone = True

    return movesDone


def score(map: Grid) -> int:
    #Get x/y bounds of elves, and a count of them
    count = 0
    xmin, xmax, ymin, ymax = 0,0,0,0
    for (x,y,c) in map:
        if c != "#":
            continue

        count += 1
        if count == 1:
            xmin = x
            xmax = x
            ymin = y
            ymax = y
        else:
            xmin = min(xmin, x)
            xmax = max(xmax, x)
            ymin = min(ymin, y)
            ymax = max(ymax, y)

    squaresize = (xmax-xmin+1) * (ymax-ymin+1)

    return squaresize - count

def part1(input: list[str]):
    map: Grid = parsemap(input, 11)

    #print("Initial state:")
    #print(map)
    #print()

    round = 0

    while round<10:
        moved = moveRound(map, round)
        if moved:
            #print("Round", round+1)
            #print(map)
            #print()
            round += 1
        else:
            print("No more moves")
            break

    #print(map)

    return score(map)

def part2(input: list[str]):

    buffer = 200
    if tests:
        buffer = 2

    map: Grid = parsemap(input, buffer)

    #print("Initial state:")
    #print(map)
    #print()

    round = 0

    while True:
        moved = moveRound(map, round)
        round += 1
        print(round)
        if moved:
            #print("Round", round+1)
            #print(map)
            #print()
            pass
        else:
            print("No more moves")
            break

    #print(map)

    return round



def fixInput(raw: str) -> list[str]:
    lines = [x.strip() for x in raw.rstrip().split("\n")]

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
        else: rawinput = rawinput.strip()

        input = fixInput(rawinput)
        

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