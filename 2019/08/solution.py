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


sys.path.append("../..")
from lib.aoc import *


def part1(sx: int, sy: int, image: str) -> int:
    assert len(image) % (sx*sy)==0, "Invalid image size"

    layer_size = sx*sy
    n_layers = len(image) // layer_size

    print(f"{n_layers} layers of size {layer_size}")

    fewest_zeroes = layer_size+1
    bestscore = 0

    result = ["2"] * layer_size

    for i in range(n_layers):
        start = i*layer_size
        end = (i+1)*layer_size
        layer = image[start:end]

        c = collections.Counter(layer)

        n_zeros = c["0"]

        #print(f"Layer {i} has {n_zeros} zeros")

        #n_ones = c["1"]
        #n_twos = c["2"]
        #score = n_ones * n_twos
        #print(f"Layer {i} has {n_ones} ones and {n_twos} twos, score {score}")


        if n_zeros < fewest_zeroes:
            #print("*** LOWEST YET ***")
            fewest_zeroes = n_zeros
            bestscore = c["1"]*c["2"]

        #print(layer)
        #print()

        for pos, x in enumerate(layer):
            if result[pos] == "2":
                result[pos] = x

    row_len = layer_size // size_y
    for y in range(size_y):
        start = y*row_len
        end = (y+1)*row_len
        row = result[start:end]
        line = "".join(row).replace("0", ".").replace("1", "#")
        print(line)


    return bestscore


if __name__ == "__main__":
    (size_x, size_y) = [int(x) for x in sys.stdin.readline().strip().split()]
    data = sys.stdin.readline().strip()

    print(f"Image size {size_x} X {size_y}")
    print(f"Data size: {len(data)}")

    input = ["foo"]

    p1 = part1(size_x, size_y, data)
    print("Part 1:", p1)
