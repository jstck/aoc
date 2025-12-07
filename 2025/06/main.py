#!/usr/bin/env python3

from functools import reduce

import sys


sys.path.append("../..")
from lib.aoc import *

def part1(input: list[str]):
    numbers = [[int(x) for x in line.split()] for line in input[:-1]]
    operations = input[-1].split()

    length = len(operations)

    total1 = 0
    for n in numbers:
        assert len(n) == length

    for i in range(length):
        operands = [n[i] for n in numbers]
        operator = operations[i]
        print(operator, operands)
        if operator=="+":
            op = lambda x,y: x+y
        elif operator=="*":
            op = lambda x,y: x*y
        else:
            assert False

        result = reduce(op, operands)

        total1 += result
    return total1

def part2(input: list[str]):
    total = 0

    operators = input[-1]

    #The leftmost digits of any problem operands are always in same column as operator
    #Step through and look for those
    for i in range(len(operators)):
        if operators[i]==" ": continue

        operator = operators[i]

        if operator=="+":
            op = lambda x,y: x+y
        elif operator=="*":
            op = lambda x,y: x*y
        else:
            assert False

        operands = []
        #Step through numbers in this column to build an operand, until there is one with all spaces
        for j in range(10): #Max sensible length, seems to actually be 4
            digits = "".join([line[i+j] for line in input[:-1]]).strip()
            print(digits)
            if len(digits) == 0: #All spaces
                break
            else:
                operands.append(int(digits))

        result = reduce(op, operands)
        total += result


    return total


if __name__ == "__main__":
    #Remove newlines, but make sure there's a safety whitespace at the end
    input = [line.rstrip("\n") + " " for line in sys.stdin.readlines() if len(line.strip())> 0]
    print(input)

    p1 = part1(input)
    print("Part 1:", p1)

    p2 = part2(input)
    print("Part 2:", p2)
