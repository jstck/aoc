#!/usr/bin/env python3

import sys
from collections import defaultdict


with open("input.txt") as fp:
    lines = fp.readlines()


list1 = []
list2 = []

counts = defaultdict(int)

for line in lines:
    line = line.strip()
    parts = line.split()

    a = int(parts[0].strip())
    b = int(parts[1].strip())
    list1.append(a)
    list2.append(b)

    counts[b] += 1



list1.sort()
list2.sort()

sum = 0
sim = 0

for i in range(len(list1)):
    a = list1[i]
    b = list2[i]
    dist = abs(a-b)
    sum += dist

    sim += a * counts[a]

print("part1:",sum)
print("part2:",sim)
