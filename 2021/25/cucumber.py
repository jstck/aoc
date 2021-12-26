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
parser.add_argument('--verbose', '-v', action='count', default=0, help="Increase verbosity")

args = parser.parse_args()

part2 = vars(args)["2"]
part1 = vars(args)["1"] or not part2 #Do part 1 if not part 2 specified
verbosity = vars(args)["verbose"]

#Print controlled by verbosity level
def vprint(*args):
    if args[0]<= verbosity:
        print(*args[1:])

#for line in sys.stdin.readlines():
#    pass


grid = [list(l.strip()) for l in sys.stdin.readlines()]


def moverow(r):
    row = grid[r]
    cols = len(row)
    i0 = row[0]
    moved = False
    skip = False
    for i in range(cols-1):
        if not skip and row[i]=='>' and row[i+1]=='.':
            row[i+1] = '>'
            row[i] = '.'
            moved = True
            skip = True
        else:
            skip = False

    #Wraparound
    if not skip and row[cols-1]=='>' and i0=='.':
        row[0] = '>'
        row[cols-1] = '.'
        moved = True
    return moved

def moveright():
    moved = False
    for r in range(len(grid)):
        moved = moverow(r) or moved
    return moved


def movecol(c):
    rows = len(grid)
    i0 = grid[0][c]
    moved = False
    skip = False
    for i in range(rows-1):
        if not skip and grid[i][c]=='v' and grid[i+1][c]=='.':
            grid[i+1][c] = 'v'
            grid[i][c] = '.'
            moved = True
            skip = True
        else:
            skip = False
    if not skip and grid[rows-1][c]=='v' and i0=='.':
        grid[0][c] = 'v'
        grid[rows-1][c] = '.'
        moved = True

    return moved

def movedown():
    moved = False
    for c in range(len(grid[0])):
        moved = movecol(c) or moved
    return moved


def printgrid():
    print("\n".join("".join(row) for row in grid))
    print(count,moved)
    print()

moved = True
count=0
while moved:
    moved = moveright()
    moved = movedown() or moved
    count += 1
    if verbosity>0:
        printgrid()
print(count)