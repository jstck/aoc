#!/usr/bin/env python3

import sys
sys.path.append("../..")
from lib.aoc import *
from collections import defaultdict

def solve(result, accumulator, operands):
    if len(operands)==0:
        return result == accumulator
    if accumulator > result:
        return False
    
    first, rest = operands[0], operands[1:]

    mult = solve(result, accumulator*first, rest)
    add = solve(result, accumulator+first, rest)

    return mult or add

def part1(calibrations) -> int:
    sum = 0
    for (result, operands) in calibrations:
        first, rest = operands[0], operands[1:]
        if solve(result, first, rest):
            sum += result

    return sum


def solve2(result, accumulator, operands):
    if len(operands)==0:
        return result == accumulator
    if accumulator > result:
        return False
    
    first, rest = operands[0], operands[1:]

    #Multiplication
    if solve2(result, accumulator*first, rest):
        return True
    
    #Addition
    if solve2(result, accumulator+first, rest):
        return True
    
    #Concatenation:
    if solve2(result, int(str(accumulator)+str(first)), rest):
        return True


def part2(calibrations) -> int:
    sum = 0
    for (result, operands) in calibrations:
        first = operands[0]
        rest = operands[1:]
        if solve2(result, first, rest):
            #print("Solved", result)
            sum += result

    return sum


if __name__ == "__main__":

    calibrations = []

    for line in readinput():
        result, operands = line.split(":")
        result = int(result)
        operands = list(map(int, operands.strip().split(" ")))
        calibrations.append((result, operands))

    print("Part 1:", part1(calibrations))
    print("Part 2:", part2(calibrations))