#!/usr/bin/env python3

from functools import cache
import sys

sys.path.append("../..")
from lib.aoc import *

#Keep graph global because simple stupid
graph: dict[str,list[str]] = {}


@cache
def dfs_paths(start: str, end: str) -> int:
    if start == end:
        return 1
    
    return sum([dfs_paths(next, end) for next in graph[start]])

def part1() -> int:
    return dfs_paths("you", "out")

def part2() -> int:
    
    searchy1 = [("svr", "fft"),("fft","dac"),("dac","out")]
    searchy2 = [("svr", "dac"),("dac","fft"),("fft","out")]

    paths = [ ["svr", "fft", "dac", "out"], ["svr", "dac", "fft", "out"]]
    sum = 0

    # Multiply the number of subpaths together, and sum them.
    # One of the paths dac->fft and fft->dac will be zero. If not, there would be a loop
    # and answer would be infinity.
    for path in paths:
        x = 1
        for start,end in zip(path, path[1:]):
            c = dfs_paths(start,end)
            x *= c
            # if x==0: break
        sum += x
    return sum

if __name__ == "__main__":
    input = readinput()

    for line in input:
        a, b = line.split(":")
        a = a.strip()
        b = b.split()
        graph[a] = b

    # Add empty out node for safety (so paths searched in part 2 can end there)
    graph["out"] = []

    #print(graph)

    try:
        p1 = part1()
        print("Part 1:", p1)
    except:
        print("Input does not work for part 1")

    try:
        p2 = part2()
        print("Part 2:", p2)
    except:
        print("Input does not work for part 2")

