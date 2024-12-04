#!/usr/bin/env python3

import re
import sys

remul = re.compile(r'mul\((\d+),(\d+)\)')

sum = 0

for line in sys.stdin.readlines():
    for (a,b) in remul.findall(line):
        sum += int(a)*int(b)

print(sum)
