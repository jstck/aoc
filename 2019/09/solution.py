#!/usr/bin/env python3

import functools
from functools import cache
from itertools import combinations
import itertools
import collections
from queue import PriorityQueue
import heapq
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

import math
import re
import sys

from IntCodeVM import IntCodeVM

sys.path.append("../..")
from lib.aoc import *


def part1(program: list[int]) :
    vm = IntCodeVM(program, [1], False)
    try:
        vm.run()
    except Exception as e:
        print("EXCEPTION OCCURED")
        print(f"{type(e).__name__}: {e}")
        print()
        vm.dump()
        sys.exit(1)

    out = []
    while vm.has_output():
        out.append(vm.get_output())

    return ",".join(map(str,out)) #+ " STATE: " + str(vm.state)

def part2(program: list[int]):
    vm = IntCodeVM(program, [2], False)
    try:
        vm.run()
    except Exception as e:
        print("EXCEPTION OCCURED")
        print(f"{type(e).__name__}: {e}")
        print()
        vm.dump()
        sys.exit(1)

    out = []
    while vm.has_output():
        out.append(vm.get_output())

    return ",".join(map(str,out)) #+ " STATE: " + str(vm.state)


if __name__ == "__main__":
    programs = []
    for p in sys.stdin.readlines():
        programs.append([int(i.strip()) for i in p.split(',')])

    print("Part 1:")
    for program in programs:
        print(part1(program))

    print("Part 2:")
    for program in programs:
        print(part2(program))
