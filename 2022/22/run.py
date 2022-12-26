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
        "input": "FILE:sample.txt",
        "output": 6032,
        "output2": 5031
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

warp_truth = {
    (1, "^"): (6, ">"),
    (1, "<"): (4, ">"),
    (2, "^"): (6, "^"),
    (2, ">"): (5, "<"),
    (2, "v"): (3, "<"),
    (3, "<"): (4, "v"),
    (3, ">"): (2, "^"),
    (4, "^"): (3, ">"),
    (4, "<"): (1, ">"),
    (5, ">"): (2, "<"),
    (5, "v"): (6, "<"),
    (6, "<"): (1, "v"),
    (6, ">"): (5, "^"),
    (6, "v"): (2, "v"),
}


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

def quadrant(pos: Position, map: Grid) -> int:
    if tests:
        x = (4*pos.x) // map.sizeX
        y = 3*pos.y // map.sizeY

        if x==2 and y==0: return 1
        if x==0 and y==1: return 2
        if x==1 and y==1: return 3
        if x==2 and y==1: return 4
        if x==2 and y==2: return 5
        if x==3 and y==2: return 6

        return 0

    else:
        x = (3*pos.x) // map.sizeX
        y = 4*pos.y // map.sizeY
        if x==1 and y==0: return 1
        if x==2 and y==0: return 2
        if x==1 and y==1: return 3
        if x==0 and y==2: return 4
        if x==1 and y==2: return 5
        if x==0 and y==3: return 6

        return 0

def mapstate(x: int, y: int, d: str) -> tuple[Position, str]:
    return (Position(x,y), d)

def warp(pos: Position, heading, map: Grid) -> tuple[Position, str]:
    qfrom = quadrant(pos, map)

    #Size of one square
    if tests:
        square_x = map.sizeX // 4
        square_y = map.sizeY // 3
    else:
        square_x = map.sizeX // 3
        square_y = map.sizeY // 4

    assert square_x == square_y

    square = square_x

    #X and Y coords within it's square
    px = pos.x % square
    py = pos.y % square

    if tests:

        if qfrom == 1 and heading == "^":
            #Map to Q2 North, reversed
            y = square
            x = square - 1 - px # square_x - (pos.x - 2*square_x)
            return mapstate(x,y,"v")

        if qfrom == 1 and heading == "<":
            #Map to Q3 north
            y = square
            x = square + py
            return mapstate(x,y,"v")
        if qfrom == 1 and heading == ">":
            #Map to Q6 east, reversed
            x = 4*square-1
            y = 3*square - 1 - py
            return mapstate(x,y,"<")

        if qfrom == 2 and heading == "^":
            #map to 1 N reversed
            x = 0
            y = 3*square - 1 - px
            return mapstate(x,y,"v")

        if qfrom == 2 and heading == "<":
            #Map to 6 S reversed
            y = 3*square-1
            x = 4*square - 1 - py
            return mapstate(x,y,"^")

        if qfrom == 2 and heading == "v":
            #Map to 5S, reversed
            y = 3*square-1
            x = 3*square - 1 - px
            return mapstate(x,y,"^")

        if qfrom == 3 and heading == "^":
            #Map to 1 W
            x = 2*square
            y = px
            return mapstate(x,y,">")

        if qfrom == 3 and heading == "v":
            #Map to 5W reversed
            x = 2*square
            y = 3*square - 1 - px
            return mapstate(x,y,">")

        if qfrom == 4 and heading == ">":
            #6N reversed
            y = 2*square
            x = 4*square - 1 - py
            return mapstate(x,y,"v")

        if qfrom == 5 and heading == "<":
            #3S reversed
            y = 2*square - 1
            x = 2*square - 1 - py
            return mapstate(x,y,"^")

        if qfrom == 5 and heading == "v":
            #2S reversed
            y = 2*square - 1
            x = square - 1 - px
            return mapstate(x,y,"^")
        
        if qfrom == 6 and heading == "^":
            #4E reversed
            x = 3*square - 1
            y = 2*square - 1 - px
            return mapstate(x,y,"<")
        
        if qfrom == 6 and heading == ">":
            #1E reversed
            x = 3*square - 1
            y = square - 1 - py
            return mapstate(x,y,"<")
        
        if qfrom == 6 and heading == "v":
            #2W reversed
            x = 0
            y = 2*square - 1 - px
            return mapstate(x,y,">")
    else:
        #REAL CUBE
        
        if qfrom == 1 and heading == "^":
            #Map to 6W
            x = 0
            y = 3*square + px
            return mapstate(x,y,">")

        if qfrom == 1 and heading == "<":
            #Map to 4W reversed
            x = 0
            y = 3*square -1 - py
            return mapstate(x,y,">")

        if qfrom == 2 and heading == "^":
            #Map to 6S
            y = 4*square - 1
            x = px
            return mapstate(x,y,"^")

        if qfrom == 2 and heading == ">":
            #Map to 5E reversed
            x = 2 * square - 1
            y = 3*square - 1 - py
            return mapstate(x,y,"<")

        if qfrom == 2 and heading == "v":
            #Map to 3E
            x = 2 * square - 1
            y = square + px
            return mapstate(x,y,"<")

        if qfrom == 3 and heading == "<":
            #Map to 4N
            y = 2*square
            x = py
            return mapstate(x,y,"v")

        if qfrom == 3 and heading == ">":
            #Map to 2S
            y = square-1
            x = 2*square + py
            return mapstate(x,y,"^")

        if qfrom == 4 and heading == "^":
            #Map to 3W
            x = square
            y = square + px
            return mapstate(x,y,">")

        if qfrom == 4 and heading == "<":
            #Map to 1W R
            x = square
            y = square - 1 - py
            return mapstate(x,y,">")

        if qfrom == 5 and heading == ">":
            #Map to 2E R
            x = 3 * square - 1
            y = square - 1 - py
            return mapstate(x,y,"<")

        if qfrom == 5 and heading == "v":
            #Map to 6E
            x = square - 1
            y = 3 * square + px
            return mapstate(x,y,"<")

        if qfrom == 6 and heading == "<":
            #Map to 1N
            y = 0
            x = square + py
            return mapstate(x,y,"v")

        if qfrom == 6 and heading == ">":
            #Map to 5S
            y = 3*square - 1
            x = square + py
            return mapstate(x,y,"^")

        if qfrom == 6 and heading == "v":
            #Map to 2N
            y = 0
            x = 2*square + px
            return mapstate(x,y,"v")
        

    print(f"I don't where I'm going from quadrant {qfrom} going {heading}, from {pos}")
    assert False
    #return (pos, heading)

def walk(pos: Position, heading, map: Grid, part2=False):
    #See if we can go straight ahead
    newpos = pos + dmove[heading]

    if  0 <= newpos.x < map.sizeX and 0<= newpos.y < map.sizeY:
        dest = map[newpos.x, newpos.y]
    else:
        dest = " " #Warp sign

    if dest == " ": #Warp
        if part2:
            (newpos, newheading) = warp(pos, heading, map)
            qfrom = quadrant(pos, map)
            qto = quadrant(newpos, map)
            print(f"Warp from {pos} Q{qfrom} {heading} to {pos} Q{qto} {newheading}")
            warptarget = map[newpos.x, newpos.y]

            #Validate_warp
            warp_dest = warp_truth[(qfrom, heading)]
            if not warp_dest == (qto, newheading):
                print(f"INVALID WARP from {qfrom} {heading}. Should be {warp_dest}, is {(qto, newheading)}")
                assert False

            if warptarget == "#":
                return None
            elif warptarget in ".<>^v":
                map[newpos.x,newpos.y] = newheading
                return mapstate(newpos.x,newpos.y,newheading)
            else:
                print(f"INVALID WARP TARGET {warptarget} at {newpos} Q{qto} (from {pos} Q{qfrom} {heading}")
                map[newpos.x,newpos.y] = "X"
                print(map)
                assert False

        if heading == ">":
            for (x, c) in enumerate(map.row(pos.y)):
                if c == " ": continue
                if c == "#": return None #Blocked!
                
                map[x, newpos.y] = heading
                return mapstate(x, newpos.y, heading)

        if heading == "<":
            for (x, c) in reversed(list(enumerate(map.row(pos.y)))):
                if c == " ": continue
                if c == "#": return None #Blocked!
                
                map[x, newpos.y] = heading
                return mapstate(x, newpos.y, heading)

        if heading == "v":
            for (y, c) in enumerate(map.col(pos.x)):
                if c == " ": continue
                if c == "#": return None #Blocked!
                
                map[newpos.x, y] = heading
                return mapstate(newpos.x, y, heading)

        if heading == "^":
            for (y, c) in reversed(list(enumerate(map.col(pos.x)))):
                if c == " ": continue
                if c == "#": return None #Blocked!

                map[newpos.x, y] = heading
                return mapstate(newpos.x, y, heading)

    if dest == "#":
        #Can't go there
        return None

    map[newpos.x, newpos.y] = heading
    return mapstate(newpos.x, newpos.y, heading)
    

def move(pos: Position, dir: str, map: Grid, op, part2=False) -> tuple[Position, str]:
    if isinstance(op, str):
        newdir = turn(dir, op)
        map[pos.x, pos.y] = newdir
        return (pos, newdir)

    else:
        for _ in range(op):
            newstate = walk(pos, dir, map, part2)
            if newstate is None:
                return (pos, dir)
            else:
                (pos, dir) = newstate
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
    #print(map)

    return score(pos, dir)


def part2(input: list[str]):
    route, map = parse(input)

    start_Y = 0
    start_X = map.row(start_Y).index(".")

    dir = ">"

    map[start_X,start_Y] = dir

    pos = Position(start_X, start_Y)

    for op in route:
        (pos, dir) = move(pos, dir, map, op, part2=True)

    print(pos)
    #print(map)

    return score(pos, dir)



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