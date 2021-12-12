#!/usr/bin/env python3

import sys

prevdepth = -1000

count = 0

for line in sys.stdin:
    line = line.strip()
    newdepth = int(line)

    if newdepth > prevdepth and not prevdepth<0:
        count += 1

    prevdepth = newdepth

print(count)

    