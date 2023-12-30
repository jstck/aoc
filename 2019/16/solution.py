#!/usr/bin/env python3
from __future__ import annotations

from functools import cache
from itertools import combinations, permutations
import collections
from queue import PriorityQueue, SimpleQueue
from collections import defaultdict, deque, Counter, OrderedDict
import heapq
from dataclasses import dataclass
import math
import re
import sys
from typing import TypeAlias, Optional, Iterator
from operator import mul

import math
import re
import sys


sys.path.append("../..")
from lib.aoc import *

@cache
def pattern(n: int, size: int) -> list[int]:
    basepattern = [0, 1, 0, -1]
    res = []
    for count in range(size):
        pos = ((count+1)//(n+1))%4
        res.append(basepattern[pos])
    return res

#Do one pass of FFT
def FFTpass(input: list[int]) -> list[int]:
    l = len(input)
    r = []
    for i in range(l):
        r.append(abs(sum(map(mul, input, pattern(i,l)))) % 10)
    return r

def FFT(input: list[int], rounds) -> list[int]:
    a = input
    for _ in range(rounds):
        a = FFTpass(a)

    return a


def part1(input: list[int]) -> str:
    res = FFT(input, 100)
    return "".join([str(x) for x in res[:8]])

def part2(input: list[int]) -> int:
    return 0


if __name__ == "__main__":

    sequences = [[int(x) for x in list(line)] for line in readinput()]


    for sequence in sequences:
        p1 = part1(sequence)
        print("Part 1:", p1)

        #p2 = part2(sequence)
        #print("Part 2:", p2)