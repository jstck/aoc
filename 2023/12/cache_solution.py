#!/usr/bin/env python3

import sys
from functools import cache

@cache
def subsolve(springs: str, counts, curcount) -> int:
    #print(springs,counts,curcount)
    
    if len(springs) == 0:

        #No more springs
        if curcount == 0 and len(counts) == 0:
            return 1
        
        #Current set of springs finished
        if len(counts) == 1 and counts[0] == curcount:
            return 1
        
        return 0
    
    if len(counts) == 0:
        if curcount == 0 and "#" not in springs:
            return 1
        return 0
    
    head = springs[0]
    tail = springs[1:]

    #We're not currently in a row of springs
    if curcount == 0:

        if head == ".":
            #Skip this one and continue
            return subsolve(tail, counts, 0)
        
        elif head == "#":
            #Start a new count on this one
            return subsolve(tail,counts, 1)
        
        elif head == "?":

            #Try both and memorize
            return subsolve(tail, counts, 0) + subsolve(tail, counts, 1)
                
    #Current quota fulfilled
    elif curcount == counts[0]:
        if head == "#":
            #Can't be more springs here!
            return 0
        
        else:
            #Both ? and . have to count as "not a spring" for this to work. Close current count.

            #If no more springs, there can't be any more # remaining (all remaining ? are .)
            if len(counts) == 0:
                if "#" in tail:
                    return 0
                else:
                    #print(prev+springs)
                    return 1
                
            return subsolve(tail, counts[1:], 0)
    
    #Increase current count
    else:
        assert(curcount < counts[0])

        if head == ".":
            #This can't work, need more springs!
            return 0
        else:
            #Both ? and # have to be a spring
            return subsolve(tail, counts, curcount+1)
        
    assert(False)

def solve(t):
    return subsolve(t[0], t[1], 0)


def unfold(t):
    (springs, counts) = t
    springs = "?".join(5*[springs])
    counts = counts*5

    return (springs, counts)

if __name__ == "__main__":
    input = sys.stdin.readlines()
    items = []
    maxlen = 0
    for line in input:
        line = line.strip()
        springs, counts = line.split(" ")
        counts = tuple([int(x) for x in counts.split(",")])
        items.append((springs,counts))

    sum = 0
    for t in items:
        sum += solve(t)

    print("Part 1:", sum)

    items2 = map(unfold, items)
    sum = 0
    for t in items2:
        sum += solve(t)

    print("Part 2:", sum)
