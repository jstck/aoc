#!/usr/bin/env python3

import re
import sys

remul = re.compile(r'mul\((\d+),(\d+)\)')

sum = 0

for line in sys.stdin.readlines():
    for (a,b) in remul.findall(line):
        a,b = int(a), int(b)
        c = a*b
        #print(f"{a}*{b}={c}")
        sum += c

print(sum)
