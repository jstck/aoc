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
from typing import Union
import pprint

match = re.search(r"aoc/?(\d+)/(\d+)", __file__)
if match:
    descr = "Advent of Code " + match.group(1) + ":" + match.group(2)
else:
    descr = "Advent of some kind of Code"

parser = argparse.ArgumentParser(description=descr)

parser.add_argument("-1", action="store_true", help="Do part 1")
parser.add_argument("-2", action="store_true", help="Do part 2")
parser.add_argument("-t", action="store_true", help="Run tests")
parser.add_argument("-f", "--input-file", default="input.txt")
parser.add_argument(
    "--verbose", "-v", action="count", default=0, help="Increase verbosity"
)

args = parser.parse_args()

tests = vars(args)["t"]
run2 = vars(args)["2"]
run1 = vars(args)["1"] or not run2  # Do part 1 if nothing else specified
verbosity = vars(args)["verbose"]
input_file = vars(args)["input_file"]

pp = pprint.PrettyPrinter(indent=2)

# Print controlled by verbosity level
def vprint(*args) -> None:
    if args[0] <= verbosity:
        print(*args[1:])

test_cases = [
    {
        "input": """
1
2
-3
3
-2
0
4
""",
        "output": 3,
        "output2": 1623178306,
    }
]

def shift(positions: dict[int, int], index: int, delta: int, size: int) -> None:
    invpos = {b: a for (a,b) in positions.items()}
    
    oldpos = positions[index]
    newpos = (oldpos + delta) % (size-1)
    if delta < 0 and newpos == 0:
        newpos = size-1
    if delta > 0 and newpos == size-1:
        newpos = 0
        
    if newpos > oldpos:
        #Everything between newpos and pos gets shifted one step left
        #print(f"shiftstuff between {oldpos+1} - {newpos}")
        for i in range(oldpos+1, newpos+1):
            target = invpos[i]
            positions[target] -= 1
        positions[index] = newpos

    elif newpos < oldpos:
        #Everything between newpos and pos gets shifted one step right
        for i in range(newpos, oldpos):
            target = invpos[i]
            positions[target] += 1
        positions[index] = newpos

def render(positions: dict[int, int], orig: list[int]) -> list[int]:
    size = len(positions)

    tmp: list[Union[None,int]]= [None] * size

    for (oldpos, newpos) in positions.items():
        if tmp[newpos] is not None:
            print("DUPLICATE POSITION: ", newpos)

        tmp[newpos] = orig[oldpos]

    for (i, v) in enumerate(tmp):
        if v is None:
            print("NO VALUE FOR POSITION:", i)

    result: list[int] = []

    for v in tmp:
        if isinstance(v, int):
            result.append(v)
        else:
            result.append(-10000)

    return result


def score(seq: list[int]) -> int:
    zero = seq.index(0)

    size = len(seq)

    n1k = seq[(zero+1000)%size]
    n2k = seq[(zero+2000)%size]
    n3k = seq[(zero+3000)%size]

    #print(n1k, n2k, n3k)
    return n1k+n2k+n3k

def part1(input: list[str]) -> int:
    seq = [int(x) for x in input]
    size = len(seq)

    positions = {i: i for i, _ in enumerate(seq)}

    for i in positions:
        v = seq[i]
        shift(positions, i, v, size)

    seq2 = render(positions, seq)
    #print(seq2)
    x = score(seq2)
    print(x)

    return x


def part2(input: list[str]) -> int:
    key = 811589153
    seq = [int(x)*key for x in input]
    size = len(seq)

    positions = {i: i for i, _ in enumerate(seq)}

    for round in range(10):
        print("Round", round+1)
        for i in positions:
            v = seq[i]
            shift(positions, i, v, size)

    seq2 = render(positions, seq)
    #print(seq2)
    x = score(seq2)
    #print(x)

    return x


def fixInput(raw: str) -> list[str]:
    lines = [x.strip() for x in raw.split("\n")]

    # Remove trailing blank lines
    while len(lines[-1]) == 0:
        lines.pop()
    return lines


if tests:

    success = True

    for case in test_cases:
        rawinput = case["input"]

        match = re.search(r"^FILE:([\S]+)$", rawinput.strip())
        if match:
            filename = match.group(1)
            print("Loading", filename)
            with open(filename, "r") as fp:
                rawinput = fp.read()

        input = fixInput(rawinput.strip())

        if run1 and "output" in case and case["output"] is not None:
            output = part1(input)
            if output != case["output"]:
                print(
                    f"Test part 1failed for input:\n====\n{case['input'].strip()}\n====\n.\n\nGot:\n{output}\n\nExpected:\n{case['output']}\n"
                )
                success = False

        if run2 and "output2" in case and case["output2"] is not None:
            output = part2(input)
            if output != case["output2"]:
                print(
                    f"Test part 2 failed for input:\n====\n{case['input'].strip()}\n====\nGot:\n{output}\n\nExpected:\n{case['output2']}\n"
                )
                success = False

    if success:
        print("All tests passed successfully!")

else:
    result1, result2 = None, None
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
