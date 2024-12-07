#!/usr/bin/env python3

import sys
sys.path.append("../..")
from lib.aoc import *
from collections import defaultdict
from lib.grid import Grid


def turnright(dir: tuple[int,int]) -> tuple[int,int]:
    #Normally multiplying by i would rotate left/counterclockwise, but we're doing "positive down" in this grid so it's mirrored
    z = complex(dir[0],dir[1]) * complex(0,1)
    return (int(z.real),int(z.imag))

def part1(g: Grid) -> int:

    visited: set[tuple[int,int]] = set()

    pos = next(grid.findvalue("^"))

    visited.add(pos)

    #Up
    direction = (0,-1)
    
    while True:
        newpos = (pos[0]+direction[0],pos[1]+direction[1])

        if newpos[0] < 0 or newpos[0] >= grid.size_x or newpos[1] < 0 or newpos[1] >= grid.size_y:
            #Gone outside grid, we're done.
            g2 = grid.copy()
            for _, pos in enumerate(visited):
                g2[pos] = "X"
            print(g2)

            return len(visited)
        
        if grid[newpos] == "#":
            #Hit obstacle, turn
            direction = turnright(direction)
            continue

        #Take a step
        pos = newpos
        visited.add(pos)

#Similar to part 1, but instead of just positions, keep track of pos+dir to find loops
def findloop(grid: Grid) -> int:
    

    pos = next(grid.findvalue("^"))
    direction = (0,-1)

    visited: set[tuple[tuple[int,int],tuple[int,int]]] = set()


    visited.add((pos,direction))

    
    while True:
        newpos = (pos[0]+direction[0],pos[1]+direction[1])

        if newpos[0] < 0 or newpos[0] >= grid.size_x or newpos[1] < 0 or newpos[1] >= grid.size_y:
            #Gone outside grid, no loop found
            return False
        
        if grid[newpos] == "#":
            #Hit obstacle, turn
            direction = turnright(direction)
            continue

        #Take a step
        pos = newpos

        if (pos,direction) in visited:
            #Been at this place in this direction before, loop found
            return True
        visited.add((pos,direction))

def part2(g:  Grid) -> int:
    loopcount = 0
    for (x,y,c) in g.enumerate():
        
        #Can't block start
        if c == "^": continue

        #No point adding obstacle where one is already
        if c == "#": continue

        #Add an obstacle and run it
        g2 = g.copy()
        g2[(x,y)] = "#"

        #print("testing",x,y)
        if findloop(g2):
            print("Found loop at",x,y)
            loopcount += 1
    return loopcount
    
        



if __name__ == "__main__":

    grid = Grid(readinput())

    print("Part 1:", part1(grid))
    print("Part 2:", part2(grid))