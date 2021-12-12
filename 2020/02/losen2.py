#!/usr/bin/env python3

import re
import sys

spalt = re.compile(r'^(\d+)-(\d+)\s+([a-z]):\s*([a-z]+)\s+$')

correct = 0

for line in sys.stdin:
    parts = spalt.split(line)

    lo = int(parts[1])
    hi = int(parts[2])

    c = parts[3]
    pw = parts[4]

    c1 = pw[lo-1]
    c2 = pw[hi-1]

    ena = c1==c
    andra = c2==c

    ok = (ena ^ andra)

    print(lo, hi, c, pw, ok)

    if ok:
        correct+=1

print(correct)

    