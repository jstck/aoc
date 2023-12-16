#!/usr/bin/env python3

from queue import Queue
import sys


sys.path.append("../..")
from lib.aoc import *

UP="u"
RIGHT="r"
DOWN="d"
LEFT="l"

def visitnodes(visited: set[tuple[int,int,str]], grid: list[str], q: Queue[tuple[int,int,str]], x: int , y: int, dir: str):

    cur = (x,y,dir)

    size_x, size_y = len(grid[0]), len(grid)
    

    #Check if we're off the grid
    if x<0 or x>=size_x or y<0 or y>=size_y:
        return


    #This state has already been done
    if cur in visited:
        return
    
    visited.add(cur)

    tile = grid[y][x]

    match [dir, tile]:

        case ["u", "." | "|"] | ["l", "\\"] | ["r", "/"]:
            q.put((x,y-1,"u"))
        case ["d", "." | "|"] | ["l", "/"] | ["r", "\\"]:
            q.put((x,y+1,"d"))
        case ["l", "." | "-"] | ["u", "\\"] | ["d", "/"]:
            q.put((x-1,y,"l"))
        case ["r", "." | "-"] | ["u", "/"] | ["d", "\\"]:
            q.put((x+1,y,"r"))

        #Splitters
        case ["u" | "d", "-"]:
            q.put((x-1, y, "l"))
            q.put((x+1, y, "r"))
        case ["l" | "r", "|"]:
            q.put((x, y-1, "u"))
            q.put((x, y+1, "d"))
        case [d, t]:
            print(f"Totally invalid thing: {d},{t}")
    
#Get "grid energy" for a certain starting square
def getEnergy(grid: list[str], x: int , y: int, dir: str, printout=False) -> int:
    #Set containing tuples of (x,y,dir) for nodes visited
    visited = set()

    q: Queue[tuple[int,int,str]] = Queue()

    q.put((x,y,dir))
    
    while not q.empty():
        (x,y,dir) = q.get()
        visitnodes(visited, grid, q, x, y, dir)

    #Extract all (x,y) tuples as a set (removes duplicate directions per grid square)
    energized = {(x,y) for (x,y,_) in visited}

    if printout:
        for row in range(len(grid)):
            r = []
            for col in range(len(grid[0])):
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
        maxenergy = max(maxenergy, getEnergy(grid, x, y, dir))

    return maxenergy

if __name__ == "__main__":
    input = readinput()

    p1 = part1(input)
    print("Part 1:", p1)

    p2 = part2(input)
    print("Part 2:", p2)