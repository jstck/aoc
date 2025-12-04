#!/usr/bin/env python3

import functools
from functools import cache
from itertools import combinations
import itertools
import collections
from queue import PriorityQueue
import heapq
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Union, Optional, Iterable

import math
import re
import sys


sys.path.append("../..")
from lib.aoc import *
from lib.grid import Grid

def step(pos: tuple[int,int], dir: str, nsteps=1) -> tuple[int,int]:
    x,y = pos
    if dir == "<":
        return (x-nsteps,y)
    if dir == ">":
        return (x+nsteps,y)
    if dir == "^":
        return (x,y-nsteps)
    if dir == "v":
        return (x,y+nsteps)
    
    assert(False)

def printwithbot(grid: Grid[str], bot: tuple[int,int]):
    foo = grid[bot]
    grid[bot] = "@"
    print(grid)
    grid[bot] = foo
    if foo not in [".","@"]:
        print(f"Bot was on a {foo}")

def part1(grid: Grid[str], moves):
    
    #Find the bot and remove it from the grid for now
    bots = list(grid.findvalue("@"))
    assert(len(bots)==1)
    botpos = bots[0]
    grid[botpos] = "."

    for move in moves:

        botx, boty = botpos
        #Get the chunk of grid in the direction of the move
        if move == "<":
            seq = reversed(list(grid.row(boty))[:botx])
        elif move == ">":
            seq = list(grid.row(boty))[botx+1:]
        elif move == "^":
            seq = reversed(list(grid.col(botx))[:boty])
        elif move == "v":
            seq = list(grid.col(botx))[boty+1:]
        else:
            assert(False)

        #See if a move is possible, go along the sequence and see if there's a gap or a wall first
        canmove = False
        for s in seq:
            if s == ".":
                canmove = True
                break
            if s == "#":
                canmove = False
                break

        if not canmove:
            #print("Can not move", move)
            #print()
            continue

        #Move the bot into whatever is in the right direction
        botpos = step(botpos, move)
        if grid[botpos] == "O":
            #Move boxes out of the way. Pick up the one where we are, and step in the direction of the move
            #until there's a gap to put it in
            grid[botpos] = "."
            pos = step(botpos, move)
            while True:
                stuff = grid[pos]
                assert(stuff in [".","O"]) #Make sure we don't hit an unexpected wall we missed earlier
                if grid[pos] == ".": #Put it here
                    grid[pos] = "O"
                    break

                pos = step(pos, move)

    #Put the bot back to print the grid
    #grid[botpos] = "@"
    #print(grid)
    #print()

    #Score the grid
    sum = 0
    for x,y in grid.findvalue("O"):
        sum += x+100*y

    return sum


def expand(grid: Grid[str]) -> Iterable[Iterable[str]]:
    for y in range(grid.size_y):
        row = grid.row(y)
        newrow = []
        for cell in row:
            if cell == ".":
                newrow.extend([".","."])
            elif cell == "#":
                newrow.extend(["#","#"])
            elif cell == "O":
                newrow.extend(["[","]"])
            elif cell == "@":
                newrow.extend(["@","."])
            else:
                assert(False)
        yield newrow

#Cache of which boxes can move, since each box can push on two boxes, but those two then push on the same one.
#This cache needs to be emptied, since it is only valid for a single grid state and move direction
movecache: dict[tuple[int,int], bool] = {}

def canmove(grid: Grid[str], direction: str, pos: tuple[int,int]) -> bool:

    if pos in movecache:
        return movecache[pos]


    if pos == (14,2):
        print(grid)
        return False

    #Horizontal move, much simple.
    if direction in ["<", ">"]:
        #Check what's in that direction
        neighbour = step(pos, direction)
        n = grid[neighbour]
        if n == "#":
            movecache[pos] = False
            return False
        elif n == ".":
            movecache[pos] = True
            return True
        elif n in ["[", "]"]:
            #Piece of box, just see if that can move. Box parts can be seen as individual boxes.
            r = canmove(grid, direction, neighbour)
            movecache[pos] = r
            return r
        assert(False)

    else:
        #Going up or downs
        print("canmove", pos, direction)
        me = grid[pos]
        if me == "[":
            #We're a box and have two neighbours
            n1 = step(pos, direction)
            n2 = step(n1, ">")
            neighbours = [n1, n2]
        else:
            neighbours = [step(pos, direction)]

        for neighbour in neighbours:
            n = grid[neighbour]
            if n == "#":
                movecache[pos] = False
                return False
            elif n == ".":
                pass
            elif n in ["[","]"]:

                if n == "]":
                    #The right side of a box. Let's try pushing on the left side instead.
                    box = step(neighbour, "<")
                else:
                    box = neighbour

                r = canmove(grid, direction, box)
                if r:
                    pass
                else:
                    movecache[pos] = False
                    return False
            else:
                print("WEIRD GRID SQUARE:", n, neighbour)
                assert(False)
        #All the things above/below us can move, so we can too.
        movecache[pos] = True
        return True
    
#Perform a move (that has been verified to work). Will mutilate the grid.
def domove(grid: Grid[str], direction: str, pos: tuple[int,int], bot=False):
    print(f"Domove {pos} {direction}")
    me = grid[pos]
    if me == "." and not bot:
        return
    if me == "#":
        assert(False)

    #Move other thing out of the way
    newspot = step(pos, direction)
    domove(grid, direction, newspot)
    grid[newspot] = me
    grid[pos] = "."

    #Also move other half of box if going up or down
    if direction in ["^", "v"]:
        if me == "[":
            domove(grid, direction, step(pos, ">"))
        if me == "]":
            domove(grid, direction, step(pos, "<"))

            

def part2(grid, moves):
    #Expand the grid. Every box coordinate is it's top left corner

    grid = Grid(expand(grid))

    print(grid)

    #Find the bot and remove it from the grid for now
    bots = list(grid.findvalue("@"))
    assert(len(bots)==1)
    botpos = bots[0]
    grid[botpos] = "."

    for move in moves:
        #Clear the cache for new grid state
        movecache.clear()

        print(f"At {botpos} going {move}")

        if canmove(grid, move, botpos):
            domove(grid, move, botpos, True)
            botpos = step(botpos, move)
            printwithbot(grid, botpos)
        else:
            print("Can't move")
            pass

    print()

    #Put the bot back to print the grid
    grid[botpos] = "@"
    print(grid)
    print()

    #Score the grid
    sum = 0
    for x,y in grid.findvalue("["):
        sum += x+100*y

    return sum


if __name__ == "__main__":
    (grid, moves) = chunks(readinput())

    grid = Grid(grid)
    moves = [m for row in moves for m in row]

    #print(grid)

    p1 = part1(grid.copy(), moves)
    print("Part 1:", p1)

    p2 = part2(grid.copy(), moves)
    print("Part 2:", p2)
