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