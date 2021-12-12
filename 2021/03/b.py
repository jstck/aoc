#!/usr/bin/env python3

import sys

lines = [l.strip() for l in sys.stdin.readlines()]

#print(lines)

size = len(lines[0])

o2_lines = lines
co2_lines = lines

pos=0
while len(o2_lines) > 1 and pos<size:
    zeros = [0] * size
    ones = [0] * size
    for line in o2_lines:
        for i in range(0, size):
            digit = line[i]
            if digit == "0":
                zeros[i] += 1
            elif digit == "1":
                ones[i] += 1
            else:
                raise Exception("WEIRD DIGIT %s", digit)

    if zeros[pos] > ones[pos]:
        keep="1"
    else:
        keep="0" #Equal = keep 0

    o2_lines = [x for x in o2_lines if x[pos]==keep]
    #print(o2_lines)
    pos += 1

o2_rating = int(o2_lines[0],2)
print("Oxygen rating:", o2_rating)


pos=0
while len(co2_lines) > 1 and pos<size:
    zeros = [0] * size
    ones = [0] * size
    for line in co2_lines:
        for i in range(0, size):
            digit = line[i]
            if digit == "0":
                zeros[i] += 1
            elif digit == "1":
                ones[i] += 1
            else:
                raise Exception("WEIRD DIGIT %s", digit)

    if zeros[pos] > ones[pos]:
        keep="0"
    else:
        keep="1" #Equal = keep 1

    co2_lines = [x for x in co2_lines if x[pos]==keep]
    #print(co2_lines)
    pos += 1


co2_rating = int(co2_lines[0],2)
print("CO2 rating:", co2_rating)

print("Result:", o2_rating * co2_rating)
