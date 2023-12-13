#!/usr/bin/env python3

from __future__ import annotations

import sys
from typing import List, Tuple, Dict, Optional

class Cup:
    def __init__(self, value: int, next: Optional[Cup]=None):
        self.value: int = value
        if next is not None:
            self.next: Cup = next

def cuplist(startcup: Cup, count: int=9) -> list[int]:
    tmp = startcup
    result: list[int] = [tmp.value]

    for _ in range(count-1):
        tmp = tmp.next
        result.append(tmp.value)
    
    return result



def fastcrab(index: Dict[int,Cup], rounds: int, start: int, maxcup: int=0) -> list[int]:
    #If no maxcup given, figure it out.
    if maxcup == 0:
        maxcup = max(index.keys())
    
    currentCup: Cup = index[start]

    debuggle = rounds // 100

    for round in range(rounds):
        cur: int = currentCup.value
        #Yoink next 3 cups from current position
        yoinkstart = currentCup.next
        yoinkmid = yoinkstart.next
        yoinkend = yoinkmid.next

        #List of yoinked cup values (as well as current) to avoid as destination
        yoinks: list[int] = [cur, yoinkstart.value, yoinkmid.value, yoinkend.value]

        #Find next cup value
        dst = cur
        while dst in yoinks:
            dst -= 1
            if dst <= 0:
                dst = maxcup

        #Debug print
        if round % debuggle == 0:
            print(f"-- move {round+1} --")
            firstcups = " ".join([f"({x})" if x==cur else str(x) for x in cuplist(currentCup)])
            print("cups:",firstcups)
            print("pick up:", ", ".join([str(x) for x in yoinks[1:]]))
            print("destination:", dst)
            print()

        #Relink list
        destCup: Cup = index[dst]
        currentCup.next = yoinkend.next
        yoinkend.next = destCup.next
        destCup.next = yoinkstart

        currentCup = currentCup.next
    

    #Return a list of 8 values starting with the cup immediately after cup 1
    cupOne: Cup = index[1]
    
    return cuplist(cupOne.next, 8)

def slowcrab(cups: List[int], rounds: int) -> List[int]:
    currentcup = cups[0]
    size = len(cups)
    pos = 0
    for round in range(rounds):
        r = round + 1
        if r % 1000 == 0:
            print("ROUND", r)
        #print("Current cup:", currentcup)

        yoinkstart = pos+1
        yoinkend = pos+4
        if yoinkend <= size:
            yoink = cups[yoinkstart:yoinkend]
            cups = cups[:yoinkstart] + cups[yoinkend:]
        else:
            yoink = cups[yoinkstart:]
            cups = cups[:yoinkstart]
            l = 3-len(yoink)
            yoink += cups[:l]
            cups = cups[l:]

        #print("Yoinked cups:", yoink)

        #Find destination cup
        t = currentcup
        while t in yoink + [currentcup]:
            t = t - 1
            if t<=0:
                t=size

        #print("Destination cup:", t)

        tpos = cups.index(t)
        cups = cups[0:tpos+1] + yoink + cups[tpos+1:]

        currentpos = cups.index(currentcup)
        pos = (currentpos + 1) % size
        currentcup = cups[pos]

        #print("".join([str(c) for c in cups]))
        
    #Reorder cups
    i = cups.index(1)
    return cups[i+1:] + cups[:i]


def parseAndInit(input: str) -> Tuple[List[int],Dict[int,Cup]]:
    startcups = [int(x) for x in list(input.strip())]
    index: Dict[int,Cup] = {}

        
    prev = None
    for c in startcups:
        cup = Cup(c)
        if prev is not None:
            prev.next = cup
        index[c] = cup
        prev = cup

    #Link to a loop
    assert(prev is not None)
    prev.next = index[startcups[0]]

    return (startcups, index)

if __name__ == "__main__":
    indata = sys.stdin.read()
    
    (startcups, index) = parseAndInit(indata)

    p1 = slowcrab(startcups, 100)
    p1b = fastcrab(index, 100, startcups[0])

    p1_answer = "".join([str(c) for c in p1])
    print(f"Part1: {p1_answer}")
    print("Fastcrab:", "".join([str(c) for c in p1b]))

    # PART 2
    TOTALCUPS = 1000000

    #reinit state
    (startcups, index) = parseAndInit(indata)

    #Create a million more cups
    prev = index[startcups[-1]]
    for c in range(len(startcups)+1, TOTALCUPS+1):
        cup = Cup(c)
        prev.next = cup
        index[c] = cup
        prev = cup

    #loop it
    firstcup = index[startcups[0]]
    prev.next = firstcup


    #cups = cups + list(range(len(cups)+1, 1000001))

    #p2 = crab(cups,10000000)
    #p2 = crab(cups,10000)
    p2 = fastcrab(index, 10_000_000, firstcup.value, TOTALCUPS)

    s1 = p2[0]
    s2 = p2[1]
    print(f"Part2: {s1}*{s1} = {s1*s2}")


