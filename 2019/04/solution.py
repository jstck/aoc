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


def validpassword(p: int) -> bool:
    double = False

    digits = list(str(p))

    for i in range(len(digits)-1):
        d1 = digits[i]
        d2 = digits[i+1]

        if d1 > d2:
            return False
        if d1 == d2:
            double = True

    return double

def validpassword2(p: int) -> bool:
    double = False

    digits = list(str(p))

    repeats = 0

    for i in range(len(digits)-1):
        
        d1 = digits[i]
        d2 = digits[i+1]

        #print(i,d1,d2,repeats)

        if d1 > d2:
            return False
        if d1 == d2:
            repeats += 1
        else: #d1 < d2
            #Non repeat, reset it
            if repeats == 1:
                #print(f"valid repeat found, i {i}  {d1,d2} ")
                double = True
            repeats = 0

    if repeats == 1:
        double = True

    return double


if __name__ == "__main__":

    tests1 = [111111, 223450, 123789]
    tests2 = [112233, 123444, 111122]

    print("Part 1 tests:")
    for t1 in tests1:
        print(t1, validpassword(t1))

    print("Part 2 tests:")
    for t2 in tests2:
        print(t2, validpassword2(t2))
    print()

    a,b = 273025, 767253

    count = 0
    count2 = 0

    for p in range(a,b+1):
        if validpassword(p):
            count += 1
        if validpassword2(p):
            count2 += 1

    print("Part 1:", count)
    print("Part 2:", count2)