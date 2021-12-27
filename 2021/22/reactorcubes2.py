#!/usr/bin/env python3

import sys
import argparse
import re
import random

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

regions = []

class cuboid():
    def __init__(self, x0, x1, y0, y1, z0, z1):
        if x0>x1: (x1,x0) = (x0,x1)
        if y0>y1: (y1,y0) = (y0,y1)
        if z0>z1: (z1,z0) = (z0,z1)
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.z0 = z0
        self.z1 = z1
    
    def volume(self):
        x = (self.x1-self.x0+1)
        y = (self.y1-self.y0+1)
        z = (self.z1-self.z0+1)
        return x*y*z


    def overlap(self, other):
        if self.x1 < other.x0: return False
        if self.x0 > other.x1: return False
        if self.y1 < other.y0: return False
        if self.y0 > other.y1: return False
        if self.z1 < other.z0: return False
        if self.z0 > other.z1: return False
        return True

    def coordinates(self):
        return [self.x0, self.x1, self.y0, self.y1, self.z0, self.z1]

    def isInside(self, other):
        return self.x0 >= other.x0 and \
               self.x1 <= other.x1 and \
               self.y0 >= other.y0 and \
               self.y1 <= other.y1 and \
               self.z0 >= other.z0 and \
               self.z1 <= other.z1

    def union(self, other):

        #Check for easy case where one is inside of the other
        if self.isInside(other):
            yield other
            return
        elif other.isInside(self):
            yield self
            return

        #"Shave off" whatever sticks out in the X- direction (part of just one of the cuboids)
        #Make new x0,x1 for next steps
        if self.x0 < other.x0:
            #it's "this one" that sticks out
            yield cuboid(self.x0, other.x0-1, self.y0, self.y1, self.z0, self.z1)
            x0 = other.x0
        elif other.x0 < self.x0:
            #The other one sticks out
            yield cuboid(other.x0, self.x0-1, other.y0, other.y1, other.z0, other.z1)
            x0 = self.x0
        else: #X0 coords equal. Nothing sticks out
            x0 = self.x0

        #Same thing in the X+ direction
        if self.x1 > other.x1:
            #it's "this one" that sticks out
            yield cuboid(other.x1+1, self.x1, self.y0, self.y1, self.z0, self.z1)
            x1 = other.x1
        elif other.x1 > self.x1:
            #The other one sticks out
            yield cuboid(self.x1+1, other.x1, other.y0, other.y1, other.z0, other.z1)
            x1 = self.x1
        else:
            x1 = self.x1


        #Y-
        if self.y0 < other.y0:
            yield cuboid(x0, x1, self.y0, other.y0-1, self.z0, self.z1)
            y0 = other.y0
        elif other.y0 < self.y0:
            yield cuboid(x0, x1, other.y0, self.y0-1, other.z0, other.z1)
            y0 = self.y0
        else:
            y0 = self.y0

        #Y+
        if self.y1 > other.y1:
            yield cuboid(x0, x1, other.y1+1, self.y1, self.z0, self.z1)
            y1 = other.y1
        elif other.y1 > self.y1:
            yield cuboid(x0, x1, self.y1+1, other.y1, other.z0, other.z1)
            y1 = self.y1
        else:
            y1 = self.y1

        #Remaing chunk is "shaved off" in Y and X, make a cuboid spanning all of Z here
        zs = sorted([self.z0, self.z1, other.z0, other.z1])
        z0 = zs[0]
        z1 = zs[3]
        yield cuboid(x0,x1,y0,y1,z0,z1)


    #Return cuboids for what is left if other is subtracted from self
    def subtract(self, other):
        #If this cube is entirely inside the other one, there is nothing left
        if self.isInside(other):
            return []
        
        #See if something sticks out on either side and return those bits
        #and make new coordinates for "remaining stuff"
        
        #X-
        if self.x0 < other.x0:
            yield cuboid(self.x0, other.x0-1, self.y0, self.y1, self.z0, self.z1)
            x0 = other.x0
        else: #X0 coords equal. Nothing sticks out
            x0 = self.x0

        #X+
        if self.x1 > other.x1:
            yield cuboid(other.x1+1, self.x1, self.y0, self.y1, self.z0, self.z1)
            x1 = other.x1
        else:
            x1 = self.x1

        #Y-
        if self.y0 < other.y0:
            yield cuboid(x0, x1, self.y0, other.y0-1, self.z0, self.z1)
            y0 = other.y0
        else:
            y0 = self.y0
        
        #Y+
        if self.y1 > other.y1:
            yield cuboid(x0, x1, other.y1+1, self.y1, self.z0, self.z1)
            y1 = other.y1
        else:
            y1 = self.y1

        #Z-
        if self.z0 < other.z0:
            yield cuboid(x0, x1, y0, y1, self.z0, other.z0-1)
            z0 = other.z0
        else:
            z0 = self.z0

        #Z+
        if self.z1 > other.z1:
            yield cuboid(x0, x1, y0, y1, other.z1+1, self.z1)
            z1 = other.z1
        else:
            z1 = self.z1

        #Whatever's left is two overlapping "cores" that should just be nothingness


    def intersection(self,other):
        if not self.overlap(other): return None
        (x0,x1) = sorted([self.x0, self.x1, other.x0, other.x1])[1:3]
        (y0,y1) = sorted([self.y0, self.y1, other.y0, other.y1])[1:3]
        (z0,z1) = sorted([self.z0, self.z1, other.z0, other.z1])[1:3]
        return cuboid(x0,x1,y0,y1,z0,z1)

    def __str__(self):
        return "X: {0}-{1}  Y: {2}-{3}  Z: {4}-{5}".format(*tuple(self.coordinates()))

universe = []

count=0
for line in sys.stdin.readlines():
    m = re.match('(on|off) x=([0-9-]+)\.\.([0-9-]+),y=([0-9-]+)\.\.([0-9-]+),z=([0-9-]+)\.\.([0-9-]+)', line.strip())

    state = m.group(1)
    coords = [int(x) for x in m.groups()[1:]]

    [x0,x1] = sorted(coords[0:2])
    [y0,y1] = sorted(coords[2:4])
    [z0,z1] = sorted(coords[4:6])

    newcuboid = cuboid(x0,x1,y0,y1,z0,z1)

    if state=='off':
        #Go through all current cuboids and replace with their intersections
        newuniverse = []
        for c in universe:
            if not c.overlap(newcuboid):
                newuniverse.append(c)
            else:
                bits = c.subtract(newcuboid)
                newuniverse += bits
        universe = newuniverse
    elif state=='on':
        newuniverse = []
        overlaps = []
        for c in universe:
            if not c.overlap(newcuboid):
                newuniverse.append(c)
            else:
                overlaps.append(c)
        if len(overlaps) == 0:
            newuniverse.append(newcuboid)
        else:
            for c in overlaps:
                bits = c.subtract(newcuboid)
                newuniverse += bits
            newuniverse.append(newcuboid)
        universe = newuniverse

    count += 1
    print(count, newcuboid, state, len(universe))

v = 0
for c in universe:
    v+=c.volume()
print(v)