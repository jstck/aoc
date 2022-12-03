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
        "input": """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""",
        "output": 157,
        "output2": 70
    }
]

def part1(input):
    sum = 0
    for line in input:
        
        halva = len(line)//2

        r1 = line[0:halva]
        r2 = line[halva:]

        s1 = set(list(r1))
        s2 = set(list(r2))

        i = s1 & s2
        
        c = list(i)[0][0] #first char of first item in set

        if c.islower():
            score = 1+ord(c)-ord('a')
        elif c.isupper():
            score = 27+ord(c)-ord('A')
        else:
            print("ERROR", c)
            sys.exit(1)

        vprint(1, c, score)
        sum += score

    return sum

def part2(input):
    lines = len(input)
    groups = lines//3
    sum = 0

    for n in range(groups):
        l1, l2, l3 = input[n*3:n*3+3]
        #vprint(1,n,len(l1), len(l2),len(l3))

        s1 = set(list(l1))
        s2 = set(list(l2))
        s3 = set(list(l3))

        i = s1 & s2 & s3
        c = list(i)[0][0]


        if c.islower():
            score = 1+ord(c)-ord('a')
        elif c.isupper():
            score = 27+ord(c)-ord('A')
        else:
            print("ERROR", c)
            sys.exit(1)

        vprint(1, c, score)
        sum += score

    return sum






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