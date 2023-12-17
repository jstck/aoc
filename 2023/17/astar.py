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


#This is usually incorrect, as it only does "best path ignoring straight-line-rules" only going left or down
#Seems to work for sample, but not for real input
def makeheuristics_dumb(grid: list[list[int]]) -> list[list[int]]:

    size_x = len(grid[0])
    size_y = len(grid)

    #Make a heuristics grid, allowing unlimited "closest" moves to target (ignoring the max-3 limit)
    H = [ [0] * size_x for _ in range(size_y) ]

    #Target corner
    H[size_y-1][size_x-1] = grid[size_y-1][size_x-1]

    #bottom row
    for x in range(size_x-2,-1,-1):
        H[size_y-1][x] = H[size_y-1][x+1] + grid[size_y-1][x]
    
    #rightmost column
    for y in range(size_y-2,-1,-1):
        H[y][size_x-1] = H[y+1][size_x-1] + grid[y][size_x-1]

    #Rest, bottom up
    for y in range(size_y-2,-1,-1):
        for x in range(size_x-2,-1,-1):
            H[y][x] = grid[y][x] + min(H[y+1][x], H[y][x+1])

    return H

#Dijkstra your eyes out to find guaranteed at-least-as-good paths
#Go from finish and make sure to get all blocks
def makeheuristics(grid: list[list[int]]) -> list[list[int]]:


    size_x = len(grid[0])
    size_y = len(grid)
    bounds = (size_x, size_y)

    #Blank grid
    H = [ [9999] * size_x for _ in range(size_y) ]


    startx,starty = size_x-1,size_y-1

    visited = set()

    q = PriorityQueue()
    q.put((0, startx, starty))

    while not q.empty():
        c,x,y = q.get()
        pos = (x,y)
        if pos in visited: continue
        H[y][x]=c
        visited.add(pos)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x+dx,y+dy
            newpos = (nx,ny)
            if not inside(newpos, bounds): continue
            if newpos in visited: continue
            newcost = c + grid[y][x]
            q.put((newcost, nx, ny))

    return H


def inside(pos,bounds):
    x,y=pos
    xmax,ymax=bounds
    if x<0 or y<0: return False

    if x>=xmax or y>=ymax: return False

    return True

def findpath(grid: list[list[int]], moves: dict[str,tuple[int,int,str]], astar_guess: list[list[int]]) -> int:

    size_x, size_y = len(grid[0]), len(grid)

    visited = set() #(pos, step made to get here)
    
    frontier = PriorityQueue()

    bounds = (size_x, size_y)
    finish = (size_x-1, size_y-1)

    frontier.put((0, 0, (0,0), ("x",)))


    while not frontier.empty():
        _, c, pos, fullpath = frontier.get()

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

            #Calcumalate an a* heuristic (greek for "lowball guess")
            #Manhattan distance
            #h = newcost + (size_x-nx) + (size_y-ny)
            #Cheapest (including disallowed) path
            h = newcost + astar_guess[ny][nx]
            #This is just Dijkstra
            #h = newcost

            frontier.put((h, newcost, nextpos, nextpath))

    print("NO PATH FOUND")
    return 0

if __name__ == "__main__":
    t0 = time.process_time()

    input = readinput()

    grid = [ [int(x) for x in list(row)] for row in input]

    t1 = time.process_time()
    astar_guess = makeheuristics(grid)

    t2 = time.process_time()

    p1moves = makelongermoves(1,3)
    p1 = findpath(grid, p1moves, astar_guess)
    print("Part 1:", p1)

    t3 = time.process_time()

    p2moves = makelongermoves(4,10)
    p2 = findpath(grid, p2moves, astar_guess)
    print("Part 2:", p2)

    t4 = time.process_time()

    print()
    print(f"Parsing:    {t1-t0:0.4f}s")
    print(f"Heuristics: {t2-t1:0.3f}s")
    print(f"Part1:      {t3-t2:0.3f}s")
    print(f"Part2:      {t4-t3:0.3f}s")
    print(f"Total:      {t4-t0:0.3f}s")