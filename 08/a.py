#!/usr/bin/env python3

import sys
from collections import Counter

output = []

lines = sys.stdin.readlines()
for line in lines:
    output.extend(line.split("|",1)[1].strip().split())


output = [len(s.strip()) for s in output]

counts = Counter(output)

ones = counts[2]
fours = counts[4]
sevens = counts[3]
eights = counts[7]

print(ones+fours+sevens+eights)