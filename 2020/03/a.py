#!/usr/bin/env python3

import sys

y = 0
x = 0

trees = 0

for line in sys.stdin:
    line = line.strip()

    stuff = line[x]
    if stuff == "#":
        trees += 1

    y += 1
    x = (x+3) % len(line)

print(trees)
