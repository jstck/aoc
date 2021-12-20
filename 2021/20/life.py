#!/usr/bin/env python3

import sys

def c2b(c):
    if c=="#":
        return 1
    return 0

def b2c(b):
    if b==1:
        return '#'
    return '.'

def b2c2(b):
    if b==1:
        return '[]'
    return ' .'

def getPixelIndex(image,x,y):
    index = 0
    for dy in [-1,0,1]:
        for dx in [-1,0,1]:
            index = index*2 + getPixelBounded(image,x+dx,y+dy)
    return index


rules = []
for i in range(512):

    #Binary string (skipping 0b at start)
    b = bin(i)[2:]

    #pad to 9 digits
    l = len(b)
    if l<9:
        b = '0'*(9-l) + b

    bits = [int(x) for x in list(b)]

    me = bits[4]
    neighbours = sum(bits[0:4] + bits[5:])

    if me==0:
        if neighbours==3:
            out = "#"
        else:
            out = "."
    else:
        if neighbours==3 or neighbours==2:
            out = "#"
        else:
            out = "."
    rules.append(out)

print("".join(rules))
print(len(rules))
