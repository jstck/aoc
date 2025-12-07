#!/usr/bin/env python3

from functools import reduce
from typing import Callable

import sys


sys.path.append("../..")
from lib.aoc import *

def operators(op) -> Callable[[int,int], int]:
    if op=="+":
        return lambda x,y: x+y
    elif op=="*":
        return lambda x,y: x*y
    else:
        assert False


def part1(input: list[str]):
    numbers = [[int(x) for x in line.split()] for line in input[:-1]]
    operations = input[-1].split()

    length = len(operations)

    total1 = 0
    for n in numbers:
        assert len(n) == length

    for i in range(length):
        operands = [n[i] for n in numbers]
        op = operations[i]

        result = reduce(operators(op), operands)

        total1 += result
    return total1

def part2(input: list[str]):
    total = 0

    operations = input[-1]

    #The leftmost digits of any problem operands are always in same column as operator
    #Step through and look for those
    for i in range(len(operations)):
        if operations[i]==" ": continue

        op = operations[i]

        operands = []
        #Step through numbers in this column to build an operand, until there is one with all spaces
        for j in range(10): #Max sensible length, seems to actually be 4
            digits = "".join([line[i+j] for line in input[:-1]]).strip()
            if len(digits) == 0: #All spaces
                break
            else:
                operands.append(int(digits))

        result = reduce(operators(op), operands)
        total += result

    return total


if __name__ == "__main__":
    #Remove newlines, but make sure there's a safety whitespace at the end
    input = [line.rstrip("\n") + " " for line in sys.stdin.readlines() if len(line.strip())> 0]

    p1 = part1(input)
    print("Part 1:", p1)

    p2 = part2(input)
    print("Part 2:", p2)
