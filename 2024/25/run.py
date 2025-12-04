#!/usr/bin/env python3

import sys


sys.path.append("../..")
from lib.aoc import *
from lib.grid import Grid

def part1(input: list[str]):
    return ""

def part2(input: list[str]):
    return ""

def numbrify(grid: Grid[str]) -> list[int]:
    seq = []

    for col in range(grid.size_x):
        for i, s in grid.enumCol(col):
            #Mark at first non-# (minus one to discount first row)
            if s != "#":
                seq.append(i-1)
                break
    return seq

def fits(lock: list[int], key: list[int], space) -> bool:
    for a,b in zip(lock, key):
        if a+b>space:
            return False
    return True

if __name__ == "__main__":

    locks = []
    keys = []
    for thing in chunks(readinput()):
        thing = Grid(thing)
        
        #Check if first row is "solid", then it' a lock
        islock = "." not in thing.row(0)

        #Flip keys upside down to count them
        if not islock:
            thing = thing.flipY()

        sequence = numbrify(thing)

        if islock:
            locks.append(sequence)
        else:
            keys.append(sequence)

    #print(locks)
    #print(keys)

    p1=0

    for lock in locks:
        for key in keys:
            if fits(lock, key, 5):
                #print("Fits:",lock,key)
                p1 += 1    

    print("Part 1:", p1)

