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

modules = [int(l.strip()) for l in sys.stdin.readlines()]

def mass_to_fuel(mass):
    return max((mass // 3)-2, 0)

def mass_to_fuel2(mass):
    f = (mass // 3)-2
    if f>0:
        return f + mass_to_fuel2(f)
    return 0

if part1:
    print(sum(map(mass_to_fuel, modules)))

if part2:
    print(sum(map(mass_to_fuel2, modules))
)