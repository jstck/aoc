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
def vprint(*args) -> None:
    if args[0]<= verbosity:
        print(*args[1:])

test_cases = [
    {
        "input": """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32""",
        "output": 152,
        "output2": 301
    }
]


def readmonkeys(input) -> dict[str,Union[int,list[tuple[str,str,str]]]]:
    monkeys = {}
    for line in input:
        (monkey, operation) = line.strip().split(":")
        try:
            x = int(operation.strip())
            monkeys[monkey] = x
        except ValueError:
            (m1, operand, m2) = operation.strip().split(" ")
            if not operand in "+-*/":
                print("UNKNOWN OPERAND:", operand)
            monkeys[monkey] = (operand, m1, m2)
        
    return monkeys

        
def calcmonkey(monkeyid: str, monkeys: dict, humn=None) -> int:
    
    if monkeyid=="humn" and humn is not None:
        return humn

    monkeh = monkeys[monkeyid]

    if isinstance(monkeh,int):
        return monkeh

    (op, m1, m2) = monkeh

    m1 = calcmonkey(m1, monkeys, humn)
    m2 = calcmonkey(m2, monkeys, humn)
    result = -9999
    if op == "+": result = m1+m2
    elif op == "-": result = m1-m2
    elif op == "*": result = m1*m2
    elif op == "/":
        result = m1/m2
        if m1 % m2 != 0:
            pass
    else:
        print("VAFAN", op)
    
    #Apparently caches aint needed
    #monkeys[monkeyid] = result

    return result

def part1(input: list[str]):
    monkeys = readmonkeys(input)
    return calcmonkey("root", monkeys)

def sign(x):
    if x>0: return 1
    if x<0: return -1
    return 0

def part2(input: list[str]):
    monkeys: dict[str,Union[int,list]] = readmonkeys(input)
    root = monkeys["root"]

    _, left, right = root

    #We somehow know right side never changes
    rval = calcmonkey(right, monkeys)

    #We somehow know these values produce results where left side is "too large" or "too small"
    lower = 0
    upper = 291425799367130

    if tests:
        upper = 1000

    d_lower = calcmonkey(left, monkeys, humn=lower)-rval
    d_upper = calcmonkey(left, monkeys, humn=upper)-rval

    while True:
        mid = (lower+upper) // 2

        print("Searching: ", mid)

        mid_val = calcmonkey(left, monkeys, humn=mid)-rval
        if mid_val == 0:
            return mid

        if sign(mid_val) == sign(d_lower):
            lower = mid
            d_lower = mid_val
        else:
            upper = mid
            d_upper = mid_val
        
    


def fixInput(raw: str) -> list[str]:
    lines = [x.strip() for x in raw.strip().split("\n")]

    #Remove trailing blank lines
    while len(lines[-1])==0:
        lines.pop()
    return lines

if tests:

    success = True

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