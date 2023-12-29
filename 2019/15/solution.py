#!/usr/bin/env python3

import sys
from queue import PriorityQueue

sys.path.append("../..")
from lib.sparsegrid import SparseGrid

from IntCodeVM import IntCodeVM

#Robot moves.
moves = {
    1: (0,-1), #north
    2: (0, 1), #south
    3: (-1,0), #west
    4: (1,0), #east
}

def offset(pos: tuple[int,int], move: tuple[int,int]) -> tuple[int,int]:
    return pos[0]+move[0], pos[1]+move[1]

#Find distance and first step to closest occurence of a given target.
#If no path found, return (max distance to any valid tile, 0) (for finding longest path to anywhere)
def findclosest(maze: SparseGrid, startpos, target) -> tuple[int,int]:

    maxdist=0

    if len(target) == 0:
        assert False, "Target not found"

    #Queue of distance, firstmove, (pos)
    q: PriorityQueue[tuple[int,int,tuple[int,int]]] = PriorityQueue()
    visited: set[tuple[int,int]] = set()
    visited.add(startpos)
    for move, relmove in moves.items():
        mpos = offset(startpos, relmove)
        if mpos in maze and maze[mpos] != "#":
            q.put( (1, move, mpos))

    while not q.empty():
        dist, firstmove, pos = q.get_nowait()

        maxdist = max(maxdist,dist)

        if pos in visited: continue
        visited.add(pos)

        assert pos in maze
        tile = maze[pos]
        assert tile is not None

        #Found 
        if tile == target:
            return dist, firstmove
        elif tile in "S.O":
            #Keep walking, enqueue neighbours (that are not walls, but exist in map)
            for nextpos, nexttile in maze.neighbours(pos):
                if nextpos in visited:
                    continue
                if nexttile == "#":
                    continue
                #print("Queueing", nextpos, "at distance", dist+1)
                q.put_nowait((dist+1,firstmove,nextpos))
        #Hit a wall or something else (should not happen)
        elif tile == "#":
            print(f"Hit wall at pos {str(pos)} dist {dist}")
        else:
            assert False, f"Weird tile: '{tile}' at pos {str(pos)} dist {dist}"

    #Path not found, return "max reachable spot"
    return (maxdist, 0)

def printmaze(maze: SparseGrid[str]):
    xmin,xmax,ymin,ymax = maze.boundingbox()
    for y in range(ymin,ymax+1):
        row = []
        for x in range(xmin,xmax+1):
            pos = (x,y)
            if pos in maze:
                tile = maze[pos]
            else:
                tile = " "
            row.append(tile)
        print("".join(row))
    print()


def fix_oxygen(program: list[int]):

    pos = (0,0)
    maze: SparseGrid[str] = SparseGrid([])

    #Assume we start on an empty square, or it wouldn't be any fun
    maze[pos] = "S"

    #Add "unknown" squares around start
    for neighbour in maze.neighbourPos(pos):
        maze[neighbour] = "?"

    oxypos = (0,0)

    vm = IntCodeVM(program)

    while True:

        #Find position of closest unknown square
        dist, nextmove = findclosest(maze, pos, "?")
        if nextmove==0:
            #No more unknown squares, whole map traversed
            break

        vm.input_buffer.put_nowait(nextmove)

        vm.run()

        assert vm.state == IntCodeVM.STATE_HALT_INPUT

        result = vm.output_buffer.get_nowait()
        nextpos = offset(pos, moves[nextmove])

        if result == 0:
            #Hit a wall
            maze[nextpos] = "#"
        else:
            #Move to new tile
            pos = nextpos

            #Mark any unknown neighbours
            for npos in maze.neighbourPos(pos):
                if npos not in maze:
                    maze[npos] = "?"

            if result == 1:
                maze[pos] = "."
            elif result == 2:
                maze[pos] = "O"
                oxypos = pos
                print(f"Found oxygen at str{oxypos}")
            else:
                assert False, f"Unknown result: {result}"

    printmaze(maze)
    
    dist, _ = findclosest(maze, (0,0), "O")

    print("Part 1: Shortest path to oxygen:", dist)


    #Find longest path from oxygen to anywhere (search to a fake tile)
    dist, nextmove = findclosest(maze, oxypos, "@")
    assert nextmove==0

    print(f"Part 2: Maze filled with oxygen after {dist} minutes")



if __name__ == "__main__":
    program = [int(x) for x in sys.stdin.readline().strip().split(",")]
    fix_oxygen(program)
