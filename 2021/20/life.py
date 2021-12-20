#!/usr/bin/env python3

rules = []
for i in range(512):

    #Binary string (skipping 0b at start)
    b = bin(i)[2:]

    #pad to 9 digits
    l = len(b)
    if l<9:
        b = '0'*(9-l) + b

    #Make a nice list
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
