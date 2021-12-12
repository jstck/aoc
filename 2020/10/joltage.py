#!/usr/bin/env python3

import sys
import re

adapters = [int(x.strip()) for x in sys.stdin.readlines()]

adapters.sort()

adapters = [0] + adapters + [adapters[-1]+3]

steps = []
for i in range(0, len(adapters)-1):
    steps += [adapters[i+1]-adapters[i]]

ones = steps.count(1)
threes = steps.count(3)

print("1:", ones)
print("3:", threes)
print("Result:", ones*threes)
