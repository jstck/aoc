#!/usr/bin/env python3

import sys

x=0
y=0

for line in sys.stdin:
    line = line.strip()
    
    try:
        (command, value) = (line.split())
    except ValueError:
        continue

    value = int(value)

    if command == "forward":
        x += value
    elif command == "up":
        y -= value
        if y<0:
            raise ValueError("ABOVE SEA LEVEL")
            y=0
    elif command == "down":
        y += value
    else:
        raise ValueError("UNKNOWN COMMAND: %s" % command)

    print(command, value, x,y)

print(x*y)
