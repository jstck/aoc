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
        "input": "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
        "output": 7,
        "output2": 19
    },
    {
        "input": "bvwbjplbgvbhsrlpgdmjqwftvncz",
        "output": 5,
        "output2": 23
    },
    {
        "input": "nppdvjthqldpwncqszvftbrmjlhg",
        "output": 6,
        "output2": 23
    },
    {
        "input": "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
        "output": 10,
        "output2": 29
    },
    {
        "input": "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
        "output": 11,
        "output2": 26
    },
    {
        "input": "abcd",
        "output": 4
    },
    {
        "input": "ababababababababababababababababababababababcd",
        "output": 46,
        "output2": -1
    },
    {
        "input": "abcacbcbabcbacbcbcababcbacbcbabcabcbcabcbacb",
        "output": -1
    }
    
]

def findmarker(input, size):

    assert(len(input)>=size)
    for i in range(size, len(input)+1):
        seq = input[i-size:i]
        
        d = len(set(list(seq)))

        if d==size:
            return i

    return -1

def part1(input):
    return findmarker(input, 4)

def part2(input):
    return findmarker(input, 14)




if tests:

    success = True

    for case in test_cases:
        input = case["input"].strip()
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
        fp = open("input.txt", "r")
    except FileNotFoundError:
        fp = sys.stdin
    
    input = fp.readline().strip()

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