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
    c = 1
    for start,end in searchy1:
        x = dfs_paths(start,end)
        #print(f"{start}-{end}: {x}")
        if x==0:
            c = 0
            break
        c *= x
    
    d = 1
    for start,end in searchy2:
        x = dfs_paths(start,end)
        #print(f"{start}-{end}: {x}")
        if x==0:
            d = 0
            break
        d *= x
    
    return c+d

if __name__ == "__main__":
    input = readinput()

    for line in input:
        a, b = line.split(":")
        a = a.strip()
        b = b.split()
        graph[a] = b

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

