#!/usr/bin/env python3

import sys

part1 = True
part2 = False

if len(sys.argv) > 1:
    if sys.argv[1] == "2":
        part1 = False
        part2 = True
    elif sys.argv[1] == "both":
        part1 = True
        part2 = True
    

exits = {}

START = 'start'
END = 'end'

def big(c):
    return c[0].isupper()

for line in sys.stdin.readlines():
    (a, b) = line.strip().split("-",1)
    if a in exits.keys():
        exits[a].append(b)
    else:
        exits[a] = [b]

    if b in exits.keys():
        exits[b].append(a)
    else:
        exits[b] = [a]

    if big(a) and big(b):
        print("DANGERWARNING: %s and %s are connected, will cause a loop" % (a, b))
        #sys.exit(1)


maxlength = 2 * len(exits)

def findpaths1(path):
    #Current place in path:
    here = path[-1]

    if here == END:
        print(",".join(path))
        return 1

    #Exits from here
    newpaths = 0
    for e in exits[here]:
        if big(e) or e not in path:
            newpaths += findpaths1(path + [e])

    return newpaths

def findpaths2(path, has_revisit):
    #Current place in path:
    here = path[-1]

    #sanity filter
    if len(path) > maxlength:
        print("NOPE, path is too long now")
        #sys.exit(1)
        return 0

    #End reached
    if here == END:
        print(",".join(path))
        return 1

    #Exits from here
    newpaths = 0
    for e in exits[here]:
        if big(e) or e not in path:
            newpaths += findpaths2(path + [e], has_revisit)
        elif not has_revisit and e!=START:
            newpaths += findpaths2(path + [e], True)

    return newpaths

if part1:
    print("Part 1:",findpaths1([START]))

if part2:
    print("Part 2:",findpaths2([START], False))