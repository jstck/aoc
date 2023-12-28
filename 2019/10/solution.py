#!/usr/bin/env python3
from __future__ import annotations

from math import gcd
import sys
from sympy import atan2, pi, Expr

sys.path.append("../..")
from lib.aoc import *
from lib.grid import Grid



def part1(input: list[str]) -> tuple[int,int,int]:
    orig_grid = Grid(input)
    #print(orig_grid.header())
    #print(orig_grid)
    size_x = orig_grid.size_x
    size_y = orig_grid.size_y

    asteroids = set( (x,y) for x,y,val in orig_grid.enumerate() if val!=".")

    bestcount = 0
    bestx,besty = -1,-1

    for (x,y) in asteroids:
    #for (x,y) in [(5,8)]:

        count = 0
        
        remaining = asteroids.copy()
        #Itself doesn't count
        remaining.remove((x,y))

        #Iterate over all other spots by manhattan distance

        #Max manhattan distance from this spot
        maxhattan = max(x, size_x-x) + max(y, size_y-y)
        #print(f"Potential base at {x},{y} (maxhattan {maxhattan})")
        for manhattan in range(1, maxhattan+1):
            for dx in range(0,manhattan+1):
                dy = manhattan-dx
                for quadrant in ((1,1), (-1,1), (-1,-1), (1,-1)):
                    dx1,dy1 = dx*quadrant[0],dy*quadrant[1]
                    x1,y1 = x+dx1,y+dy1

                    if not (x1,y1) in remaining: continue

                    #print(f"  Sees asteroid at {x1},{y1} ({orig_grid[x1,y1]})")
                    remaining.remove((x1,y1))

                    count += 1

                    #Integer-sized steps of this coordinate
                    size = gcd(dx1,dy1)
                    stepx,stepy = dx1//size, dy1//size

                    nsteps = 1
                    while True:
                        nsteps += 1
                        blockx, blocky = x+nsteps*stepx, y+nsteps*stepy
                        if blockx<0 or blockx>=size_x or blocky<0 or blocky>=size_y:
                            break
                        if (blockx,blocky) in remaining:
                            #print(f"    Blocks asteroid at {blockx},{blocky}  ({orig_grid[blockx,blocky]})")
                            remaining.remove((blockx,blocky))
        #print(f"Sees {count} other asteroids")
        #print(len(remaining))

        if count > bestcount:
            bestcount = count
            bestx,besty = x,y

        #print()

    return bestx,besty,bestcount

def part2(input: list[str], x0:int, y0:int):

    grid = Grid(input)

    asteroids: dict[Expr,list] = dict()

    for x, y, v in grid.enumerate():
        if v != "#":
            continue

        dx,dy = x-x0,y-y0
        if dx==0 and dy==0: continue

        #Distance squared
        dist = dx*dx+dy*dy

        angle = atan2(dx,-dy)
        if angle < 0: # type: ignore
            angle += 2*pi
        
        datta = (dist, x, y)
        if angle in asteroids:
            asteroids[angle].append(datta)
        else:
            asteroids[angle] = [datta]

    #for k,v in asteroids.items():
    #    print(k,len(v))

    angles = list(asteroids.keys())
    #print(angles)
    angles.sort(key=lambda x: x) # type: ignore
    

    #Sort every angle by distance (first element of tuple) in reverse order, so we can pop them.
    for v in asteroids.values():
        v.sort(reverse=True)

    #for angle in angles:
    #    print(angle, len(asteroids[angle]), asteroids[angle]) # type: ignore

    lazorcount = 0

    score = 0

    lazored = True
    while lazored:
        lazored = False
        for angle in angles:
            if len(asteroids[angle])>0:
                _, x, y = asteroids[angle].pop()
                lazorcount += 1
                print(f"Lazored {lazorcount:3} - {x},{y}")

                if lazorcount == 200:
                    score = x*100+y
                lazored = True


    return score


if __name__ == "__main__":

    for chunk in chunks(readinput()):
        #Check if answer on first line
        facit = None
        if chunk[0][0] == "A":
            answer = chunk[0]
            chunk = chunk[1:]

            facit = tuple(int(x) for x in answer.split(" ")[1].split(","))

        p1 = part1(chunk)
        print("Part 1:", p1)
        if facit is not None:
            print("Should be: ", facit)
        x,y,_ = p1
        print()

        p2 = part2(chunk, x, y)
        print("Part 2:", p2)