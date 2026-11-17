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

ScoreState: TypeAlias = tuple[int, State]

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


def part2(grid: Grid[str]) -> int:

    startpos = list(grid.findvalue("S"))
    assert(len(startpos)==1)
    startpos = startpos[0]
    endpos = list(grid.findvalue("E"))
    assert(len(endpos)==1)
    endpos = endpos[0]

    # Predecessor states for any state, to backtrack and count.
    predecessors: dict[State, set[State]] = {}

    q = PriorityQueue()
    visited: set[State] = set()  #Score, (x, y), direction

    bestscores: dict[State, int] = {}  #Best score to reach this state
    #0 = right 1 = up 2 = left 3 = down, ok?

    bestfinish = 1E9

    q.put_nowait((0,startpos,0,None))

    while not q.empty():
        score, pos, direction, prev = q.get_nowait()

        state: State = (pos, direction)

        if (pos, direction) in visited:
            if score == bestscores[(pos, direction)]:
                #Update with possible states to get here equally quickly
                predecessors[state].add(prev)
            
            continue

        visited.add((pos, direction))
        bestscores[(pos, direction)] = score
        predecessors[state] = set([prev]) if prev is not None else set()

        here = grid[pos]
        if here == "#":
            continue

        if here == "E":
            bestfinish = min(bestfinish, score)
            #print("Found end with score", score, "at", pos, "from", prev)
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

        newpos = tuple(map(sum, zip(pos, m)))
        q.put_nowait((score+1, newpos, direction, state))

        #Turn counterclockwise
        newdir = (direction+1)%4
        q.put_nowait((score+1000, pos, newdir, state))

        #Turn clockwise
        newdir = (direction-1)%4
        q.put_nowait((score+1000, pos, newdir, state))

    #Backtrack to count all unique states that led to the end position

    @cache
    def allPredTiles(state: State) -> set[Pos]:

        pos: Pos = state[0]

        if pos == startpos:
            return set([pos])

        #No predecessors means this somewhere we never got (finish with unused
        #incoming direction)
        if state not in predecessors:
            return set()

        allvisited: set[Pos] = set([pos])

        for pred in predecessors[state]:
            allvisited.update(allPredTiles(pred))

        return allvisited

    alltiles: set[Pos] = set()

    for dir in range(4):
        state: State = (endpos, dir)
        if bestscores.get(state, 1E9) == bestfinish:
            alltiles.update(allPredTiles(state))

    return len(alltiles)

if __name__ == "__main__":
    input = readinput()

    grid = Grid(input)

    p1 = part1(grid)
    print("Part 1:", p1)

    p2 = part2(grid)
    print("Part 2:", p2)
