#!/usr/bin/env python3


import sys


crabs = [int(f.strip()) for f in sys.stdin.readline().strip().split(",")]

a = min(crabs)
b = max(crabs)


bestfuel = 0
bestpos = -1

for target in range(a,b+1):

    fuel = [abs(x-target) for x in crabs]

    fuelsum = sum(fuel)

    print("Pos", target, "fuel", fuelsum)

    if bestpos < 0 or fuelsum < bestfuel:
        bestpos = target
        bestfuel = fuelsum

print("Min fuel", bestfuel, "at", bestpos)