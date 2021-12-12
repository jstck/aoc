#!/usr/bin/env python3

import re
import sys

spalt = re.compile('^(\d+)-(\d+)\s+([a-z]):\s*([a-z]+)\s+$')

correct = 0

for line in sys.stdin:
    parts = spalt.split(line)

    lo = int(parts[1])
    hi = int(parts[2])

    c = parts[3]
    pw = parts[4]

    num = pw.count(c)

    ok = (num >= lo and num <= hi)

    print(lo, hi, c, pw, ok)

    if ok:
        correct+=1

print(correct)

    