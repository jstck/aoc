#!/usr/bin/env python3

import sys
import argparse
import re
from grid import Grid
from queue import PriorityQueue
from pprint import PrettyPrinter


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

pp = PrettyPrinter(indent=2)


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

#TOO HIGH: 484

test_cases = [
    {
        "input": """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""",
        "output": 31,
        "output2": 29
    }
]


def parse(input):
    sizeX = len(input[0])
    sizeY = len(input)

    mountain = Grid(sizeX, sizeY)

    for i in range(len(input)):
        line = list(input[i])

        try:
            startX = line.index("S")
            startY = i
            line[startX] = 'a'
        except ValueError:
            pass

        try:
            endX = line.index("E")
            endY = i
            line[endX] = 'z'
        except ValueError:
            pass

        heights = [ord(x) - ord('a') for x in line]

        mountain[i] = heights

    return (mountain, startX, startY, endX, endY)

def neighbours(x, y, sizeX, sizeY):
    for dx in [-1, 1]:
        x1 = x + dx
        if x1 < 0 or x1>=sizeX:
            continue
        yield (x1,y)
    for dy in [-1, 1]:
        y1 = y + dy
        if y1 < 0 or y1>=sizeY:
            continue
        yield (x,y1)



def part1(input):
    pq = PriorityQueue()
    visited = set()

    (mountain, startX, startY, endX, endY) = parse(input)
    sizeX = mountain.sizeX
    sizeY = mountain.sizeY

    pq.put((0, startX, startY))

    while not pq.empty():
        (cost, x, y) = pq.get()

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if x == endX and y == endY:
            print("FOUND", cost)
            return cost

        height = mountain[x, y]

        for (nx, ny) in neighbours(x, y, sizeX, sizeY):
            if (nx, ny) not in visited:
                newheight = mountain[nx, ny]
                if newheight <= height+1:
                    pq.put((cost+1, nx, ny))


def part2(input):
    pq = PriorityQueue()
    visited = set()

    (mountain, startX, startY, endX, endY) = parse(input)
    sizeX = mountain.sizeX
    sizeY = mountain.sizeY

    for x in range(sizeX):
        for y in range(sizeY):
            if mountain[x, y] == 0 and not (x == startX and y == startY):
                pq.put((0, x, y))

    while not pq.empty():
        (cost, x, y) = pq.get()

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if x == endX and y == endY:
            print("FOUND", cost)
            return cost

        height = mountain[x, y]

        for (nx, ny) in neighbours(x, y, sizeX, sizeY):
            if (nx, ny) not in visited:
                newheight = mountain[nx, ny]
                if newheight <= height+1:
                    pq.put((cost+1, nx, ny))



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