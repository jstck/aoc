#!/usr/bin/env python3

import sys
import argparse
import re

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
        "input": "FILE:sample.txt",
        "output": 112,
        "output2": None
    }
]

def initial_set(input):
    space = set()
    z=0
    for (y, row) in enumerate(input):
        print(y,row)
        for (x, cell) in enumerate(row):
            if cell=="#":
                space.add((x,y,z))

    return space

def findBounds(space):
    xmin, xmax, ymin, ymax, zmin, zmax = None, None, None, None, None, None

    for (x, y, z) in space:
        if xmin is None or x < xmin: xmin = x
        if xmax is None or x > xmax: xmax = x
        if ymin is None or y < xmin: ymin = y
        if ymax is None or y > xmax: ymax = y
        if zmin is None or z < xmin: zmin = z
        if zmax is None or z > xmax: zmax = z

    return ( (xmin, xmax), (ymin, ymax), (zmin, zmax) )

def neighbours(t):
    (x,y,z) = t

    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            for dz in [-1,0,1]:
                if dx==0 and dy==0 and dz==0: continue
                yield (x+dx,y+dy,z+dz)


def printslice(space, z=0):
    (xbounds, ybounds, _) = findBounds(space)
    (xmin, xmax) = xbounds
    (ymin, ymax) = ybounds

    for y in range(ymin, ymax+1):
        r = []
        for x in range(xmin, xmax+1):
            if (x,y,z) in space:
                r.append("#")
            else:
                r.append(".")
        print("".join(r))
    

def part1(input):
    space = initial_set(input)

    for round in range(1,6+1):
        print("ROUND", round)
        (xbounds, ybounds, zbounds) = findBounds(space)
        
        newspace = set()

        for x in range(xbounds[0]-1, xbounds[1]+2):
            for y in range(ybounds[0]-1, ybounds[1]+2):
                for z in range(zbounds[0]-1, zbounds[1]+2):
                    t = (x,y,z)
                    me = (x,y,z) in space
                    n = len([p for p in neighbours((x,y,z)) if p in space])
                    if n==3 or (n==2 and me): newspace.add(t)

        printslice(newspace, 0)
        print(len(newspace))
        space = newspace


def part2(input):
    pass



def fixInput(raw):
    lines = [x.strip() for x in raw.split("\n")]

    #Remove trailing blank lines
    while len(lines[-1]):
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