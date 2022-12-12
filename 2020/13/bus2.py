#!/usr/bin/env python3

import sys
import re
import math
from functools import reduce

_ = int(sys.stdin.readline().strip()) #Discard timestamp

buses_raw = sys.stdin.readline().strip().split(",")

buses = [int(bus) for bus in buses_raw if not bus=='x']

offsets = [int(b) - i for i,b in enumerate(buses_raw) if b != 'x']

buses_pos = {}

#print(buses_raw)

for i in range(len(buses_raw)):
    c = buses_raw[i]
    if c == 'x':
        continue
    bus = int(c)
    buses_pos[bus] = i

print(buses)
print(buses_pos)
print(offsets)

def CRT(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    x0 = 0
    x1 = 1
    b0 = b
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

n = CRT(buses, offsets)

print(n)