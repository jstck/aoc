#!/usr/bin/env python3

import sys
import re

timestamp = int(sys.stdin.readline().strip())

buses = [int(bus) for bus in sys.stdin.readline().strip().split(",") if not bus=='x']

print(timestamp)
print(buses)

bestuntil = 0
bestbus = None

for bus in buses:
    since = timestamp%bus   #Minutes since last departure
    until = bus-since       #Minutes until next departure

    print(bus, since, until)

    if bestbus is None or until < bestuntil:
        bestbus = bus
        bestuntil = until

print("Best bus is", bestbus, "which departs in", bestuntil, "minutes")
print("Result: ", bestbus*bestuntil)