#!/usr/bin/env python3

import sys

x=0
y=0
aim=0

for line in sys.stdin:
    line = line.strip()
    
    try:
        (command, value) = (line.split())
    except ValueError:
        continue

    value = int(value)

    if command == "forward":
        x += value
        y += aim*value
    elif command == "up":
        aim -= value
    elif command == "down":
        aim += value
    else:
        print("UNKNOWN COMMAND: %s" % command)

    print(command, value, x,y,)

print(x*y)
