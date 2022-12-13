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
        "input": "0,3,6",
        "output": 436,
        "output2": 175594
    },
    {
        "input": "1,3,2",
        "output": 1,
        "output2": 2578
    },
    {
        "input": "2,1,3",
        "output": 10,
        "output2": 3544142
    },
    {
        "input": "1,2,3",
        "output": 27,
        "output2": 261214
    },
    {
        "input": "2,3,1",
        "output": 78,
        "output2": 6895259
    },
    {
        "input": "3,2,1",
        "output": 438,
        "output2": 18
    },
    {
        "input": "3,1,2",
        "output": 1836,
        "output2": 362
    },
]

def memorygame(input, turns=2020):
    memory = {}

    start = [int(x) for x in input[0].split(",")]

    for (i, x) in enumerate(start):
        turn = i+1
        assert(x not in memory)
        memory[x] = [turn]
        last = x

    last = start[-1]

    while turn < turns:
        turn += 1
        if turn%1000000==0: print(turn)
        if len(memory[last])==1:
            speak = 0
        else:
            speak = memory[last][-1] - memory[last][-2]

        if speak in memory:
            memory[speak] = [memory[speak][-1], turn]
        else:
            memory[speak] = [turn]

        last = speak

    return last

def part1(input):
    return memorygame(input)

def part2(input):
    return memorygame(input, 30000000)



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