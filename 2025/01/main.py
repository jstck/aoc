#!/usr/bin/env python3

import sys, math

dial = 50

zcount = 0
cross = 0

for l in sys.stdin.readlines():

    l = l.strip()
    if len(l) == 0:
        continue
    d = l[0]

    n = int(l[1:])

    olddial = dial

    if d == "L":
        dial -= n
    elif d == "R":
        dial += n

    #Count if it crosses zero (or lands at 100 going to the right)
    crossy = dial // 100


    #If it was at zero and going left, count one less
    if crossy < 0 and olddial == 0:
        crossy += 1

    cross += abs(crossy)
    

    dial %= 100
    if dial == 0 and d == "L":
        cross += 1

    if dial == 0:
        zcount += 1

    print(f"{d}{n}: {olddial} -> {dial} ({crossy})")


print(f"Part A: {zcount}")
print(f"Part B: {cross}")