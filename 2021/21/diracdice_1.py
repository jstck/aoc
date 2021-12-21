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

# input = [l.strip() for l in sys.stdin.readlines()]

positions = [2,5]
score = [0,0]

totalrolls = 0

def dieroll():
    global die, totalrolls
    totalrolls += 1
    return (totalrolls-1)%100+1

pointless = True

while pointless:
    for player in [0,1]:
        rolls = [dieroll(), dieroll(), dieroll()]
        pos = positions[player] + sum(rolls)
        while pos>10:
            pos-=10
        positions[player] = pos
        score[player] += pos
        print("Player %d rolls %d+%d+%d and moves to space %d for a total score of %d." % (player+1, rolls[0],rolls[1],rolls[2],pos,score[player]))
        if score[player] >= 1000:
            pointless=False
            break

print("Result:", min(score)*totalrolls)
        
