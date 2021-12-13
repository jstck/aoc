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


#Parse set of dots
dots = set()

while sys.stdin:
    line = sys.stdin.readline().strip()
    if len(line) == 0:
        break

    (x, y) = [int(n.strip()) for n in line.split(",",1)]
    dots.add((x,y))

vprint(1,dots)

#Parse list of folds
folds = []

for line in sys.stdin.readlines():
    stuff = line.strip().split(" ")
    fold = stuff[-1].split("=")
    folds.append((fold[0], int(fold[1])))

vprint(1, folds)

def foldX(s, c):
    newset = set()
    for (x, y) in s:
        if x==c:
            #No dots should be at fold, really
            vprint(0, "DOT AT FOLD (X=%d): %d %d" % (c, x, y))
            continue
        if x>c:
            x = 2*c-x

        newset.add((x,y))

    return newset


def foldY(s, c):
    newset = set()
    for (x, y) in s:
        if y==c:
            #No dots should be at fold, really
            vprint(0, "DOT AT FOLD (Y=%d): %d %d" % (c, x, y))
            continue
        if y>c:
            y = 2*c-y

        newset.add((x,y))
    
    return newset

if part1:
    (axis, c) = folds[0]

    if axis == "x":
        dots = foldX(dots, c)
    else:
        dots = foldY(dots, c)

    vprint(1, dots)
    print(len(dots), "dots")

if part2:
    for (axis, c) in folds:
        if axis == "x":
            dots = foldX(dots, c)
        else:
            dots = foldY(dots, c)
        vprint(1, "Down to", len(dots), "dots")

    xmax, ymax = 0, 0
    for (x,y) in dots:
        xmax = max(xmax, x)
        ymax = max(ymax, y)

    grid = [ ["."] * (xmax+1) for y in range(ymax+1)]
    for (x, y) in dots:
        grid[y][x] = "#"

    for row in grid:
        print("".join(row))
