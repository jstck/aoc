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
parser.add_argument('--verbose', '-v', action='count', default=0, help="Increase verbosity")

args = parser.parse_args()

tests = vars(args)["t"]
run2 = vars(args)["2"]
run1 = vars(args)["1"] or not run2 #Do part 1 if nothing else specified
verbosity = vars(args)["verbose"]

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

    chunky.append(chunk)
    return chunky



test_cases = [
    {
        "input": """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""",
        "output": 2,
        "output2": 4
    }
]


def parse(input):
    for line in input:
        a,b = line.split(",")
        a1,a2 = a.split("-")
        b1,b2 = b.split("-")

        a1 = int(a1)
        a2 = int(a2)
        b1 = int(b1)
        b2 = int(b2)

        assert(a1<=a2)
        assert(b1<=b2)

        yield (a1,a2,b1,b2)

def rangeInside(x1,x2,y1,y2):
    if y1>=x1 and y2<=x2:
        return True
    if x1>=y1 and x2<=y2:
        return True
    return False


def hasOverlap(x1,x2,y1,y2):
    x = set(range(x1,x2+1))
    y = set(range(y1,y2+1))
    return len(x & y) > 0

def part1(input):
    count = 0
    for (a1,a2,b1,b2) in parse(input):

        if rangeInside(a1,a2,b1,b2):
            count += 1

    return count

def part2(input):
    count = 0
    for (a1,a2,b1,b2) in parse(input):

        if hasOverlap(a1,a2,b1,b2):
            count += 1

    return count








if tests:


    def splitLines(input):
        return [x.strip() for x in input.split("\n")]

    success = True

    for case in test_cases:
        input = splitLines(case["input"])
        if run1:
            output = part1(input)
            if output != case["output"]:
                print(f"Test part 1failed for input:\n====\n{case['input'].strip()}\n====\n.\n\nGot:\n{output}\n\nExpected:\n{case['output']}\n")
                success = False

        if run2 and case["output2"] is not None:
            output = part2(input)
            if output != case["output2"]:
                print(f"Test part 2 failed for input:\n====\n{case['input'].strip()}\n====\nGot:\n{output}\n\nExpected:\n{case['output2']}\n")
                success = False

    if success:
        print("All tests passed successfully!")

else:
    try:
        fp = open("input.txt", "r")
    except FileNotFoundError:
        fp = sys.stdin
    
    input = [x.strip() for x in fp.readlines()]

    if run1:
        print("PART 1")
        print("======")
        print(part1(input))

    if run1 and run2:
        print()

    if run2:
        print("PART 2")
        print("======")
        print(part2(input))