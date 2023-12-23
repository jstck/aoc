#!/usr/bin/env python3

import functools
from functools import cache
from itertools import combinations
import itertools
import collections
from queue import PriorityQueue, SimpleQueue
import heapq
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, TypeAlias

import math
import re
import sys

Pos: TypeAlias = tuple[int,int]
WeightedPos: TypeAlias = tuple[int,int,int]
Graph: TypeAlias = dict[Pos,list[WeightedPos]]


sys.path.append("../..")
from lib.aoc import *

def findvertices(grid: list[str]) -> list[Pos]:
    size_x = len(grid[0])
    size_y = len(grid)

    #Find start and finish positions
    start_x = grid[0].find(".")
    finish_x = grid[-1].find(".")

    startpos = (start_x, 0)
    finishpos = (finish_x, size_y-1)

    vertices: list[Pos] = [startpos, finishpos]

    #Look for all the vertexicexes in the graph; any spot that has more than two path neighbours from it
    for x in range(1,size_x-1):
        for y in range(1,size_y-1):

            if grid[y][x] == "#": continue

            nabo = 0
            for dx,dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                x1,y1=x+dx,y+dy
                if grid[y1][x1] in ".<>^v":
                    nabo+=1
            if nabo >= 3:
                #print(f"Vertex found at {x1},{y1}")
                vertices.append( (x,y) )

    return vertices


def findneighbours(grid: list[str], startpos: Pos, vertices: list[Pos], part2=False) -> list[tuple[Pos,tuple[tuple[WeightedPos,...]]]]:
    #print("Neighboursing", startpos)
    neighbours = []

    #queue tuple with cost so far and path of (x,y) tuples
    q: PriorityQueue[tuple[int,tuple[Pos,...]]] = PriorityQueue()

    size_x = len(grid[0])
    size_y = len(grid)

    slopes = not part2

    q.put((0,(startpos,)))

    while not q.empty():
        length, path = q.get_nowait()

        pos = path[-1]

        if pos != startpos and pos in vertices:
            neighbours.append(pos+(length,))
            continue

        for dx,dy,dir in [ (-1,0,"l"), (1,0,"r"), (0,-1,"u"), (0,1,"d")]:
            nextpos = x,y = pos[0]+dx,pos[1]+dy

            #Bounds checking: only needed in y direction (from start/finish positions)
            if y>=size_y or y<0: continue

            #Don't step backwards or cross path
            if nextpos in path: continue

            gridsquare = grid[y][x]

            #Stop at 
            if gridsquare == "#": continue
            elif slopes and gridsquare == "<" and dir != "l": continue
            elif slopes and gridsquare == ">" and dir != "r": continue
            elif slopes and gridsquare == "^" and dir != "u": continue
            elif slopes and gridsquare == "v" and dir != "d": continue

            nextpath = path + (nextpos,)
            q.put( (length+1,nextpath))

    return neighbours


def buildgraph(grid: list[str], part2=False) -> tuple[Graph,Pos,Pos]:
    vertices = findvertices(grid)
    #print(vertices)

    startpos = vertices[0]
    finishpos = vertices[1]

    graph = {}

    for vertex in vertices:
        neighbours = findneighbours(grid, vertex, vertices, part2)
        graph[vertex] = neighbours

    return graph, startpos, finishpos

def findlongest(graph: Graph, start: Pos, finish: Pos) -> int:

    #queue tuple with cost so far and path of (x,y) tuples
    q: PriorityQueue[tuple[int,tuple[Pos,...]]] = PriorityQueue()

    q.put( (0, (start,)) )

    maxpath = 0

    while not q.empty():
        length, path = q.get_nowait()
        pos = path[-1]

        #print("at", pos, grid[pos[1]][pos[0]], length)

        if pos == finish:
            #print("Found solution of length", length)
            maxpath = max(maxpath,length)
            continue

        #Check all neighbouring directions:
        for x,y,cost in graph[pos]:
            nextpos = (x,y)

            #Don't step backwards or cross path
            if nextpos in path:
                continue

            nextpath = path + (nextpos,)
            q.put( (length+cost, nextpath) )

    return maxpath

#Naive solution, works fine for part 1 and part 2 sample...
def findpaths(grid: list[str], slopes=True) -> list[tuple[tuple[int,int],...]]:

    #path is a tuple of (x,y) tuples

    q: PriorityQueue[tuple[int,tuple[tuple[int,int],...]]] = PriorityQueue()

    size_x = len(grid[0])
    size_y = len(grid)

    #Find start and finish positions
    start_x = grid[-1].find(".")
    finish_x = grid[0].find(".")

    startpos = (start_x, size_x-1)
    finishpos = (finish_x, 0)

    q.put( (0, ((startpos),)))

    solutions: list[tuple[tuple[int,int],...]] = []

    while not q.empty():
        length, path = q.get_nowait()
        pos = path[-1]

        #print("at", pos, grid[pos[1]][pos[0]], length)

        if pos == finishpos:
            print("Found solution of length", length)
            solutions.append(path)
            continue

        #Check all neighbouring directions:
        for dx,dy,dir in [ (-1,0,"l"), (1,0,"r"), (0,-1,"u"), (0,1,"d")]:
            nextpos = x,y = pos[0]+dx,pos[1]+dy

            #Bounds checking: only need to check going down from start pos, rest of maze is bounded
            if y>=size_y:
                continue

            #Don't step backwards or cross path
            if nextpos in path:
                continue

            gridsquare = grid[y][x]

            #Stop at 
            if gridsquare == "#":
                continue
            elif slopes and gridsquare == ">" and dir != "l":
                continue
            elif slopes and gridsquare == "<" and dir != "r":
                continue
            elif slopes and gridsquare == "v" and dir != "u":
                continue
            elif slopes and gridsquare == "^" and dir != "d":
                continue

            assert gridsquare in [".","<",">","^","v"], f"Invalid grid square: {gridsquare}"
            nextpath = path + (nextpos,)
            q.put( (length+1,nextpath))

    return solutions



def part1(input: list[str]) -> int:
    #allpaths = findpaths(input)
    #return max(map(len,allpaths))-1

    graph, startpos, finishpos = buildgraph(input)
    return findlongest(graph, startpos, finishpos)

def part2(input: list[str]) -> int:
    graph, startpos, finishpos = buildgraph(input,True)
    return findlongest(graph, startpos, finishpos)
    

if __name__ == "__main__":
    input = readinput()

    p1 = part1(input)
    print("Part 1:", p1)

    p2 = part2(input)
    print("Part 2:", p2)