#!/usr/bin/env python3

import sys


invalids = 0
invalids2 = 0
def is_repeat2(s: str) -> bool:
    if len(s)%2 != 0:
        return False
    half = len(s)//2

    first = s[:half]
    second = s[half:]

    return first==second

def is_repeat_any(s: str) -> bool:
    t = len(s)

    #Try all lengths of repeated sequences
    for i in range(1,t//2+1):
        if t%i!= 0:
            continue
        parts = list(map(''.join, zip(*[iter(s)]*i)))
        p0 = parts[0]
        match = True
        for p in parts[1:]:
            if p0 != p:
                match = False
                break
        if match:
            return True
    return False

for l in sys.stdin.readlines():
    if len(l) == 0: continue
    for p in l.strip().split(","):
        if len(p) == 0: continue
        (a,b) = p.split("-")

        x = int(a)
        y = int(b)

        #print(f"{x} - {y}")

        for i in range(x,y+1):
            s = str(i)

            if is_repeat2(s):
                invalids += i

            if is_repeat_any(s):
                invalids2 += i
                #print(i)

print(f"Part 1: {invalids}")
print(f"Part 2: {invalids2}")
