#!/usr/bin/env python3

import sys
import argparse
import re
import functools
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
def vprint(*args):
    if args[0]<= verbosity:
        print(*args[1:])

def chunks(input, ints=False):
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
        "input": """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""",
        "output": 24,
        "output2": 93
    }
]

def parse(input):
    for line in input:
        c = [list(map(int, x.strip().split(","))) for x in line.split("->")]
        yield c

def makeLine(x0,y0,x1,y1):
    assert(x0==x1 or y0==y1)

    if(x0==x1):
        y0,y1 = min(y0,y1),max(y0,y1)
        for y in range(y0,y1+1):
            yield (x0,y)

    if(y0==y1):
        x0,x1 = min(x0,x1),max(x0,x1)
        for x in range(x0,x1+1):
            yield (x,y0)

def makeMaze(input, floor=False):
    coords = list(parse(input))
    allpairs = [pair for row in coords for pair in row]
    allX = [pair[0] for pair in allpairs]
    allY = [pair[1] for pair in allpairs]
    
    xMin = min(allX)
    xMax = max(allX)

    yMax = max(allY)

    #Make wide enough to fit a triangle of width = 2*height
    if floor:
        xMin = 500-2*(yMax-1)
        xMax = 500+2*(yMax-1)
        yMax += 1

    xOffset = xMin -1

    xSize = xMax-xOffset+2
    ySize = yMax+2
    


    maze = Grid(xSize, ySize, ".")

    for line in coords:
        (x0, y0) = line[0]
        for (x1,y1) in line[1:]:
            for (x,y) in makeLine(x0-xOffset,y0,x1-xOffset,y1):
                maze[x,y] = "#"
                x0,y0 = x1,y1

    #Infinite-ish floor
    if floor:
        for (x,y) in makeLine(0,ySize-1,xSize-1,ySize-1): maze[x,y] = "#"

    return (maze, xOffset,yMax)


def fallSand(grid, pos, yMax): 
    (x,y) = pos

    if y > yMax:
        return False

    if grid[x,y] != ".":
        return False

    for dx in [0, -1, 1]:
        if grid[x+dx,y+1] == ".":
            return fallSand(grid, (x+dx,y+1), yMax)

    #Rest here
    grid[x,y] = "o"

    return True


def part1(input):

    (maze, xOffset, yMax) = makeMaze(input)

    vprint(1,maze)

    source = (500-xOffset, 0)

    sands = 0

    while fallSand(maze, source, yMax):
        sands += 1

    vprint(1,maze)
    
    return sands

def part2(input):

    (maze, xOffset, yMax) = makeMaze(input, True)

    vprint(1,maze)

    source = (500-xOffset, 0)

    sands = 0

    while fallSand(maze, source, yMax):
        sands += 1

    vprint(1,maze)
    
    return sands


def fixInput(raw):
    lines = [x.strip() for x in raw.split("\n")]

    #Remove trailing blank lines
    while len(lines[-1])==0:
        lines.pop()
    return lines

if tests:

    success = True

    def splitLines(input):
        return 

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