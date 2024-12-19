#!/usr/bin/env python3

from functools import cache
import sys


sys.path.append("../..")
from lib.aoc import *

#Global set of towels. Used by everyone, doesn't change.
towels: list[str] = []

@cache
#See if a subpattern can be matched
def matcha(pattern: str) -> bool:
    plen = len(pattern)
    if plen == 0:
        return True

    #Try all possible subpatterns and see if anything matches (exits at first match)
    for t in towels:
        tlen = len(t)
        if pattern[:tlen] == t:
            if matcha(pattern[tlen:]):
                return True
    return False

@cache
def matcha2(pattern: str) -> int:
    if len(pattern) == 0:
        return 1
    
    c = 0

    #Try all subpatterns and count all matches
    for t in towels:
        tlen = len(t)
        if pattern[:tlen] == t:
            c += matcha2(pattern[tlen:])
    return c

#Count how many of the given patterns can even be made
def part1(patterns: list[str]):
    c = 0

    for pattern in patterns:
        if matcha(pattern):
            #print("Funkar: ", pattern)
            c += 1

    return c

#Count how many ways they can be made (sum up subpatterns)
def part2(patterns: list[str]):
    sum = 0

    for pattern in patterns:
        c = matcha2(pattern)

        #print(pattern, c)
        sum += c

    return sum


if __name__ == "__main__":
    (towls, patterns) = chunks(readinput())

    towels = [s.strip() for s in towls[0].split(",")]

    patterns = [s.strip() for s in patterns]

    p1 = part1(patterns)
    print("Part 1:", p1)

    p2 = part2(patterns)
    print("Part 2:", p2)