#!/usr/bin/env python3

import functools
from functools import cache
from itertools import combinations
import itertools
import collections
from queue import PriorityQueue
import heapq
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Union, Optional

import math
import re
import sys


sys.path.append("../..")
from lib.aoc import *

def part1(input: list[str]):
    return ""

def part2(input: list[str]):
    return ""

variables: Dict[str,bool] = {}
rules = {}
outputs = []

@cache
def evaluate(var: str) -> bool:
    if var in variables:
        return variables[var]

    a,op,b = rules[var]

    aval = evaluate(a)
    bval = evaluate(b)

    if op == "AND":
        res = aval & bval
    elif op == "OR":
        res = aval | bval
    elif op == "XOR":
        res = aval ^ bval
    else:
        print(f"UNKNOWN STUFF: {a} {op} {b} -> {var}")
        assert(False)

    variables[var] = res

    return res



if __name__ == "__main__":
    vars, rools = chunks(readinput())

    for line in vars:
        a,b = line.split(":")
        var = a.strip()
        val = bool(int(b.strip()))
        variables[var] = val

    for line in rools:
        a1, op, a2, arrow, result = line.split()
        assert(arrow=="->")
        assert(op in ["AND", "OR", "XOR"])

        rules[result] = (a1, op, a2)

        if result[0] == "z":
            outputs.append(result)

    #Evaluate stuff from most significant bit first
    outputs.sort(reverse=True)

    p1 = 0

    for z in outputs:
        bit = int(evaluate(z))
        p1 = (p1<<1) + bit

    print("Part 1:", p1)

    #p2 = part2(input)
    #print("Part 2:", p2)
