#!/usr/bin/env python3

import sys

exits = {}


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


def findpaths(path, has_revisit):
    #Current place in path:
    here = path[-1]

    if here == 'end':
        print(",".join(path))
        return 1

    #Exits from here
    newpaths = 0
    for e in exits[here]:
        if big(e):
            newpaths += findpaths(path + [e], has_revisit)
        elif e not in path:
            newpaths += findpaths(path + [e], has_revisit)
        elif not has_revisit and e!='start':
            newpaths += findpaths(path + [e], True)

    return newpaths

print(findpaths(['start'], False))