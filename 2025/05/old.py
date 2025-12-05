#!/usr/bin/env python3

import sys


sys.path.append("../..")
from lib.aoc import *

def isfresh(ingredient, ranges) -> bool:
    for (lower,upper) in ranges:
        if ingredient >= lower and ingredient <= upper:
            return True
    return False

def part1(ingredients, ranges) -> int:
    fresh = 0
    for i in ingredients:
        if isfresh(i, ranges):
            fresh += 1

    return fresh

#Check if two ranges overlap
def overlaps(r1: tuple[int,int], r2: tuple[int,int]) -> bool:
    a1, b1 = r1
    a2, b2 = r2

    if a1 >= a2 and a1 <= b2: return True
    if b1 >= a2 and b1 <= b2: return True
    if a2 >= a1 and a2 <= b1: return True
    if b1 >= a2 and b1 <= b2: return True
    return False
    
#Merge two ranges (assumed to overlap)
def merge(r1: tuple[int,int], r2: tuple[int,int]) -> tuple[int,int]:
    a1, b1 = r1
    a2, b2 = r2

    a = min(a1,a2)
    b = max(b1,b2)

    return (a,b)

#Do one pass of range deduplication/merging
def deduplicate(ranges: list[tuple[int,int]]) -> list[tuple[int,int]]:
    newranges: list[tuple[int,int]] = []

    for i in range(0, len(ranges)):
        a = ranges[i]

        #Previously marked as don't keep
        if a[0]<0:
            continue 

        merged = False

        for j in range(i+1, len(ranges)):
            b = ranges[j]

            if overlaps(a,b):
                #print("Overlap",a,b,merge(a,b))

                newranges.append(merge(a,b))
                merged = True
                ranges[j] = (-1,-1)

        #This one didn't overlap anything, keep it as is
        if not merged:
            newranges.append(a)

    return newranges

#Keep deduplicating until it can't go further
def deduplicateAll(ranges: list[tuple[int,int]]) -> list[tuple[int,int]]:
    newlen, oldlen = 0,1

    while newlen != oldlen:
        oldlen = len(ranges)
        ranges = deduplicate(ranges)
        newlen = len(ranges)

    return ranges


def part2(ranges) -> int:
    ranges = deduplicateAll(ranges[:])

    #Since ranges are now not overlapping, just sum up the lengths of each
    total = 0

    for (a,b) in ranges:
        total += (b-a+1)    
    return total


if __name__ == "__main__":
    (ranges, ingredients) = chunks(readinput())

    ranges = [tuple([int(x) for x in p.split("-")]) for p in ranges]
    ingredients = [int(x) for x in ingredients]

    #Various assumptions about input
    for (a,b) in ranges:
        assert a<=b
        assert a>0
        assert b>0

    p1 = part1(ingredients, ranges)
    print("Part 1:", p1)

    p2 = part2(ranges)
    print("Part 2:", p2)
