#!/usr/bin/env python3

import sys
from queue import PriorityQueue

sys.path.append("../..")
from lib.grid import Grid

from IntCodeVM import IntCodeVM

beamcache = {}
def getBeam(program: list[int], x:int, y:int) -> bool:
    if (x,y) in beamcache:
        return beamcache[x,y]
    
    vm = IntCodeVM(program)
    vm.input_buffer.put_nowait(x)
    vm.input_buffer.put_nowait(y)
    vm.run()
    out = (vm.output_buffer.get_nowait() == 1)

    beamcache[x,y] = out

    return out


def part1(program: list[int]):

    data = []
    count = 0

    for y in range(50):
        row = []
        for x in range(50):
            beam = getBeam(program, x, y)
            if beam:
                count += 1
                row.append("#")
            else:
                row.append(".")
        data.append(row)

    grid = Grid(data)

    #print(grid)

    print("Part 1: ", count)

    #Find a good starting spot for part 2. A square where it as well as it's neighbours down and to the right are all #
    startpos = None
    for x, y, tile in grid.enumerate():
        if tile == "#" and grid[x+1,y] == "#" and grid[x,y+1]== "#":
            startpos = (x,y)
            break

    assert startpos is not None
    print("A good starting spot:", startpos)

    return count, startpos


def part2(program: list[int], startpos: tuple[int,int]=(50,40)):

    shipsize = 100-1

    #For each X coordinate, there's a lower and upper Y-coordinate, between which all squares should be filled.

    #Fill up with fake data until there's a good start spot for us
    x,y=startpos

    upper = [y]*(x-1)
    lower = [y]*(x-1)

    #Check if a ship fits in this upper-left coordinate:
    def shipfits(x,y):
        if y < upper[x]: return False  #Top left
        if y+shipsize > lower[x]: return False #Bottom left
        if y < upper[x+shipsize]: return False #Top right
        if y+shipsize > lower[x+shipsize]: return False
        return True


    while True:
        x = len(upper)
        u = upper[-1]
        l = lower[-1]

        #Look for upper bound. Start at current value, go down until we get a hit
        while not getBeam(program, x,u):
            u+=1

        #Look for lower bound, check for "non-hit" one square below.
        while getBeam(program, x,l+1):
            l+=1

        upper.append(u)
        lower.append(l)

        #if x%100==0:
        #    print(f"X {x}: {u} - {l}")

        if x>=shipsize+startpos[0]:
            #Check to see if a ship would fit (with upper-right corner in this spot)
            x0 = x-shipsize
            y0 = u
            if shipfits(x0,y0):
                score = x0*10000+y0 
                print(f"Can fit a ship (A) at {x0},{y0}. Score: {score}")
                return score

            #Check to see if a ship would fit with lower-right corner 100 steps back and as low as it will go
            x0 = x-shipsize
            y0 = lower[x0]- shipsize
            if shipfits(x0,y0):

                score = x0*10000+y0 
                print(f"Can fit a ship (B) at {x0},{y0}. Score: {score}")
                return score
            

            
            

if __name__ == "__main__":
    program = [int(x) for x in sys.stdin.readline().strip().split(",")]
    p1, p2start = part1(program)

    p2 = part2(program, p2start)
