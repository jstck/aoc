#!/usr/bin/env python3

import sys
import re

encrypted = [int(x.strip()) for x in sys.stdin.readlines()]

def findsum(encrypted_data, pos, lookback=25):
    x = encrypted_data[pos]

    buffer = encrypted_data[pos-lookback:pos]

    for i in range(0, len(buffer)-1):
        for j in range(i+1, len(buffer)):
            a = buffer[i]
            b = buffer[j]
            if x == a+b:
                print(x,"=",a, b)
                return True
    return False

preamble_length = 25

for i in range(preamble_length, len(encrypted)):
    if not findsum(encrypted, i, preamble_length):
        print("No match for", encrypted[i], "at pos", i)
