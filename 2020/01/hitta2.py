#!/usr/bin/env python3

import sys

seen = set()

for line in sys.stdin:
    line = line.strip()
    if len(line)==0:
        continue
    n = int(line)
    for r1 in seen:
        r2 = 2020-n-r1
        if r2 in seen:
            #Found match
            result = n*r1*r2
            print(n, r1, r2)
            print(result)
            sys.exit(0)
    seen.add(n)

sys.exit(1)