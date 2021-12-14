#!/usr/bin/env python3

import sys
import argparse
import re
from collections import Counter
from typing import Collection

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

polymer = list(sys.stdin.readline().strip())
sys.stdin.readline()

rules = {}

for line in sys.stdin.readlines():
    (a, b) = [part.strip() for part in line.strip().split('->')]
    rules[a] = b

vprint(2,polymer)
vprint(2,rules)


def polymerize(input, rules):
    output = []
    for i in range(0, len(input)-1):
        pair = input[i] + input[i+1]
        output.append(input[i])
        if pair in rules:
            output.append(rules[pair])

    #Append last character (not matching any new pair)
    output.append(input[-1])            

    return output

if part1:
    length = 10
elif part2:
    length = 40


def chunks(input, rules):
    output = []
    current = []
    for i in range(0, len(input)-1):
        pair = input[i] + input[i+1]
        current.append(input[i])
        if pair not in rules:
            output.append(current)
            current = []
        else:
            pass

    current.append(input[-1])
    output.append(current)
    return output

class myCounter:
    def __init__(self):
        self.counts = {}

    def update(self, item, count):
        if item in self.counts:
            self.counts[item] += count
        else:
            self.counts[item] = count

# input = [l.strip() for l in sys.stdin.readlines()]
vprint(2, "".join(polymer))

if part1:
    for step in range(length):
        
        polymer = polymerize(polymer, rules)
        print(chunks(polymer, rules))
        vprint(1, step, len(polymer))
        vprint(2, "".join(polymer))

    stats = Counter(polymer)

    #All elements in order of commonality
    el_order = [k for k, v in sorted(stats.items(), key=lambda item: item[1])]

    lowcount = stats[el_order[0]]
    highcount = stats[el_order[-1]]
    print(highcount-lowcount)

if part2:
    stats = myCounter()

    #Count
    for c in polymer:
        stats.update(c, 1)
    
    pairs = myCounter()
    for i in range(0, len(polymer)-1):
        pair = polymer[i] + polymer[i+1]
        pairs.update(pair,1)

    vprint(1, stats.counts)
    vprint(2, pairs.counts)

    for step in range(length):


        newpairs = myCounter()

        for key in pairs.counts:
            count = pairs.counts[key]
            if key not in rules:
                print("NOT FOUND IN RULES:", key)
                continue

            dest = rules[key]
            p1 = key[0]+dest
            p2 = dest+key[1]
            vprint(2, "%s -> %s (%d) ; %s %s" % (key, dest, count, p1, p2))

            #New "middle" character is added once per occurence of rule to total count of stuff
            stats.update(dest, count)
            #Both new pairs are added as many times as they appear
            newpairs.update(p1, count)
            newpairs.update(p2, count)

        pairs = newpairs

        vprint(1, stats.counts)
    
    #All elements in order of commonality
    el_order = [k for k, v in sorted(stats.counts.items(), key=lambda item: item[1])]

    lowcount = stats.counts[el_order[0]]
    highcount = stats.counts[el_order[-1]]
    print(highcount-lowcount)