#!/usr/bin/env python3


import sys

max_x = 0
max_y = 0


lines = [l.replace("->",",") for l in sys.stdin.readlines()]

verticals = []
horizontals = []
diagonals = []

def sign(x):
    if x>0:
        return 1
    if x<0:
        return -1

    return 0

for line in lines:
    vent = [int(x.strip()) for x in line.split(",")]

    (x1, y1, x2, y2) = vent

    if x1 == x2: #Horizontal line
        horizontals.append(vent)
    elif y1 == y2: #Vertical line
        verticals.append(vent)
    else:
        diagonals.append(vent)
        if abs(x2-x1) != abs(y2-y1):
            print("Broken diagonal:", vent)

    max_x = max(max_x, x1, x2)
    max_y = max(max_y, y1, y2)

max_x += 1
max_y += 1

print("Board size:", max_x, "X", max_y)
counts = [ [0]*max_x for i in range(max_y)]


def printboard():
    if max_x>20 or max_y>20:
        return
    
    for l in counts:
        s = "".join([str(c) for c in l]).replace("0",".")
        print(s)


for vent in horizontals:
    (x1, y1, x2, y2) = vent

    if(y1 > y2):
        y1, y2 = y2, y1

    for y in range(y1, y2+1):
        counts[y][x1] += 1


for vent in verticals:
    (x1, y1, x2, y2) = vent

    if(x1 > x2):
        x1, x2 = x2, x1

    for x in range(x1, x2+1):
        counts[y1][x] += 1

total_ortho = 0
for l in counts:
    for n in l:
        if n >=2:
            total_ortho += 1
printboard()
print("Count, orthogonal:", total_ortho)
print()

for vent in diagonals:
    (x1, y1, x2, y2) = vent

    dx = x2-x1
    dy = y2-y1

    sx = sign(dx)
    sy = sign(dy)

    for i in range(0, abs(dx)+1):
        x = x1 + sx*i
        y = y1 + sy*i
        counts[y][x] += 1


total_all=0

for l in counts:
    for n in l:
        if n >=2:
            total_all += 1

printboard()
print("Count, all:", total_all)