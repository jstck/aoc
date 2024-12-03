#!/usr/bin/env python3

import sys

with open("input.txt") as fp:
    lines = fp.readlines()


reports = []
safe = 0



def diffs(items):
    res = []
    for i in range(len(items)-1):
        res.append(items[i]-items[i+1])
    return res


def isSafe(items):
    c_up = 0
    c_down = 0
    for i in range(len(items)-1):
        a = items[i]
        b = items[i+1]

        if b-a < 1 or b-a > 3:
            c_up += 1

        if a-b < 1 or a-b > 3:
            c_down += 1

    #if c_up != 0 and c_down != 0:
    #    print(items, c_up, c_down, min(c_up, c_down))

    return min(c_up, c_down) == 0

def isHalfSafe(items):
    for i in range(len(items)):
        newreport = items[:i] + items[i+1:]
        if isSafe(newreport):
            return True
    return False

p1 = p2 = 0

for line in lines:
    line = line.strip()
    parts = list(map(int, line.split()))

    if isSafe(parts):
        p1 += 1
        p2 += 1
    else:
        if isHalfSafe(parts):
            p2 += 1
    
print("part1:", p1)
print("part2:", p2)