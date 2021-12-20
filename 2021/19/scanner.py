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


sensors = []
beacons = []
for line in sys.stdin.readlines():
    line = line.strip()
    if len(line)==0: continue
    if line[:3]=="---":
        if len(beacons)> 0:
            sensors.append(beacons)
            beacons = []
    else:
        beacon = tuple([int(x.strip()) for x in line.split(",")])
        beacons.append(beacon)

if len(beacons)> 0:
    sensors.append(beacons)

print("#sensors:", len(sensors))


def rotate(p, n):
    (x,y,z) = p
    if n>=24:
        n-=24
        z=-z
    
    if   n==0:  return (x,y,z)
    elif n==1:  return (x,-z,y)
    elif n==2:  return (x,-y,-z)
    elif n==3:  return (x,z,-y)
    elif n==4:  return (-x,y,-z)
    elif n==5:  return (-x,z,y)
    elif n==6:  return (-x,-y,z)
    elif n==7:  return (-x,-z,-y)
    elif n==8:  return (y,x,-z)
    elif n==9:  return (y,z,x)
    elif n==10: return (y,-x,z)
    elif n==11: return (y,-z,-x)
    elif n==12: return (-y,x,z)
    elif n==13: return (-y,-z,x)
    elif n==14: return (-y,-x,-z)
    elif n==15: return (-y,z,-x)
    elif n==16: return (z,x,y)
    elif n==17: return (z,-y,x)
    elif n==18: return (z,-x,-y)
    elif n==19: return (z,y,-x)
    elif n==20: return (-z,x,-y)
    elif n==21: return (-z,y,x)
    elif n==22: return (-z,-x,y)
    elif n==23: return (-z,-y,-x)

    print("ERROR ROTATION")
    sys.exit(1)


def offset(p0,p1):
    (x0,y0,z0) = p0
    (x1,y1,z1) = p1
    return (x1-x0,y1-y0,z1-z0)


def add(p0,p1):
    (x0,y0,z0) = p0
    (x1,y1,z1) = p1
    return (x0+x1,y0+y1,z0+z1)

#sensor0 = sensors.pop(0)

#beacons = set(sensor0)

def merge(sensorlist, s0, s1, d, rot):
    sensor0 = sensorlist[s0]
    sensor1 = sensorlist.pop(s1)
    #sensor1 = sensorlist[s1]
    #sensorlist[s1] = []
    
    
    dupes = 0

    for b1 in sensor1:
        b1p = add(d,rotate(b1,rot))

        if b1p not in sensor0:
            sensor0.append(b1p)
        else:
            dupes += 1

    return dupes

sensor_offsets = [(0,0,0)]

def matchsensors(sensors):
    global sensor_offsets
    print("Beacon counts:")
    print(" ".join([str(len(x)) for x in sensors]))
    #for i in range(len(sensors)):
    for i in [0]:
        sensor0 = sensors[i]
        for j in range(i+1,len(sensors)):

            sensor1 = sensors[j]
            bestmove = ()
            besthits = 0
            for rot in range(24):
                offsets = {}
                for b1 in sensor1:
                    for b0 in sensor0:
                        b1r = rotate(b1, rot)

                        d = offset(b1r,b0)
                        offsets[d] = 1 + offsets.get(d,0)

                        if offsets[d] >= 12:
                             print("Merging %d into %d with offset %s rot %d" % (j, i, str(d), rot))
                             c = merge(sensors, i, j, d, rot)
                             print(c, "duplicates found")
                             sensor_offsets.append(d)
                             return True
                
                #hits = [(d, count) for (d, count) in sorted(offsets.items(), key=lambda x: x[1]) if count>1]
                #if len(hits)>0:
                #    tophit = hits[0][1]
                #    if tophit > besthits:
                #       besthits = tophit
                #        bestoffset = hits[0][0]
                #        bestmove = (bestoffset, rot)

            #if besthits >= 12:
            #    (d, rot) = bestmove
            #    print("Merging %d into %d with offset %s rot %d (%d hits)" % (j, i, str(d), rot, besthits))

            #    c = merge(sensors, i, j, d, rot)
            #    print(c, "duplicates found")
            #    return True
    
    return False

#Check that all rotations seem sane
rots = []

p = (1,2,3)
for r in range(48):
    p1 = rotate(p,r)
    if p1 in rots:
        print(r,"already in:", str(p1))
    else:
        rots.append(p1)


while matchsensors(sensors):
    pass
                    
        #         #print(offsets)
        #         #hits = sum([x for x in offsets.values() if x>1])
        #         hits = max(offsets.values())
        #         if hits > besthits:
        #             besthits = hits
        #             bestrot = rot
        #             if hits > 1:
        #                 print(i,j,rot)
        #                 [print(d, count) for (d, count) in sorted(offsets.items(), key=lambda x: x[1]) if count>1]
        # #print(i,"-",j," - rot",rot,"max",besthits)

print("Total beacons: ",sum([len(s) for s in sensors]))

#Part 2

def manhattan(p1,p2):
    (x1,y1,z1) = p1
    (x2,y2,z2) = p2

    return abs(x1-x2)+abs(y1-y2)+abs(z1-z2)

best=(0,0,0)

for i in range(len(sensor_offsets)-1):
    for j in range(i+1,len(sensor_offsets)):
        dist = manhattan(sensor_offsets[i],sensor_offsets[j])
        if dist>best[0]:
            best=(dist,i,j)

print("Longest distance:",best)