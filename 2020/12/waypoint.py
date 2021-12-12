#!/usr/bin/env python3

import sys
import re

instructions = [x.strip() for x in sys.stdin.readlines()]

wp_x = 10
wp_y = 1

ship_x = 0
ship_y = 0

for instruction in instructions:
    command = instruction[0]
    value = int(instruction[1:])

    if command=="N":
        wp_y += value
    elif command=="S":
        wp_y -= value
    elif command=="E":
        wp_x += value
    elif command=="W":
        wp_x -= value
    elif command in ["L", "R"]:

        if command == "L":
            angle = value % 360
        elif command == "R":
            angle = -value % 360

        if angle == 0:
            pass
        elif angle == 90:
            (wp_x, wp_y) = (-wp_y, wp_x)
        elif angle == 180:
            (wp_x, wp_y) = (-wp_x, -wp_y)
        elif angle == 270:
            (wp_x, wp_y) = (wp_y, -wp_x)
        else:
            print("WEIRD ANGLE", angle, instruction)            

    elif command=="F":
        print("Moving", value, "times", (wp_x, wp_y))
        
        ship_x += value * wp_x
        ship_y += value * wp_y

    else:
        print("WEIRD COMMAND", instruction)

print("New position:", (ship_x, ship_y))
print("Travelled:", abs(ship_x)+abs(ship_y))