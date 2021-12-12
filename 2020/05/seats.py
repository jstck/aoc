#!/usr/bin/env python3

import sys

translation = "BLAHONGA".maketrans("FBLR", "0101")

maxseat=0
minseat=1000

seats = []

for line in sys.stdin:
    line = line.strip()

    binary = line.translate(translation)

    seatid = int(binary, 2)

    maxseat = max(maxseat, seatid)
    minseat = min(minseat, seatid)

    seats.append(seatid)

    #print(line, binary, seatid)
    

print(minseat, maxseat)

#seats.sort()

#print(seats)

for i in range(minseat,maxseat):
    if i not in seats:
        print("Missing seat", i)