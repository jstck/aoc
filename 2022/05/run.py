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
        if len(line.strip()) == 0:
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
        "input": """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2""",
        "output": "CMZ",
        "output2": "MCD"
    }
]




def parse(input):
    parts = chunks(input)

    assert(len(parts)==2)

    stacks = parts[0]
    moves = parts[1]

    labels = stacks[-1]
    stacks = stacks[:-1]

    width = (int(len(labels.strip()))+3)//4

    assert(len(labels.strip().split())==width)

    cargo = []

    for i in range(width):
        cargo.append([])

    for line in stacks:
        for i in range(width):
            pos = 1+i*4
            if pos > len(line):
                continue

            c = line[pos].strip()
            if len(c)>0:
                assert(len(c)==1)
                cargo[i].append(c)

    #print(cargo)

    seq = []

    for move in moves:
        parts = move.split()
        n = int(parts[1])
        f = int(parts[3])-1
        t = int(parts[5])-1

        seq.append((n,f,t))

    #print(seq)

    for stack in cargo:
        stack.reverse()

    return(cargo, seq)


def printstacks(stacks):
    x = ""
    for s in stacks:
        x += str(s) + "\n"
    return x

def part1(input):
    stacks, moves = parse(input)

    vprint(1,printstacks(stacks))


    for (n, src, dst) in moves:
        vprint(2,f"Move {n} from {src} to {dst}:")
        for i in range(n):
            c = stacks[src].pop()
            stacks[dst].append(c)
        vprint(2,printstacks(stacks))
    
    return "".join([s[-1] for s in stacks])

def part2(input):
    stacks, moves = parse(input)

    vprint(1,printstacks(stacks))


    for (n, src, dst) in moves:
        vprint(2,f"Move {n} from {src} to {dst}:")
        c = stacks[src][-n:]
        stacks[src] = stacks[src][:-n]
        stacks[dst].extend(c)
        vprint(2,printstacks(stacks))
    
    return "".join([s[-1] for s in stacks])


if tests:


    def splitLines(input):
        return [x for x in input.split("\n")]

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
    
    input = [x for x in fp.readlines()]

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