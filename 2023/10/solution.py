#!/usr/bin/env python3

import sys
from typing import Tuple, List, Union

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

dirmap = {
    UP: "up",
    RIGHT: "right",
    DOWN: "down",
    LEFT: "left"
}


def parse(input: list[str]) -> Tuple[List[List[str]],int,int]:
    grid = []
    x = -1
    y = -1
    for i, line in enumerate(input):
        row = list(line.strip())
        grid.append(row)
        try:
            x = row.index("S")
            y = i
        except ValueError:
            pass

    return (grid, x, y)

#Find next step in path, following direction of tiles. Returns None if not valid tile for path
def findpath(grid: List[List[str]], path, posx: int, posy: int, dir: int) -> Union[List[Tuple[int,int]],None]:

    size_x = len(grid[0])
    size_y = len(grid)

    while True:

        #print(f"At ({posx},{posy}) facing {dirmap[dir]}")
        #print(path)

        if dir == UP:
            (nextx, nexty) = posx, posy-1
        elif dir == RIGHT:
            (nextx, nexty) = posx+1, posy
        elif dir == DOWN:
            (nextx, nexty) = posx, posy+1
        elif dir == LEFT:
            (nextx, nexty) = posx-1, posy
        else:
            print("INVALID DIRECTION:",dir)
            assert(False)

        if nextx<0 or nextx>=size_x or nexty<0 or nexty>=size_y:
            print(f"Out of bounds at {nextx} {nexty}")
            assert(False)
        
        nexttile = grid[nexty][nextx]

        if (nextx,nexty) in path:
            assert(nexttile == "S")
            return path
            
        #Continue straight up/down
        if nexttile == "|":
            if dir in [LEFT,RIGHT]:
                return None
            nextdir = dir
            
        #Straight left/right
        elif nexttile == "-":
            if dir in [UP,DOWN]:
                return None
            nextdir = dir

        elif nexttile == "L":
            if dir == DOWN:
                nextdir = RIGHT
            elif dir  == LEFT:
                nextdir = UP
            else: return None

        elif nexttile == "J":
            if dir == DOWN:
                nextdir = LEFT
            elif dir  == RIGHT:
                nextdir = UP
            else: return None

        elif nexttile == "7":
            if dir == UP:
                nextdir = LEFT
            elif dir  == RIGHT:
                nextdir = DOWN
            else: return None

        elif nexttile == "F":
            if dir == UP:
                nextdir = RIGHT
            elif dir  == LEFT:
                nextdir = DOWN
            else: return None

        else:
            #Path hit a non-valid tile. Happens when trying different directions from start.
            return None
        
        path = path + [(nextx, nexty)]
        (posx, posy, dir) = (nextx, nexty, nextdir)

        #print(f"GOING {dirmap[dir]}")

if __name__ == "__main__":
    grid, startx, starty = parse(sys.stdin.readlines())

    size_x = len(grid[0])
    size_y = len(grid)

    print(f"Starting at {startx},{starty}, grid is {size_x}X{size_y}")

    #path: Union[None,List[Tuple[int,int]]] = [(startx,starty)]
    spath = [(startx,starty)]
    path = None

    for dir in [UP,DOWN,LEFT,RIGHT]:
        #print(f"Trying to go {dirmap[dir]}")
        path = findpath(grid, spath, startx, starty, dir)
        if path is None:
            continue
        else:
            print("Path found!")
            break
        

    assert(path is not None)

    #print(path)
    #print()
    #print(len(path))

    showpath = [["."]*size_x for y in range(size_y)]
    for (x,y) in path:
        showpath[y][x]=grid[y][x]
#    for row in showpath:
#        print("".join(row))

    tilesinside = 0
    for x in range(size_x):
        for y in range(size_y):
            if (x,y) in path: continue

            crossings = 0
            lastbend = None
            way_out = showpath[y][x+1:]
            if "S" in way_out:
                way_out = showpath[y][:x]
            for tile in way_out:
                if tile == "|":
                    crossings += 1
                if tile in ["F", "L"]:
                    lastbend = tile
                if tile == "7":
                    if lastbend == "F":
                        crossings += 2
                    elif lastbend == "L":
                        crossings += 1
                    else:
                        assert(False)
                if tile == "J":
                    if lastbend == "L":
                        crossings += 2
                    elif lastbend == "F":
                        crossings += 1
                    else:
                        assert(False)
                

            if crossings % 2 == 1:
                #Odd number of crossings, inside loop
                showpath[y][x] = "I"
                tilesinside += 1
            else:
                showpath[y][x] = "O"

#    for row in showpath:
#        print("".join(row))

    print(f"PART 1: Max distance is {len(path)//2}")

    print(f"PART 2: {tilesinside} tiles inside path")
