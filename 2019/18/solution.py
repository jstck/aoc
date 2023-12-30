#!/usr/bin/env python3
from __future__ import annotations

from functools import cache
from itertools import combinations, permutations
import collections
from queue import PriorityQueue, SimpleQueue
from collections import defaultdict, deque, Counter, OrderedDict
import heapq
from dataclasses import dataclass
import math
import re
import sys
from typing import TypeAlias, Optional, Iterator
from operator import mul

import math
import re
import sys


sys.path.append("../..")
from lib.aoc import *
from lib.grid import Grid


def part1(maze: Grid[str]) -> int:
    #print(maze)

    #Find start position, all keys, and all doors
    startpos = None
    allkeys = set()
    doors = set()
    for x,y,tile in maze.enumerate():
        if tile=="@":
            startpos = (x,y)
        elif tile.isupper():
            doors.add(tile)
        elif tile.islower():
            allkeys.add(tile)

    assert startpos is not None
    assert len(allkeys) > 0
    assert len(doors) > 0

    #print(startpos)
    #print(allkeys)
    #print(doors)

    #Enqueue states as (steps, x, y, (keys)), with keys sorted
    startstate = (0, startpos[0], startpos[1], ())

    #Visited is same thing minus the number of steps
    visited = set()

    q = PriorityQueue()
    q.put(startstate)

    while not q.empty():
        steps, x, y, keys = q.get_nowait()

        state = (x, y, keys)
        if state in visited: continue
        visited.add(state)

        #print(f"Visiting {x},{y} with keys {str(keys)}")

        tile = maze[x,y]

        #On a key?
        if tile.islower():
            #Found a key?
            if tile not in keys:
                #Found a key!
                keys = tuple(sorted(keys + (tile,)))

                if len(keys) == len(allkeys):
                    #Found the final key, done!
                    return steps
                
        #Check all neighbouring spots
        for nx,ny, ntile in maze.neighbours(x,y):
            if ntile == "#": #A wall
                continue

            if ntile.isupper() and not ntile.lower() in keys: #A key we don't have
                continue
                
            nstate = (nx,ny,keys)
            if nstate in visited: continue
        
            nq = (steps+1,nx,ny,keys)
            q.put(nq)


    #No path found
    return -1

#Find all reachable and previously-not-found keys from a given position
#Return x, y, distance and name of each key
findkeys_stash = {}
def findkeys(maze: Grid[str], keys: tuple[str,...], x: int, y: int) -> list[tuple[int,int,int,str]]:

    stashkey = (x, y, keys)
    if stashkey in findkeys_stash:
        return findkeys_stash[stashkey]
    
    result = []

    visited = set()
    q = PriorityQueue()

    q.put((0, x, y))

    while not q.empty():
        dist, x, y = q.get_nowait()
        if (x,y) in visited: continue
        visited.add((x,y))

        tile = maze[x,y]

        if tile.islower() and not tile in keys:
            result.append((x, y, dist, tile))

        for nx,ny,tile in maze.neighbours(x,y):
            if tile == "#":
                continue

            if (nx,ny) in visited:
                continue

            #Make sure we can get through doors
            if tile.isupper() and tile.lower() not in keys:
                continue

            q.put((dist+1, nx, ny))

    findkeys_stash[stashkey] = result
    return result


def part2(maze: Grid[str], part2=True) -> int:
    #print(maze)

    #Find start position, all keys, and all doors
    startpos = None
    allkeys = set()
    doors = set()
    for x,y,tile in maze.enumerate():
        if tile=="@":
            startpos = (x,y)
        elif tile.isupper():
            doors.add(tile)
        elif tile.islower():
            allkeys.add(tile)

    assert startpos is not None

    startx, starty = startpos

    if part2:
        bots = []

        #Make sure it's a valid map for part2
        for _,_,tile in maze.neighbours(startx,starty):
            if tile != ".":
                print("Not a valid map for part 2!")
                return -1

        #Change grid to partition it and add more bots
        #Walls
        for dx,dy in [(-1,0), (0,0), (1,0), (0,-1), (0,1)]:
            maze[startx+dx,starty+dy] = "#"

        #Bots
        for dx,dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            maze[startx+dx,starty+dy] = "@"
            bots.append((startx+dx,starty+dy))
        bots = tuple(bots)
    else:
        bots = ((startx,starty),)

    #print(maze)
        

    #Enqueue states as (steps, ( (bot0x, bot0y), ... ), (keys)), with keys sorted
    startstate = (0, bots, ())

    #Visited is same thing minus the number of steps
    visited = set()

    q: PriorityQueue[tuple[int,tuple[tuple[int,int],...],tuple[str,...]]] = PriorityQueue()
    q.put(startstate)

    maxsteps = 0

    while not q.empty():
        steps, bots, keys = q.get_nowait()

        if steps > maxsteps:
            #print(f"{steps} steps, {len(visited)} states visited, {len(findkeys_stash)} dijkstrings")
            maxsteps = steps

        state = (bots, keys)
        #print(steps, state)
        if state in visited: continue
        visited.add(state)

        #See if any bot found a key
        for i in range(len(bots)):
            x,y = bots[i]
            tile = maze[x,y]

            #On a key?
            if tile.islower():
                #Found a new key?
                if tile not in keys:
                    #Found a key!
                    keys = tuple(sorted(keys + (tile,)))

                    if len(keys) == len(allkeys):
                        #Found the final key, done!
                        return steps

        for i in range(len(bots)):
            x,y = bots[i]

            prebots = bots[:i]
            postbots = bots[i+1:]                    

            #Find all reasonable moves for this bot
            for nx, ny, dist, newkey in findkeys(maze, keys, x, y):
                nkeys = tuple(sorted(keys + (newkey,)))
                nbots = prebots + ((nx,ny),) + postbots
                    
                nstate = (nbots,nkeys)
                if nstate in visited: continue
            
                nq = (steps+dist,nbots,keys)
                q.put(nq)


    #No path found
    return -1

if __name__ == "__main__":

    maze = Grid(readinput())
    
    p1 = part1(maze)
    #p1 = part2(maze, False)
    print("Part 1:", p1)

    p2 = part2(maze)
    print("Part 2:", p2)