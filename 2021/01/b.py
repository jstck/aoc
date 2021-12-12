#!/usr/bin/env python3

import sys

prevdepth = -1000

count = 0

values = [int(line.strip()) for line in sys.stdin]

#print(values)

sums = []

for i in range(2, len(values)):
    sums.append(values[i-2] + values[i-1] + values[i])

#print(sums)

for x in sums:
    if x > prevdepth and not prevdepth<0:
        count += 1

    prevdepth = x

print(count)
