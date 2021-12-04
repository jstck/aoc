#!/usr/bin/env python3

import sys

lines = [l.strip() for l in sys.stdin.readlines()]

print(lines)

size = len(lines[0])

zeros = [0] * size
ones = [0] * size


for line in lines:
    for i in range(0, size):
        digit = line[i]
        if digit == "0":
            zeros[i] += 1
        elif digit == "1":
            ones[i] += 1
        else:
            raise Exception("WEIRD DIGIT %s", digit)

result = ""
antiresult = ""

print(zeros, ones)

for i in range(0, size):
    if ones[i] > zeros[i]:
        result += "1"
        antiresult += "0"
    else:
        result += "0"
        antiresult += "1"

gamma = int(result[0:size],2)
epsilon = int(antiresult[0:size],2)
print("Gamma", gamma)
print("Epsilon", epsilon)
print("Result", gamma*epsilon)
