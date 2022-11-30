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





test_cases = [
    {
        "input": "",
        "output": "",
        "output2": None
    }
]

def part1(input):
    return ""

def part2(input):
    pass






if tests:


    def splitLines(input):
        return [x.strip() for x in input.split("\n")]

    success = True

    for case in test_cases:
        input = splitLines(case["input"])
        if run1:
            output = part1(input)
            if output != case["output"]:
                print(f"Test failed for input {case['input']}.\n\nGot:\n{output}\n\nExpected:\n{case['output']}\n")
                success = False

        if run2 and case["output2"] is not None:
            output = part2(input)
            if output != case["output2"]:
                print(f"Test failed for input {case['input']}.\n\nGot:\n{output}\n\nExpected:\n{case['output2']}\n")
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

    if run2:
        print("PART 2")
        print("======")
        print(part2(input))