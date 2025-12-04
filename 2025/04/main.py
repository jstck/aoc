#!/usr/bin/env python3

import sys

sys.path.append("../..")
from lib.aoc import *
from lib.grid import Grid

if __name__ == "__main__":
    g = Grid(readinput())

    firstpass = True
    total = 0

    while True:

        accessible = set()

        for (x,y),c in g:
            p = (x,y)
            if c != "@":
                continue #Not a roll of paper

            n = 0
            for _,_,neigh in g.neighboursDiag(p):
                if neigh in ["x", "@"]:
                    n += 1
            if n < 4:
                accessible.add(p)
                g[p] = "x"

        removable = len(accessible)

        total += removable

        if firstpass:
            print(f"Part 1: {removable}")
            firstpass = False

        if removable == 0:
            break

        #print(g)
        for p in accessible:
            g[p] = "."


        


    
    #print(g)
    
    print(f"Part 2: {total}")