#!/usr/bin/env python3

import re
import sys

re_ops = re.compile(r'(do)\(\)|(don\'t)\(\)|mul\((\d+),(\d+)\)')

p1, p2 = 0, 0

domul = True

for line in sys.stdin.readlines():
    for m in re_ops.findall(line):
        if m[0] == "do":
            domul = True
        elif m[1] == "don't":
            domul = False
        else:
            x = int(m[2])*int(m[3])
            p1 += x
            if domul:
                p2 += x

print("Part 1:", p1)
print("Part 2:", p2)
