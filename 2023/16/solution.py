#!/usr/bin/env python3

from queue import Queue
import sys


sys.path.append("../..")
from lib.aoc import *

UP=0
RIGHT=1
DOWN=2
LEFT=3

def visitnodes(visited: set[tuple[int,int,int]], grid: list[str], q: Queue[tuple[int,int,int]], x: int , y: int, dir: int):
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

    assert dir in [0, 1, 2, 3], "Invalid direction: " + str(dir)
    assert tile in ".|-\\/", "Invalid tile: " +  tile

    if dir == UP:
        if tile=="." or tile=="|":
            #Keep going
            q.put((x,y-1,UP))
        elif tile=="\\":
            #Turn left
            q.put((x-1, y, LEFT))
        elif tile=="/":
            #Turn right
            q.put((x+1, y, RIGHT))
        elif tile=="-":
            #Split left+right
            q.put((x-1, y, LEFT))
            q.put((x+1, y, RIGHT))
        else:
            assert False, f"Invalid state x {x} y {y} dir {dir} t '{tile}'"
    
    elif dir == RIGHT:
        if tile=="." or tile=="-":
            #Keep going
            q.put((x+1, y, RIGHT))
        elif tile=="\\":
            #Turn down
            q.put((x, y+1, DOWN))
        elif tile=="/":
            #Turn up
            q.put((x, y-1, UP))
        elif tile=="|":
            #Split
            q.put((x, y-1, UP))
            q.put((x, y+1, DOWN))
        else:
            assert False, f"Invalid state x {x} y {y} dir {dir} t '{tile}'"
    
    elif dir == DOWN:
        if tile=="." or tile=="|":
            #Keep going
            q.put((x, y+1, DOWN))
        elif tile=="\\":
            #Turn right
            q.put((x+1, y, RIGHT))
        elif tile=="/":
            #Turn left
            q.put((x-1, y, LEFT))
        elif tile=="-":
            #Split left+right
            q.put((x-1, y, LEFT))
            q.put((x+1, y, RIGHT))
        else:
            assert False, f"Invalid state x {x} y {y} dir {dir} t '{tile}'"
    
    elif dir == LEFT:
        if tile=="." or tile=="-":
            #Keep going
            q.put((x-1, y, LEFT))
        elif tile=="\\":
            #Turn up
            q.put((x, y-1, UP))
        elif tile=="/":
            #Turn down
            q.put((x, y+1, DOWN))
            
        elif tile=="|":
            #Split
            q.put((x, y-1, UP))
            q.put((x, y+1, DOWN))
        else:
            assert False, f"Invalid state x {x} y {y} dir {dir} t '{tile}'"

    else:
        assert False, f"Invalid state x {x} y {y} dir {dir} t '{tile}'"
    
#Get "grid energy" for a certain starting square
def getEnergy(grid: list[str], x: int , y: int, dir: int) -> int:
    #Set containing tuples of (x,y,dir) for nodes visited
    visited = set()

    q: Queue[tuple[int,int,int]] = Queue()

    q.put((x,y,dir))
    
    while not q.empty():
        (x,y,dir) = q.get()
        visitnodes(visited, grid, q, x, y, dir)

    #Extract all (x,y) tuples as a set (removes duplicate directions per grid square)
    energized = {(x,y) for (x,y,_) in visited}

    return len(energized)



def part1(input: list[str]):
    grid = input

    return getEnergy(grid, 0, 0, RIGHT)

    

def part2(input: list[str]):
    grid = input

    size_x, size_y = len(grid[0]), len(grid)

    edges = []

    for x in range(size_x):
        edges.append((x,0,DOWN))
        edges.append((x,size_y-1,UP))

    for y in range(size_y):
        edges.append((0,y,RIGHT))
        edges.append((size_x,y-1,LEFT))

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