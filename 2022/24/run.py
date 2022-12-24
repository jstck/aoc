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
from typing import Iterator

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

DIR_NORTH = 0
DIR_SOUTH = 1
DIR_WEST = 2
DIR_EAST = 3

def getDirection(dir: str) -> int:
    return "^v<>".index(dir)

@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __repr__(self):
        return f"(X{self.x} Y{self.y})"

    def __lt__(self, other):
        #Less than = "lower manhattan distance to goal" = "higher sum of x+y"
        mine = self.x + self.y
        theirs = other.x + other.y

        return mine > theirs

@dataclass(frozen=True)
class Blizzard:
    start: Position
    direction: int
    size_x: int
    size_y: int

    def getPosition(self, time=0) -> Position:
        x = self.start.x
        y = self.start.y

        if self.direction == DIR_WEST:
            x = (self.start.x - time) % self.size_x
        elif self.direction == DIR_EAST:
            x = (self.start.x + time) % self.size_x
        elif self.direction == DIR_NORTH:
            y = (self.start.y - time) % self.size_y
        elif self.direction == DIR_SOUTH:
            y = (self.start.y + time) % self.size_y
        else:
            print("INVALID DIRECTION", self.direction)
            assert(False)

        return Position(x,y)

Forecast = frozenset[Position]

State = tuple[int, Position]


class Forecaster:

    def __init__(self, blizzards: list[Blizzard]):
        self.blizzards: list[Blizzard] = blizzards
        self._forecasts: dict[int,Forecast] = {}

    def getForecast(self, time: int) -> Forecast:
        if time in self._forecasts:
            return self._forecasts[time]
        else:
            newforecast = set()
            for blizzard in self.blizzards:
                newforecast.add(blizzard.getPosition(time))
            
            newforecast = frozenset(newforecast)
            self._forecasts[time] = newforecast
            #vprint(1, f"Made new forecast for t={time}")
            return newforecast



def parse(input: list[str]):
    #First and last lines are boring, ignore those
    size_x = len(input[0]) - 2
    size_y = len(input) - 2

    blizzards: list[Blizzard] = list()

    for (y, row) in enumerate(input[1:-1]):
        for (x, c) in enumerate(row[1:-1]):
            if c == ".": continue

            d = getDirection(c)
            blizzard = Blizzard(Position(x,y), d, size_x, size_y)
            blizzards.append(blizzard)
    forecasts = Forecaster(blizzards)

    startpos = Position(0, -1)

    endpos = Position(size_x-1, size_y)

    return (startpos, endpos, size_x, size_y, forecasts)

def makemoves(pos: Position, time: int, forecasts: Forecaster, max_x: int, max_y: int) -> Iterator[State]:

    t1 = time + 1
    #Weather forecast for next position
    forecast: Forecast = forecasts.getForecast(t1)

    #Go right?
    if pos.x < max_x and pos.y>=0 and pos.y <= max_y: #Can't move right on start/end rows (-1)
        right = Position(pos.x+1, pos.y)
        if not right in forecast:
            yield(t1, right)

    #Go down?
    if pos.y < max_y:
        down = Position(pos.x, pos.y+1)
        if not down in forecast:
            yield(t1, down)

    #Go left?
    if pos.x > 0 and pos.y>=0 and pos.y <= max_y: #Can't move left on start/end rows (-1)
        left = Position(pos.x-1, pos.y)
        if not left in forecast:
            yield(t1, left)

    #Go up?
    if pos.y > 0:
        up = Position(pos.x, pos.y-1)
        if not up in forecast:
            yield(t1, up)

    #Shelter in place?
    if pos not in forecast:
        yield(t1, pos)



test_cases = [
    {
        "input": "FILE:sample.txt",
        "output": 18,
        "output2": 54
    }
]


def printstate(state: State, forecasts: Forecaster, size_x, size_y):
    (t, pos) = state

    blizz = forecasts.getForecast(t)
    print(f"T={t}")
    if pos in blizz: print("KROCK VID", pos)
    firstline = ["#"] * (size_x+2)
    if pos == Position(0, -1):
        firstline[1] = "E"
    else:
        firstline[1] = "."
    print("".join(firstline))

    for y in range(0, size_y):
        row = ["#"]
        for x in range(0, size_x):
            p = Position(x,y)
            if p in blizz:
                row.append("@")
            elif p == pos:
                row.append("E")
            else:
                row.append(".")
        row.append("#")
        print("".join(row))

    lastline = ["#"] * (size_x+2)
    lastline[-2] = "."
    print("".join(lastline))
    print()


def findpath(startpos, endpos, size_x, size_y, forecasts, t_start = 0) -> int:
    visited: set[State] = set()

    max_x = size_x - 1
    max_y = size_y - 1

    pq = PriorityQueue()
    pq.put((t_start, startpos))

    while not pq.empty():
        state: State = pq.get()
        (t, pos) = state

        if pos == endpos:
            #Solution found
            print(f"FOUND SOLUTION to {endpos} AT t={t}")
            return t

        if state in visited:
            continue

        visited.add(state)

        for newstate in makemoves(pos, t, forecasts, max_x, max_y):
            if not newstate in visited:
                pq.put(newstate)

    return -1


def part1(input: list[str]):
    (startpos, endpos, size_x, size_y, forecasts) = parse(input)

    almost_end = Position(endpos.x, endpos.y-1)

    moves = findpath(startpos, almost_end, size_x, size_y, forecasts, 0)+1

    return moves

def part2(input: list[str]):
    (startpos, endpos, size_x, size_y, forecasts) = parse(input)

    almost_start = Position(startpos.x, startpos.y+1)
    almost_end = Position(endpos.x, endpos.y-1)

    moves = findpath(startpos, almost_end, size_x, size_y, forecasts, 0)+1
    moves = findpath(endpos, almost_start, size_x, size_y, forecasts, moves)+1
    moves = findpath(startpos, almost_end, size_x, size_y, forecasts, moves)+1

    return moves



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