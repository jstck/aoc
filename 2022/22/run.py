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
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5""",
        "output": 6032,
        "output2": None
    }
]


def parse(input) -> tuple[list, Grid]:
    map, route = chunks(input)

    #route = re.split(r"((\d\w)|(\w\d))", route[0])
    route = re.findall(r"(\d+|\D+)", route[0])

    route = [a if a in "LR" else int(a) for a in route]

    map_Y = len(map)
    map_X = max([len(row) for row in map])

    mapgrid = Grid(map_X, map_Y, " ")

    for (y, row) in enumerate(map):
        for (x, cell) in enumerate(row):
            mapgrid[x,y] = cell

    return route, mapgrid

@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other):
        return Position(x=self.x+other.x, y=self.y+other.y)

    def __sub__(self, other):
        return Position(x=self.x-other.x, y=self.y-other.y)


def turn(heading, spin):
    l = {
            "v": ">",
            ">": "^",
            "^": "<",
            "<": "v"
    }

    r = {
            "v": "<",
            "<": "^",
            "^": ">",
            ">": "v"
    }

    if spin == "L": return l[heading]
    if spin == "R": return r[heading]
    assert False


#Relative moves 1 step
dmove = {
    ">": Position(1, 0),
    "v": Position(0, 1),
    "<": Position(-1, 0),
    "^": Position(0, -1),
}


def walk(pos: Position, heading, map: Grid):
    #See if we can go straight ahead
    newpos = pos + dmove[heading]

    if  0 <= newpos.x < map.sizeX and 0<= newpos.y < map.sizeY:
        dest = map[newpos.x, newpos.y]
    else:
        dest = " " #Warp sign

    if dest == " ": #Warp
        if heading == ">":
            for (x, c) in enumerate(map.row(pos.y)):
                if c == " ": continue
                if c == "#": return None #Blocked!
                
                map[x, newpos.y] = heading
                return Position(x, newpos.y)

        if heading == "<":
            for (x, c) in reversed(list(enumerate(map.row(pos.y)))):
                if c == " ": continue
                if c == "#": return None #Blocked!
                
                map[x, newpos.y] = heading
                return Position(x, newpos.y)

        if heading == "v":
            for (y, c) in enumerate(map.col(pos.x)):
                if c == " ": continue
                if c == "#": return None #Blocked!
                
                map[newpos.x, y] = heading
                return Position(newpos.x, y)

        if heading == "^":
            for (y, c) in reversed(list(enumerate(map.col(pos.x)))):
                if c == " ": continue
                if c == "#": return None #Blocked!

                map[newpos.x, y] = heading
                return Position(newpos.x, y)

    if dest == "#":
        #Can't go there
        return None

    map[newpos.x, newpos.y] = heading
    return newpos
    

def move(pos: Position, dir: str, map: Grid, op) -> tuple[Position, str]:
    print(op)
    if isinstance(op, str):
        newdir = turn(dir, op)
        map[pos.x, pos.y] = newdir
        return (pos, newdir)

    else:
        for _ in range(op):
            newpos = walk(pos, dir, map)
            if newpos is None:
                return (pos, dir)
            else:
                pos = newpos
        return (pos, dir)


def score(pos, dir):
    r = 1000 * (pos.y+1)
    c = 4 * (pos.x+1)

    h = ">v<^".index(dir)

    print(r,c,h)

    return r+c+h


def part1(input: list[str]):
    
    route, map = parse(input)

    start_Y = 0
    start_X = map.row(start_Y).index(".")

    dir = ">"

    map[start_X,start_Y] = dir

    pos = Position(start_X, start_Y)

    for op in route:
        (pos, dir) = move(pos, dir, map, op)

    print(pos)
    print(map)

    return score(pos, dir)


def part2(input: list[str]):
    pass



def fixInput(raw: str) -> list[str]:
    lines = raw.strip("\n").split("\n")

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

        input = fixInput(rawinput)
        

        if run1 and "output" in case and case["output"] is not None:
            output = part1(input)
            if output != case["output"]:
                if output is not None:
                    print(f"Test part 1failed for input:\n====\n{case['input'].strip()}\n====\n.\n\nGot:\n{output}\n\nExpected:\n{case['output']}\n")
                success = False

        if run2 and "output2" in case and case["output2"] is not None:
            output = part2(input)
            if output != case["output2"]:
                if output is not None:
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