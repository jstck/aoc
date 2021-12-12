#!/usr/bin/env python3

import sys
import re

adapters = [int(x.strip()) for x in sys.stdin.readlines()]

adapters.sort()

#Add start and end
adapters = [0] + adapters + [adapters[-1]+3]

steps = []
for i in range(0, len(adapters)-1):
    steps += [adapters[i+1]-adapters[i]]

stepstr = "".join([str(x) for x in steps])

#Split on 3's to get all sequences of 1's
onechunks = stepstr.split("3")

runs = [len(s) for s in onechunks if len(s) >= 3]

print(runs)

#Each run of 3 gives 8 options, each run of 4 gives 7
threes = runs.count(3)
fours = runs.count(4)

print("3:", threes, ", 4:", fours)

result = 8**threes * 7**fours

print(result)