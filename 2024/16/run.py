#!/usr/bin/env python3

import functools
from functools import cache
from itertools import combinations
import itertools
import collections
from queue import PriorityQueue
import heapq
from dataclasses import dataclass
from typing import TypeAlias

import math
import re
import sys


sys.path.append("../..")
from lib.aoc import *
from lib.grid import Grid

Pos: TypeAlias = tuple[int,int]
State: TypeAlias = tuple[Pos, int]

#Plain BFS
def part1(grid: Grid[str]) -> int:

    startpos = list(grid.findvalue("S"))
    assert(len(startpos)==1)
    startpos = startpos[0]
    endpos = list(grid.findvalue("E"))
    assert(len(endpos)==1)
    endpos = endpos[0]

    q = PriorityQueue()
    visited: set[State] = set()  #Score, (x, y), direction
    #0 = right 1 = up 2 = left 3 = down, ok?

    q.put_nowait((0,startpos,0))

    while not q.empty():
        score, pos, direction = q.get_nowait()

        if (pos, direction) in visited:
            continue

        visited.add((pos, direction))

        here = grid[pos]
        if here == "#":
            continue

        if here == "E":
            return score
        
        #Go straight
        if direction == 0:
            m = (1,0)
        elif direction == 1:
            m = (0,-1)
        elif direction == 2:
            m = (-1,0)
        elif direction == 3:
            m = (0,1)
        else:
            assert(False)

        newpos = tuple(map(sum, zip(pos, m)))
        q.put_nowait((score+1, newpos, direction))

        #Turn counterclockwise
        newdir = (direction+1)%4
        q.put_nowait((score+1000, pos, newdir))

        #Turn clockwise
        newdir = (direction-1)%4
        q.put_nowait((score+1000, pos, newdir))

    return -1

def part2b(grid: Grid[str]) -> int:

    startpos = list(grid.findvalue("S"))
    assert(len(startpos)==1)
    startpos = startpos[0]
    endpos = list(grid.findvalue("E"))
    assert(len(endpos)==1)
    endpos = endpos[0]

    q: PriorityQueue[tuple[int, State, frozenset[State]]] = PriorityQueue()

    visited: dict[State, tuple[int, set[State]]] = {}  #All states that led to this one, to backtrack (marked with best score to reach state)

    #0 = right 1 = up 2 = left 3 = down, ok?

    #Queue has score, state, previous states to get here
    q.put_nowait((0,(startpos,0),frozenset()))

    bestscore = 1E9 #Upper bound to start with

    while not q.empty():
        score, state, prev = q.get_nowait()

        if state in visited:
            bestscorehere = visited[state][0]
            #Paths here with better score will not happen, because BFS. Can only equal
            if score == bestscorehere:
                #Update with possible states to get here equally quickly
                visited[state][1].update(prev)
            continue #No need to go further

        visited[state] = (score, set(prev))

        pos, direction = state

        here = grid[pos]
        if here == "#":
            continue

        #Don't go further if we're worse than best path (everything "good enough" is already processed)
        if score > bestscore:
            break

        if here == "E":
            if score <= bestscore:
                bestscore = score
                continue
        
        #Go straight
        if direction == 0:
            m = (1,0)
        elif direction == 1:
            m = (0,-1)
        elif direction == 2:
            m = (-1,0)
        elif direction == 3:
            m = (0,1)
        else:
            assert(False)

        newpos: Pos = (pos[0]+m[0], pos[1]+m[1])
        newstate: State = (newpos, direction)
        q.put_nowait((score+1, newstate, prev.union(set([state])) ))

        #Turn counterclockwise
        newdir = (direction+1)%4
        newstate: State = (pos, newdir)
        q.put_nowait((score+1000, newstate, prev.union(set([state]))))

        #Turn clockwise
        newdir = (direction-1)%4
        newstate: State = (pos, newdir)
        q.put_nowait((score+1000, newstate, prev.union(set([state]))))

    print("Best score:", bestscore)
    allvisited = set([endpos])
    for dir in [0,1,2,3]:
        state: State = (endpos, dir)
    print("# things visited:", len())

    return -1


#Dijkstra your eyes out
def part2d(grid: Grid[str]):

    startpos = list(grid.findvalue("S"))
    assert(len(startpos)==1)
    startpos = startpos[0]
    endpos = list(grid.findvalue("E"))
    assert(len(endpos)==1)
    endpos = endpos[0]

    #Unvisited is every "empty cell" (not a wall), for every direction
    unvisited: set[tuple[Pos,int]] = set()

    for pos in itertools.chain(grid.findvalue("."), [startpos, endpos]):
        #Upper bound cost is manhattan distance * 1001 (one move and one turn each step)
        #This won't work if a path takes a long detour and gets back to somewhere close to the start though.
        pass



if __name__ == "__main__":
    input = readinput()

    grid = Grid(input)

    p1 = part1(grid)
    print("Part 1:", p1)

    p2 = part2(grid)
    print("Part 2:", p2)
