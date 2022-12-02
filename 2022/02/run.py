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
        "input":"""A Y
B X
C Z
""",
        "output": 15,
        "output2": 12
    }
]


def round_score(playerA, playerB):
    t = (playerA, playerB)
    if t == ("A", "X"): return 1+3 #Rock Rock draw
    if t == ("A", "Y"): return 2+6 #Rock Paper win
    if t == ("A", "Z"): return 3+0 #Rock Scissors loss
    if t == ("B", "X"): return 1+0 #Paper Rock loss
    if t == ("B", "Y"): return 2+3 #Paper Paper draw
    if t == ("B", "Z"): return 3+6 #Paper Scissors win
    if t == ("C", "X"): return 1+6 #Scissors Rock win
    if t == ("C", "Y"): return 2+0 #Scissors Paper loss
    if t == ("C", "Z"): return 3+3 #Scissors Scissors draw

    print("ERROR", t)
    sys.exit(1)


def round_strat(playerA, playerB):
    t = (playerA, playerB)
    if t == ("A", "X"): return 0+3 #Rock, lose = scissors
    if t == ("A", "Y"): return 3+1 #Rock, draw = rock
    if t == ("A", "Z"): return 6+2 #Rock, win = paper
    if t == ("B", "X"): return 0+1 #Paper, lose = rock
    if t == ("B", "Y"): return 3+2 #Paper, draw = paper
    if t == ("B", "Z"): return 6+3 #Paper, win = scissors
    if t == ("C", "X"): return 0+2 #Scissors, lose = paper
    if t == ("C", "Y"): return 3+3 #Scissors, draw = scissors
    if t == ("C", "Z"): return 6+1 #Scissors, win = rock

    print("ERROR", t)
    sys.exit(1)



def part1(input):
    sum = 0
    for line in input:
        points = 0
        vprint(2, line)
        (elf, me) = line.strip().split(" ")
        score = round_score(elf, me)
        vprint(1, score)
        sum += score
    return sum


def part2(input):
    sum = 0
    for line in input:
        points = 0
        vprint(2, line)
        (elf, me) = line.strip().split(" ")
        score = round_strat(elf, me)
        vprint(1, score)
        sum += score
    return sum



if tests:


    def splitLines(input):
        return [x.strip() for x in input.strip().split("\n")]

    success = True

    for case in test_cases:
        input = splitLines(case["input"])
        if run1:
            output = part1(input)
            vprint(2, "IN:\n",input)
            vprint(1, "OUT:\n",output)
            if output != case["output"]:
                print(f"Test part 1failed for input:\n====\n{case['input'].strip()}\n====\n.\n\nGot:\n{output}\n\nExpected:\n{case['output']}\n")
                success = False

        if run2 and case["output2"] is not None:
            output = part2(input)
            vprint(2, "IN:\n",input)
            vprint(1, "OUT:\n",output)
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