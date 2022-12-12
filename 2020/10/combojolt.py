#!/usr/bin/env python3

import sys
import re

adapters = [int(x.strip()) for x in sys.stdin.readlines()]

adapters.sort()

#Add start and end
adapters = [0] + adapters + [adapters[-1]+3]

print(adapters)

steps = []
for i in range(0, len(adapters)-1):
    steps += [adapters[i+1]-adapters[i]]

stepstr = "".join([str(x) for x in steps])

#Split on 3's to get all sequences of 1's
onechunks = stepstr.split("3")

print(onechunks)

runs = [len(s) for s in onechunks if len(s) >= 2]

print(runs)

#Each run of 3 gives 4 options, each run of 4 gives 7, each run of 2 gives 2
threes = runs.count(3)
fours = runs.count(4)
twos = runs.count(2)

print("2:", twos, "3:", threes, ", 4:", fours)

result = (2**twos) * (4**threes) * (7**fours)

print(result)