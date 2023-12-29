#!/usr/bin/env python3

from collections import defaultdict
import sys


sys.path.append("../..")
from lib.aoc import *

def makefuel(reactions: dict[str,tuple[int,list[tuple[str,int]]]], fuelcount: int=1) -> int:

    needs: dict[str,int] = {"FUEL": fuelcount}
    stash: dict[str,int] = defaultdict(lambda: 0)
    ore = 0

    while len(needs)>0:
        #Check what stuff we need to make
        stuff = next(iter(needs))
        needcount = needs.pop(stuff)

        #See if stuff needed is already present
        if stuff in stash:
            has = stash[stuff]
            if has < needcount:
                needcount -= has
                stash[stuff] = 0
            else:
                stash[stuff] -= needcount
                #We got all we need of this stuff!
                continue

        #Find reaction
        outcount, reaction = reactions[stuff]

        #How many times does reaction need to be performed
        if needcount % outcount == 0:
            reactcount = needcount // outcount
            leftover = 0
        elif outcount > needcount:
            reactcount = 1
            leftover = outcount-needcount
        else:
            reactcount = needcount // outcount + 1
            leftover = outcount*reactcount - needcount

        for ingredient, ingcount in reaction:
            if ingredient == "ORE":
                ore += ingcount * reactcount
            else:
                needs[ingredient] = needs.get(ingredient, 0) + ingcount * reactcount

        if leftover > 0: stash[stuff] += leftover

    return ore

def maxfuel(reactions: dict[str,tuple[int,list[tuple[str,int]]]], orecount: int=1_000_000_000_000) -> int:
    lowerfuel = 0
    lowerore = 0

    upperfuel = 1
    upperore = makefuel(reactions,upperfuel)

    #Double upper bound until we get enough, move lower bound along behind
    while upperore < orecount:
        lowerfuel = upperfuel
        lowerore = upperore

        upperfuel *= 2
        upperore = makefuel(reactions, upperfuel)

    #print(f"{upperore} ore makes {upperfuel} fuel")

    #Binary search
    while upperfuel-lowerfuel > 1:
        midfuel = (upperfuel+lowerfuel)//2
        midore = makefuel(reactions,midfuel)

        if midore > orecount:
            #Move upper bound down
            upperfuel = midfuel
            upperore = midore
        else:
            lowerfuel = midfuel
            lowerore = midore

    return lowerfuel


if __name__ == "__main__":
    for chunk in chunks(readinput()):
        reactions: dict[str,tuple[int,list[tuple[str,int]]]] = {}
        for line in chunk:
            bits = line.strip().split()
            outgredient = bits.pop()

            assert outgredient not in reactions

            outcount = int(bits.pop())
            bits.pop() #arrow
            assert len(bits) % 2 == 0 and len(bits)>0
            ingredients = []
            while len(bits)>0:
                ingredient = bits.pop().rstrip(",")
                incount = int(bits.pop())
                ingredients.append((ingredient,incount))
            reactions[outgredient] = (outcount, ingredients)
        #for k,v in reactions.items():
        #    print(k,v)
            
            
        p1 = makefuel(reactions)
        print("Part 1:", p1)

        p2 = maxfuel(reactions)
        print("Part 2:", p2)

        print()
