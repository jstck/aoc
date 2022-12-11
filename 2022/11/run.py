#!/usr/bin/env python3

import sys
import argparse
import re

from monkey import Monkey

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
        "input": "FILE:test.txt",
        "output": 10605,
        "output2": 2713310158
    }
]

def part1(input):
    monkeys = []

    for chunkymonkey in chunks(input):
        monkey = Monkey(chunkymonkey)
        monkeys.append(monkey)

    for round in range(1, 21):
        print(f"Round {round}")

        for monkey in monkeys:
            monkey.throwShit(monkeys)
        
        for monkey in monkeys:
            items = ", ".join([str(x) for x in monkey.items])
            m = monkey.monkeynum
            print(f"Monkey {m}: {items}")
        print()

    inspects = []
    for monkey in monkeys:
        num = monkey.monkeynum
        i = monkey.inspected
        print(f"Monkey {num} inspected {i} things")
        inspects.append(i)

    inspects.sort()
    result = inspects[-2] * inspects[-1]

    print()
    print("Result:", result)

    return result

def part2(input):
    import math
    monkeys = []

    for chunkymonkey in chunks(input):
        monkey = Monkey(chunkymonkey)
        monkeys.append(monkey)


    divs = [monkey.divisor for monkey in monkeys]

    total = math.prod(divs)
    print(f"Divisor {total} ({', '.join([str(d) for d in divs])})")

    for monkey in monkeys:
        monkey.modulus = total

    for round in range(1, 10001):

        for monkey in monkeys:
            monkey.throwShit(monkeys)
        
        if round in [1, 20] or round%1000==0:
            print(f"== After round {round} ==")
            for monkey in monkeys:
                i = monkey.inspected
                m = monkey.monkeynum
                print(f"Monkey {m} inspected items {i} times.")
            print()

    inspects = []
    for monkey in monkeys:
        num = monkey.monkeynum
        i = monkey.inspected
        print(f"Monkey {num} inspected {i} things")
        inspects.append(i)

    inspects.sort()
    result = inspects[-2] * inspects[-1]

    print()
    print("Result:", result)

    return result



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
        print("PART 1")
        print("======")
        print(part1(input))

    if run1 and run2:
        print()

    if run2:
        print("PART 2")
        print("======")
        print(part2(input))