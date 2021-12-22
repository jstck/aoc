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


initsize = [-50,50]

cubes = []

#for x in range(initsize[0],initsize[1]+1):
#    for x in range(initsize[0],initsize[1]+1):

cubes = [ [ [0]*101 for y in range(101)] for x in range(101)]


for line in sys.stdin.readlines():
    m = re.match('(on|off) x=([0-9-]+)\.\.([0-9-]+),y=([0-9-]+)\.\.([0-9-]+),z=([0-9-]+)\.\.([0-9-]+)', line.strip())

    state = m.group(1)
    [x0, x1, y0, y1, z0, z1] = [int(x) for x in m.groups()[1:]]

    #Sort coordinate pairs
    if x0>x1:
        x0,x1 = x1,x0
    if y0>y1:
        y0,y1 = y1,y0
    if z0>z1:
        z0,z1 = z1,z0

    #Skip out of bounds
    if x0>50:  continue
    if x1<-50: continue
    if y0>50:  continue
    if y1<-50: continue
    if y0>50:  continue
    if y1<-50: continue

    #Limit to active range
    if x0<-50: x0=-50
    if x1>50:  x1=50
    if y0<-50: y0=-50
    if y1>50:  y1=50
    if z0<-50: z0=-50
    if z1>50:  z1=50

    print("Turning",state,(x0,x1,y0,y1,z0,z1))

    if state=='on':
        cubestate = 1
    else:
        cubestate = 0

    for x in range(x0,x1+1):
        for y in range(y0,y1+1):
            for z in range(z0,z1+1):
                cubes[x-50][y-50][z-50] = cubestate


total = 0
for x in range(101):
    for y in range(101):
        total += sum(cubes[x][y])

print(total)