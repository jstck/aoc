#!/usr/bin/env python3

from queue import Queue
from typing import TypeAlias
import sys


sys.path.append("../..")
from lib.aoc import *

UP="u"
RIGHT="r"
DOWN="d"
LEFT="l"

State: TypeAlias = tuple[int,int,str]

NONE_STATE: State = (-1,-1,"X")

statecache: dict[State,set[State]] = {}

def cache_update_all(p: State, s: set[State], q: Queue[State]):

    if p is None:
        return
    
    #Add new set
    if p not in statecache:
        statecache[p] = set()
    statecache[p].update(s)

    #Recursively update anything that contains this node
    for p1, s1 in statecache.items():
        if p in s1:
            q.put(p1)

def cache_update2(p: State, s: set[State]):
    q = Queue()
    q.put(s)

    while not q.empty():
        cache_update_all(p,s,Queue())

def cache_update(p: State, s: set[State]):

    if p is None or p==NONE_STATE:
        return
    
    #Add new set
    if p not in statecache:
        statecache[p] = set()
    statecache[p].update(s)

    #Update all parents
    for p1, s1 in statecache.items():
        if p in s1:
            statecache[p1].update(s)


#Trace all paths from a node. Just does one node and then enqueues rest (0, 1 or 2 options), parents are updated by children later
def tracenode(state: State, grid: list[str], q: Queue[State]):

    if state in statecache:
        #Been here before. We're done.
        return

    size_x, size_y = len(grid[0]), len(grid)
    
    x,y,dir = state

    def inside(s: State) -> bool:
        return 0<=s[0]<size_x and 0<=s[1]<size_y

    #Check if we're off the grid
    if not inside(state):
        return
    
    #visited set always contains starting node.
    visited: set[State] = set([state])
    
    tile = grid[y][x]

    next = []

    match [dir, tile]:

        case ["u", "." | "|"] | ["l", "\\"] | ["r", "/"]:
            next = [(x,y-1,"u")]
        case ["d", "." | "|"] | ["l", "/"] | ["r", "\\"]:
            next = [(x,y+1,"d")]
        case ["l", "." | "-"] | ["u", "\\"] | ["d", "/"]:
            next = [(x-1,y,"l")]
        case ["r", "." | "-"] | ["u", "/"] | ["d", "\\"]:
            next = [(x+1,y,"r")]

        #Splitters
        case ["u" | "d", "-"]:
            next = [ (x-1, y, "l"), (x+1, y, "r") ]
        case ["l" | "r", "|"]:
            next = [ (x, y-1, "u"), (x, y+1, "d") ]
        case [d, t]:
            print(f"Totally invalid thing: {d},{t}")

    #Queue next states, and add this node as "containing" those
    for n in next:
        if inside(n):
            q.put(n)
            visited.add(n)

    #Targets for this node (and parents) at least contains these new ones
    cache_update(state, visited)

    return



#Get "grid energy" for a certain starting square
def getEnergy(grid: list[str], x: int , y: int, dir: str, printout=False) -> int:

    q: Queue[State] = Queue()

    start: State = (x,y,dir)

    q.put(start)
    
    while not q.empty():
        state = q.get()
        tracenode(state, grid, q)

    #Extract all (x,y) tuples as a set (removes duplicate directions per grid square)
    energized = {(x,y) for (x,y,_) in statecache[start]}

    if printout:
        for row in range(len(grid)):
            r = []
            for col in range(len(grid[row])):
                if (col, row) in energized:
                    r.append("#")
                else:
                    r.append(".")
            print("".join(r))

    return len(energized)



def part1(input: list[str]):
    grid = input

    return getEnergy(grid, 0, 0, RIGHT, True)

    

def part2(input: list[str]):
    grid = input

    size_x, size_y = len(grid[0]), len(grid)

    edges = []

    for x in range(size_x):
        edges.append((x,0,DOWN))
        edges.append((x,size_y-1,UP))

    for y in range(size_y):
        edges.append((0,y,RIGHT))
        edges.append((size_x-1,y,LEFT))

    maxenergy = 0
    for (x,y,dir) in edges:
        energy = getEnergy(grid, x, y, dir)
        #print(f"{x} {y} -> {energy}")
        maxenergy = max(maxenergy, energy)

    return maxenergy

if __name__ == "__main__":
    input = readinput()

    p1 = part1(input)
    print("Part 1:", p1)

    print()
    e = getEnergy(input, 3, 0, "d", True)
    print("P2 answer:", e)
    print()

    p2 = part2(input)
    print("Part 2:", p2)

    print()
    e = getEnergy(input, 3, 0, "d", True)
    print("P2 answer:", e)