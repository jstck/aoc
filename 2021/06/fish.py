#!/usr/bin/env python3

import sys

fishes = [int(f.strip()) for f in sys.stdin.readline().strip().split(",")]

fishstate = [0]*9

for fish in fishes:
    fishstate[fish] += 1

for day in range(256):
    newfish = fishstate[0]
    fishstate = fishstate[1:]
    fishstate[6] += newfish
    fishstate.append(newfish)
    print(day+1,fishstate,sum(fishstate))