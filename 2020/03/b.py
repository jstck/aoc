#!/usr/bin/env python3

import sys
import math

y = 0
trees = [0, 0, 0, 0, 0]

x = [0, 0, 0, 0, 0]

k = [1, 3, 5, 7, 1]

for line in sys.stdin:
    line = line.strip()

    for i in range(0, 5):
        if i==4 and y%2 != 0:
            continue
        if line[x[i]] == "#":
            trees[i] += 1
        x[i] = (x[i] + k[i]) % len(line)

    y += 1

print(trees)
print(math.prod(trees))
