#!/usr/bin/env python3

import sys
import re

instructions = [x.strip() for x in sys.stdin.readlines()]

heading = 0

x = 0
y = 0

for instruction in instructions:
    command = instruction[0]
    value = int(instruction[1:])

    if command=="N":
        y += value
    elif command=="S":
        y -= value
    elif command=="E":
        x += value
    elif command=="W":
        x -= value
    elif command=="L":
        heading = (heading + value) % 360
        print("New heading", heading)
    elif command=="R":
        heading = (heading - value) % 360
        print("New heading", heading)
    elif command=="F":
        if heading==0:
            x+=value #EAST
        elif heading==90:
            y+=value #NORTH
        elif heading==180:
            x-=value #WEST
        elif heading==270:
            y-=value #SOUTH
        else:
            print("WEIRD HEADING", heading)
    else:
        print("WEIRD COMMAND", instruction)

print("New position:", (x, y))
print("Travelled:", abs(x)+abs(y))