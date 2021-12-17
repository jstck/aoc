#!/usr/bin/env python3

import sys
import argparse
import re

match = re.search(r'aoc/?(\d+)/(\d+)', __file__)
if match:
    descr = "Advent of Code " + match.group(1) + ":" + match.group(2)
else:
    descr = "Advent of some kind of Code"

parser = argparse.ArgumentParser(description = descr)

parser.add_argument('-1', action='store_true', help="Do part 1")
parser.add_argument('-2', action='store_true', help="Do part 2")
parser.add_argument('--verbose', '-v', action='count', default=0, help="Increase verbosity")

args = parser.parse_args()

part2 = vars(args)["2"]
part1 = vars(args)["1"] or not part2 #Do part 1 if not part 2 specified
verbosity = vars(args)["verbose"]

#Print controlled by verbosity level
def vprint(*args):
    if args[0]<= verbosity:
        print(*args[1:])


#Sample:
#xtarget = [20,30]
#ytarget = [-10,-5]

#Actual input:
xtarget = [206,250]
ytarget = [-105,-57]

#The Y velocity needs to have an integer multiple inside the window.
#After going up and turning and falling back, it will pass downward from y=0
#with same velocity in downward direction
#Highest possible velocity is the furthest Y-bound of the target, anything larger
#would go right past in one step

vybound = abs(ytarget[0])
vxbound = xtarget[1]

#Simulate trajectory in Y position, count the number of steps needed
yhits = []
totalhits = 0
for vy0 in range(vybound, -vybound-1, -1):
    for vx0 in range(1,vxbound+1):

        hashit = False

        ypos = 0
        xpos = 0
        vy = vy0
        vx = vx0
        ymax = ypos
        step = 0
        while True:
            if ypos <= ytarget[1] and ypos >= ytarget[0] and xpos >= xtarget[0] and xpos <= xtarget[1]:
                #Scored first hit
                if totalhits==0:
                    print("Hit at (%d,%d) at step %d with vx=%d vy=%d, ymax=%d" % (xpos,ypos,step,vx0,vy0,ymax))
                yhits.append((vy0,step))
                if not hashit:
                    totalhits += 1
                    hashit = True

            if ypos < ytarget[0]:
                #Gone past it
                break

            if xpos > xtarget[1]:
                break
            
            ypos += vy
            vy -= 1
            xpos += vx
            if vx>0:
                vx -= 1
            ymax = max(ymax,ypos)
            
            step += 1

#print(yhits)

#Upper bound for X velocity is further x bound, or it will go past in 1 step

##for (vy0,step) in yhits:

print("Total hits (n initial values):", totalhits)
print("Total hit steps:", len(yhits))