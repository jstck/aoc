#!/usr/bin/env python3

import sys

seen = set()

for line in sys.stdin:
    line = line.strip()
    if len(line)==0:
        continue
    n = int(line)
    r = 2020-n
    if r in seen:
        #Found match
        result = n*r
        print(result)
        sys.exit(0)
    seen.add(n)

sys.exit(1)