#!/usr/bin/env python3

import sys


sys.path.append("../..")
from lib.aoc import *
from lib.intervalset import IntervalSet

def part1(ingredients: list[int], intervals: IntervalSet) -> int:
    fresh = 0
    for i in ingredients:
        if intervals.contains(i):
            fresh += 1

    return fresh

def part2(intervals: IntervalSet) -> int:
    #Since ranges are now not overlapping, just sum up the lengths of each
    total = 0

    for (a,b) in intervals.intervals():
        total += (b-a+1)    
    return total


if __name__ == "__main__":
    intervals = IntervalSet()

    (ranges, ingredients) = chunks(readinput())

    ranges = [tuple([int(x) for x in p.split("-")]) for p in ranges]
    ingredients = [int(x) for x in ingredients]

    #Various assumptions about input
    for (a,b) in ranges:
        assert a<=b
        assert a>0
        assert b>0

    for r in ranges:
        intervals.add(r)

    p1 = part1(ingredients, intervals)
    print("Part 1:", p1)

    p2 = part2(intervals)
    print("Part 2:", p2)
