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
        "input": "test.txt",
        "output": 13140,
        "output2": "4E71"
    }
]


important = [20, 60, 100, 140, 180, 220]

def output(x, cycle, results):
    y = x*cycle
    results.append(y)
    vprint(1, f"Output {x}->{y} at {cycle}", results)

def part1(input):
    results = []
    cycle = 0
    x = 1
    for line in input:
        parts = [x.strip() for x in line.split()]
        vprint(2, f"{cycle:04}: X={x:03} {line.strip()}")
        if len(parts) == 0:
            continue
        elif parts[0] == "noop":
            cycle += 1
            if cycle in important:
                output(x, cycle, results)
        elif parts[0] == "addx":
            d = int(parts[1])
            cycle += 2
            if cycle-1 in important:
                output(x, cycle-1, results)
            if cycle in important:
                output(x, cycle, results)
            x += d
            
        else:
            print("UNKNOWN INSTRUCTION:", parts)
            assert(False)

    return sum(results)

crt_row = []

def draw(x, cycle):
    global crt_row
    col = (cycle-1) % 40
    vprint(2, cycle, x, col)
    if abs(col-x) <= 1:
        crt_row.append("##")
    else:
        crt_row.append("  ")

    if col >= 39:
        print("".join(crt_row))
        crt_row = []

def part2(input):
    cycle = 0
    x = 1
    
    for line in input:
        parts = [x.strip() for x in line.split()]
        #vprint(2, f"{cycle:04}: X={x:03} {line.strip()}")
        if len(parts) == 0:
            continue
        elif parts[0] == "noop":
            cycle += 1
            draw(x, cycle)
        elif parts[0] == "addx":
            d = int(parts[1])
            cycle += 1
            draw(x, cycle)
            cycle += 1
            draw(x, cycle)
            x += d            
        else:
            print("UNKNOWN INSTRUCTION:", parts)
            assert(False)

    draw(x, cycle)

    return "4E71"






if tests:

    success = True

    def splitLines(input):
        return [x.strip() for x in input.split("\n")]

    for case in test_cases:
        with open(case["input"], "r") as stuff:
            input = stuff.readlines()
        if run1:
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