#!/usr/bin/env python3

import sys
import argparse
import re
import functools

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
        "input": "FILE:sample.txt",
        "output": 13,
        "output2": 140
    }
]


def compare(part1, part2):
    if isinstance(part1, int) and isinstance(part2, int):
        if isinstance(part2, int):
            if part1 < part2:
                return True
            if part1 > part2:
                return False
            return None

    if isinstance(part1, int):
        part1 = [part1]
    if isinstance(part2, int):
        part2 = [part2]

    for i in range(len(part1)):

        if i >= len(part2):
            #Ran out of part2, identical so far, wrong order
            return False

        item1 = part1[i]
        item2 = part2[i]

        c = compare(item1, item2)
        if c is None:
            continue
        return c

    #Lists are identical so far but part1 is shorter
    if len(part1) < len(part2):
        return True
    
    #Identical
    return None

def compare2(part1, part2):
    c = compare(part1, part2)
    if c is None:
        return 0
    if c:
        return -1
    return 1

def part1(input):
    count = 0
    sum = 0

    print(compare([1], [2]))
    print(compare([2], 2))
    print(compare(3, [2]))

    for chunk in chunks(input):
        count += 1
        line1 = chunk[0]
        line2 = chunk[1]

        packet1 = eval(line1)
        packet2 = eval(line2)

        c = compare(packet1, packet2) 

        if c or (c is None):
            print(f"{count:3} - correct")
            sum += count
        else:
            print(f"{count:3} - incorrect")

    return sum

def part2(input):
    packets = []
    for line in input:
        if len(line) == 0:
            continue

        packet = eval(line)
        packets.append(packet)

    packets.append([[2]])
    packets.append([[6]])

    packets.sort(key=functools.cmp_to_key(compare2))

    divider1 = packets.index([[2]])+1
    divider2 = packets.index([[6]])+1

    return divider1*divider2



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