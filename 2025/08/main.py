#!/usr/bin/env python3


from dataclasses import dataclass
import sys


sys.path.append("../..")
from lib.aoc import *

def sq(x: int) -> int:
    return x*x

@dataclass
class Junction:
    id: int
    x: int
    y: int
    z: int

    # Do square distances, because integers or something
    def distanceTo(self, j) -> int:
        return sq(self.x-j.x) + sq(self.y-j.y) + sq(self.z-j.z)
    
    def __str__(self) -> str:
        return f"{self.id}: [{self.x},{self.y},{self.z}]"

if __name__ == "__main__":
    input = readinput()

    id = 0
    junctions: list[Junction] = []

    for line in input:
        x,y,z = [int(c) for c in line.split(",")]
        j = Junction(id,x,y,z)
        junctions.append(j)
        id += 1

    size = id

    if size<100:
        maxconnections = 10
    else:
        maxconnections = 1000

    #Generate all pairs of distances
    distances: list[tuple[int,int,int]] = []
    for a in range(id-1):
        for b in range(a+1, size):
            d = junctions[a].distanceTo(junctions[b])
            distances.append((d,a,b))

    #Sort on shortest distance first (first item in tuple)
    distances.sort()

    #Each junction is in a group with just itself
    groups: list[set[int]] = [set([x]) for x in range(size)]

    i=0
    a=0
    b=0
    while True:
        d,a,b = distances[i]

        # Just join the two groups together and set all members to the same thing
        newgroup: set[int] = groups[a].union(groups[b])
        for id in newgroup:
            groups[id] = newgroup

        i+=1

        # Time to do part 1 now!
        if i == maxconnections:
            sizes = []
            seengroups: set[tuple[int, ...]] = set()
            for i1 in range(size):
                #Do groups as sorted tuples for hashability
                gg = tuple(sorted(list(groups[i1])))
                if gg not in seengroups:
                    sizes.append(len(gg))
                    seengroups.add(gg)

            #Just sort and find the three largest ones
            sizes.sort(reverse=True)

            s1, s2, s3 = sizes[:3]

            p1 = s1*s2*s3
            print(f"Part 1: {p1} ({s1}*{s2}*{s3})")
            print()

        # The new group contains all junctions, we're done.
        if len(newgroup) == size:
            print(f"Last two boxes connected (after {i} connections):")
            print(junctions[a])
            print(junctions[b])
            print()
            p2 = junctions[a].x * junctions[b].x
            print("Part 2:", p2)
            break

        #Safety bailout
        if i>=20000:
            print("Connection limit reached, bailing out")
            break
