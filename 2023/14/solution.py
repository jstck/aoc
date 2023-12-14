#!/usr/bin/env python3

import sys


sys.path.append("../..")
from lib.aoc import *

def getcol(grid: list[str], i) -> str:
    assert(i < len(grid[0]))

    return "".join([row[i] for row in grid])

def transpose(grid: list[str]) -> list[str]:
    size_x = len(grid[0])
    return [getcol(grid, i) for i in range(size_x)]


def rotate(grid: list[str]) -> list[str]:
    #Transpose, go by columns in reverse order
    size_x = len(grid[0])
    return [getcol(grid, size_x-i) for i in range(size_x)]


def packrocks(s: str) -> str:
    parts = s.split("#")
    newparts = []

    for p in parts:
        rocks = p.count("O")
        empty = p.count(".")
        newparts.append("O" * rocks + "."*empty)

    return "#".join(newparts)

def strrev(s: str) -> str:
    return s[::-1]

def spin(grid: list[str]) -> list[str]:

    #North
    grid = transpose(grid)
    for i, row in enumerate(grid):
        grid[i] = packrocks(row)
    grid = transpose(grid)

    #West
    for i, row in enumerate(grid):
        grid[i] = packrocks(row)

    #South
    grid = transpose(grid[::-1])
    for i, row in enumerate(grid):
        grid[i] = packrocks(row)
    grid = transpose(grid)[::-1]

    #East
    for i, row in enumerate(grid):
        grid[i] = strrev(packrocks(strrev(row)))

    return grid

#String representation of a grid for dict keys, can be split back to original grid
def cache_key(input: list[str]) -> str:
    return "|".join(input)

def load(grid: list[str]) -> int:
    weight = 0
    totalrows = len(grid)

    for i, row in enumerate(grid):
        factor = totalrows - i

        weight += factor * row.count("O")

    return weight


def part1(input: list[str]):

    #Transpose grid, moving rocks right to left per row instead
    grid = transpose(input)


    for i, row in enumerate(grid):
        grid[i] = packrocks(row)

    return load(transpose(grid))



def part2(input: list[str]):

    #Map "resulting grid" with number of cycles
    cache: dict[str,int] = {}

    cache[cache_key(input)] = 0

    grid = input
    limit = 1_000_000_000

    i=0
    cycle_start = 0
    cycle_end = 0
    while i<limit:
        i+=1
        grid = spin(grid)

        key = cache_key(grid)
        
        if key in cache:
            #print(f"Cycle found at {i} == {cache[key]}")
            cycle_start = cache[key]
            cycle_end = i
            break
        else:
            cache[key] = i
    
    cycle_length = cycle_end - cycle_start

    assert(cycle_length > 0)

    #How many more cycles?
    rounds_left = limit - cycle_end
    cycles_left = rounds_left // cycle_length
    r = cycle_end + cycles_left * cycle_length
    final_rounds = limit - r
    final_state = cycle_start + final_rounds

    #Find final state in cache
    for k, v in cache.items():
        if v == final_state:
            return load(k.split("|"))
        
    assert False, f"Cached state not found for {final_state}"


if __name__ == "__main__":
    input = readinput()

    p1 = part1(input)
    print("Part 1:", p1)

    p2 = part2(input)
    print("Part 2:", p2)