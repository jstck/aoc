#!/usr/bin/env python3

import sys


sys.path.append("../..")
from lib.aoc import *


def hash(s: str) -> int:
    value = 0

    for c in list(s):
        value = (value + ord(c))*17%256

    return value

def part1(input: list[str]) -> int:
    tokens = input[0].split(",")

    total = 0

    for token in tokens:
        total += hash(token)

    return total

def part2(input: list[str]) -> int:

    #Init empty boxes
    boxes = [ [] for _ in range(256)]

    ops = input[0].split(",")

    for op in ops:
        if "=" in op:
            #Replace lens, or add new one at the end
            (newlabel, newval) = op.split("=")
            newval = int(newval)

            box = boxes[hash(newlabel)]

            replaced = False
            for i, (label, _) in enumerate(box):
                if newlabel==label:
                    replaced = True
                    box[i] = (label, newval)
                    break
            if not replaced:
                box.append((newlabel, newval))

        elif "-" in op:
            #Remove a lens
            newlabel = op[:op.find("-")]

            box = boxes[hash(newlabel)]

            for i, (label, _) in enumerate(box):
                if newlabel==label:
                    del box[i]
                    break


    #Determine focusing power
    power = 0
    for b in range(256):
        box = boxes[b]

        for i, (label, val) in enumerate(box):
            power += (b+1) * (i+1) * val

    return power


if __name__ == "__main__":

    input = readinput()

    #print(harsh("HASH"))
    
    p1 = part1(input)
    print("Part 1:", p1)

    p2 = part2(input)
    print("Part 2:", p2)