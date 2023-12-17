#!/usr/bin/env python3

from queue import PriorityQueue
import sys
import time

sys.path.append("../..")
from lib.aoc import *

backwards = {
    "d": "u",
    "u": "d",
    "l": "r",
    "r": "l",
    "x": "y",
}
#All 1-step moves
moves1 = {
    "u": (0,-1, "d"),
    "d": (0,1, "u"),
    "l": (-1,0, "r"),
    "r": (1,0, "l"),
}

def makelongermoves(min, max):
    result = {}
    for d in moves1.keys():
        (dx, dy, reverse) = moves1[d]
        for i in range(min,max+1):
            result[d*i] = (dx*i,dy*i,reverse)
    return result

        
def inside(pos,bounds):
    x,y=pos
    xmax,ymax=bounds
    if x<0 or y<0: return False

    if x>=xmax or y>=ymax: return False

    return True

def findpath(grid: list[list[int]], moves: dict[str,tuple[int,int,str]]):

    size_x, size_y = len(grid[0]), len(grid)

    visited = set() #(pos, step made to get here)
    
    frontier = PriorityQueue()

    bounds = (size_x, size_y)
    finish = (size_x-1, size_y-1)

    frontier.put((0, (0,0), ("x",)))


    while not frontier.empty():
        c, pos, fullpath = frontier.get()

        laststep = fullpath[-1]

        #We have visited this node via the same path (last3)
        state = (pos,laststep)
        if state in visited:
            continue

        visited.add(state)

        if pos == finish:
            return c

            #Check the path cost by traversing grid
            solution = fullpath[1:]
            x=y=0
            cost=0
            for d in solution:
                dx,dy,_ = moves1[d]
                x += dx
                y += dy
                cost += grid[y][x]

            print("".join(solution))
            print("Path cost:", cost)
            print()

            return c
        
        x,y = pos
        
        for dir in moves.keys():
            dx, dy, reverse = moves[dir]

            #No reversing allowed
            if reverse == laststep:
                continue

            #Make sure we don't keep going in same direction
            nextstep = dir[0]
            if laststep == nextstep:
                continue

            nx, ny = x+dx, y+dy
            nextpos = (nx,ny)

            #Don't go outside grid
            if not inside(nextpos, bounds): continue

            nextpath = fullpath + tuple(dir)
            nextstate = (nextpos, nextpath[-1])

            #Don't enqueue visited nodes
            if nextstate in visited: continue

            if len(dir) == 1:
                #Single step
                newcost = c + grid[ny][nx]
            else:
                #Check multi-step as individual parts and make sure we don't stray outside grid and sum up cost
                nx1, ny1 = x, y
                newcost = c
                for istep in list(dir):
                    dx1, dy1, r = moves1[istep]
                    nx1 += dx1
                    ny1 += dy1
                    newcost += grid[ny1][nx1]

            frontier.put((newcost, nextpos, nextpath))

    print("NO PATH FOUND")
    return 0

if __name__ == "__main__":
    t0 = time.process_time()

    input = readinput()

    grid = [ [int(x) for x in list(row)] for row in input]

    t1 = time.process_time()

    p1moves = makelongermoves(1,3)
    p1 = findpath(grid, p1moves)
    print("Part 1:", p1)

    t2 = time.process_time()

    p2moves = makelongermoves(4,10)
    p2 = findpath(grid, p2moves)
    print("Part 2:", p2)

    t3 = time.process_time()

    print()
    print(f"Parsing:    {t1-t0:0.4f}s")
    print(f"Part1:      {t2-t1:0.3f}s")
    print(f"Part2:      {t3-t2:0.3f}s")
    print(f"Total:      {t3-t0:0.3f}s")