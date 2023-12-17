#!/usr/bin/env python3

from queue import PriorityQueue
import re
import sys


sys.path.append("../..")
from lib.aoc import *

backwards = {
    "d": "u",
    "u": "d",
    "l": "r",
    "r": "l",
    "x": "y",
}

moves1 = {
    "u": (0,-1, "d"),
    "d": (0,1, "u"),
    "l": (-1,0, "r"),
    "r": (1,0, "l"),
}

moves2 = {}
for m in moves1.keys():
    (dx, dy, reverse) = moves1[m]
    for next in list("udlr"):
        if backwards[m] == next:
            continue
        dx1, dy1, r1 = moves1[next]
        newmove = m + next
        moves2[newmove] = (dx+dx1,dy+dy1, reverse)


moves3 = {}
for m in moves2.keys():
    (dx, dy, reverse) = moves2[m]
    for next in list("udlr"):
        if backwards[m[-1]] == next:
            continue
        dx1, dy1, r1 = moves1[next]
        newmove = m + next
        moves3[newmove] = (dx+dx1,dy+dy1, reverse)

p1moves = moves1|moves2|moves3

p2moves = {}
for d in moves1.keys():
    (dx, dy, reverse) = moves1[d]
    for i in range(4,11):
        p2moves[d*i] = (dx*i,dy*i,reverse)
        
def inside(pos,bounds):
    x,y=pos
    xmax,ymax=bounds
    if x<0 or y<0: return False

    if x>=xmax or y>=ymax: return False

    return True


fourstraight = re.compile("uuuu|dddd|llll|rrrr")

def findpath(grid: list[list[int]], part2=False):
    part1 = not part2

    size_x, size_y = len(grid[0]), len(grid)

    if part2:
        moves = p2moves
    else:
        moves = p1moves
 
    #visited = set() #Node visited at all
    visited = set() #(pos, last 3 bits of path)
    
    frontier = PriorityQueue()

    bounds = (size_x, size_y)
    finish = (size_x-1, size_y-1)

    #c0 = grid[0][0]

    #Make a heuristics grid, allowing unlimited "closest" moves to target (ignoring the max-3 limit)
    H = [ [0] * size_x for _ in range(size_y)]

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

    frontier.put((0, 0, (0,0), ("x", "x", "x")))


    while not frontier.empty():
        _, c, pos, fullpath = frontier.get()

        x,y = pos[0], pos[1]
        path = fullpath[-3:]

        #We have visited this node from the same direction
        state = (pos,path)
        if state in visited:
            continue

        visited.add(state)

        if pos == finish:
            #Check the path cost by traversing grid
            solution = fullpath[3:]
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
        
        for dir in moves.keys():
            dx, dy, reverse = moves[dir]

            #No reversing allowed
            laststep = path[-1]
            if reverse == laststep:
                continue

            #Make sure we don't keep going in same direction
            if part2:
                laststep = path[-1]
                nextstep = dir[0]
                if laststep == nextstep:
                    continue

            nx, ny = x+dx, y+dy
            nextpos = (nx,ny)

            #Don't go outside grid
            if not inside(nextpos, bounds): continue

            #Ban 4 straight of the same move
            if part1:
                lastpath = path + tuple(dir)
                if fourstraight.search("".join(lastpath)): continue

            nextpath = fullpath + tuple(dir)
            nextstate = (nextpos, nextpath[-3])

            #Don't enqueue to visited nodes
            if nextstate in visited: continue

            valid = True
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
                    if not inside((nx1, ny1), bounds):
                        valid = False
                        break
                    newcost += grid[ny1][nx1]

            if not valid: continue

            #Calcumalate an a* heuristic
            #Manhattan distance
            #h = newcost + (size_x-nx) + (size_y-ny)
            #Cheapest (including disallowed) path
            #h = newcost + H[ny][nx]
            #This is just Dijkstra
            h = newcost


            frontier.put((h, newcost, nextpos, nextpath))

    print("NO PATH FOUND")
    return 0

if __name__ == "__main__":
    input = readinput()

    grid = [ [int(x) for x in list(row)] for row in input]

    p1 = findpath(grid)
    print("Part 1:", p1)

    print()

    p2 = findpath(grid, True)
    print("Part 2:", p2)