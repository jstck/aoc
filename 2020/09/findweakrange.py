#!/usr/bin/env python3

import sys
import re

encrypted = [int(x.strip()) for x in sys.stdin.readlines()]

def findrange(target, maxpos):

    for i in range(0, maxpos-1):
        for j in range(1, maxpos):
            
            chunk = encrypted[i:j]
            
            if sum(chunk)==target:
                print(target, "=", encrypted[i], "to", encrypted[j-1])
                print("At lines", i+1, "to", j)
                print(chunk)
                a = min(chunk)
                b = max(chunk)
                print("ANSWER:", a, "+", b, "=", a+b)
                return True
    return False

target = 552655238
targetpos = 610
#target = 127
#targetpos = 15

findrange(target, targetpos)
