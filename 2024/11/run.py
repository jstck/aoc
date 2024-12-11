#!/usr/bin/env python3

from functools import cache
from typing import Iterable, Iterator

import math
import re
import sys


sys.path.append("../..")
from lib.aoc import *

#Naive part 1 solution that just brute forces it all.
def blink(stones: Iterable[int]) -> Iterator[int]:
    
    for stone in stones:
        if stone == 0:
            yield 1
            continue

        s = str(stone)
        l = len(s)
        if l%2==0:
            yield int(s[:l//2])
            yield int(s[l//2:])
        else:
            yield stone*2024

def part1(stones: Iterable[int]) -> int:
    for _ in range(25):
        stones = blink(stones)

    return len(list(stones))


#Does this need to be cached? Probably not. We'll do it anyway.
@cache
def blinkone(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    s = str(stone)
    l = len(s)
    if l%2==0:
        half = l//2
        return [int(s[:half]), int(s[half:])]
    else:
        return [stone*2024]
      
@cache
def blinkc(stone: int, n: int) -> int:
    #After 0 generations, one stone is always one stone.
    if n==0:
        return 1
    
    return sum(blinkc(s,n-1) for s in blinkone(stone))

def stonify(stones: Iterable[int], ngen) -> int:
    return sum([blinkc(stone, ngen) for stone in stones])

if __name__ == "__main__":
    input = readinput()
    stones = list(map(int, input[0].split()))

    p1 = part1(stones)
    print("Part 1: ", p1)

    p1b = stonify(stones, 25)
    print("Part 1b:", p1b)

    p2 = stonify(stones, 75)
    print("Part 2: ", p2)
