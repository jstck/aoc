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
        "input": """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3""",
        "output": 26,
        "output2": 56000011
    }
]


def parse(input):
    for line in input:
        matches = re.match(r"^Sensor at x=([0-9-]+), y=([0-9-]+): closest beacon is at x=([0-9-]+), y=([0-9-]+)$", line)
        xS = int(matches.group(1))
        yS = int(matches.group(2))
        xB = int(matches.group(3))
        yB = int(matches.group(4))

        yield (xS, yS, xB, yB)

def part1(input, checkrow):

    sensors = set()
    beacons = set()
    nobeacons = set()

    for xS, yS, xB, yB in parse(input):

        if yS==checkrow: sensors.add(xS)
        if yB==checkrow: beacons.add(xB)

        distance = abs(xB-xS) + abs(yB-yS)

        #If distance from row to check is larger than distance from sensor, no coverage there
        if abs(yS - checkrow) > distance:
            continue

        xMin = xS - (distance - abs(yS - checkrow))
        xMax = xS + (distance - abs(yS - checkrow))

        for x in range(xMin, xMax+1):
            nobeacons.add(x)


    count = 0
    for x in nobeacons:
        if x not in beacons:
            count += 1
    return count


def mergeRanges(ranges):

    a0, b0 = ranges[0]

    for (a1, b1) in ranges[1:]:
        if a1 <= b0 + 1:
            b0 = max(b0,b1)
        else:
            yield(a0,b0)
            a0, b0 = a1, b1

    yield (a0, b0)


def gaps(ranges):
    if len(ranges)<=1:
        return []

    g = []

    for i in range(len(ranges)-1):
        g1 = ranges[i][1]
        g2 = ranges[i+1][0]
        g.extend(range(g1+1, g2))

    return g

def part2(input, maxsize):
    sensors = []
    beacons = set()

    for xS, yS, xB, yB in parse(input):

        distance = abs(xB-xS) + abs(yB-yS)

        sensors.append((xS, yS, distance))
        beacons.add((xB, yB))

    f = None

    for y in range(0,maxsize+1):

        coverage = []

        for (xS, yS, distance) in sensors:
            w = distance - abs(yS-y)
            #No coverage here
            if w < 0:
                continue

            xMin = xS - w
            xMax = xS + w
            coverage.append((xMin, xMax))

        if y % 100000==0: print(y, len(coverage))

        coverage.sort()
        coverage = list(mergeRanges(coverage))
        g = gaps(coverage)

        for x in g:
            f = x*4000000+y
            print()
            print(f"Gap at {x},{y}, frequency {f}")
            print()

    return f





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
            output = part1(input, 10)
            if output != case["output"]:
                print(f"Test part 1failed for input:\n====\n{case['input'].strip()}\n====\n.\n\nGot:\n{output}\n\nExpected:\n{case['output']}\n")
                success = False

        if run2 and "output2" in case and case["output2"] is not None:
            output = part2(input, 20)
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
        result1 = part1(input, 2000000)
    if run2:
        print("Running part 2")
        result2 = part2(input, 4000000)

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