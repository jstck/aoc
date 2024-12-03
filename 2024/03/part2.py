#!/usr/bin/env python3

import re
import sys

re_ops = re.compile(r'do\(\)|don\'t\(\)|mul\(\d+,\d+\)')
remul = re.compile(r'^mul\((\d+),(\d+)\)$')

sum = 0

domul = True

for line in sys.stdin.readlines():
    for m in re_ops.findall(line):
        print(m)
        if m == "do()":
            domul = True
        elif m == "don't()":
            domul = False
        else:
            m2 = remul.match(m)
            a = int(m2.group(1))
            b = int(m2.group(2))
            c = a*b
            if domul:
                sum += c

print(sum)
