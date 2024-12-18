#!/usr/bin/env python3

import re
import sys

re_ops = re.compile(r'(do)\(\)|(don\'t)\(\)|mul\((\d+),(\d+)\)')

sum = 0

domul = True

for line in sys.stdin.readlines():
    for m in re_ops.findall(line):
        if m[0] == "do":
            domul = True
        elif m[1] == "don't":
            domul = False
        elif domul:
            sum += int(m[2])*int(m[3])

print(sum)
