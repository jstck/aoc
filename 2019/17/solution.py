#!/usr/bin/env python3

import sys
import math

from IntCodeVM import IntCodeVM
sys.path.append("../..")
from lib.grid import Grid

left = {
    "^": (-1,0),
    ">": (0,-1),
    "v": (1,0),
    "<": (0,1),
}

right = {
    "^": (1,0),
    ">": (0,1),
    "v": (-1,0),
    "<": (0,-1),
}

ahead = {
    "^": (0,-1),
    ">": (1,0),
    "v": (0,1),
    "<": (-1,0),
}

leftturn = {
    "^": "<",
    ">": "^",
    "v": ">",
    "<": "v",    
}

rightturn = {
    "^": ">",
    ">": "v",
    "v": "<",
    "<": "^",    
}


def longestRepeatedSubstring(str):
 
    n = len(str)
    LCSRe = [[0 for x in range(n + 1)] 
                for y in range(n + 1)]
 
    res = "" # To store result
    res_length = 0 # To store length of result
 
    # building table in bottom-up manner
    index = 0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
             
            # (j-i) > LCSRe[i-1][j-1] to remove
            # overlapping
            if (str[i - 1] == str[j - 1] and
                LCSRe[i - 1][j - 1] < (j - i)):
                LCSRe[i][j] = LCSRe[i - 1][j - 1] + 1
 
                # updating maximum length of the
                # substring and updating the finishing
                # index of the suffix
                if (LCSRe[i][j] > res_length):
                    res_length = LCSRe[i][j]
                    index = max(i, index)
                 
            else:
                LCSRe[i][j] = 0
 
    # If we have non-empty result, then insert 
    # all characters from first character to 
    # last character of string
    if (res_length > 0):
        for i in range(index - res_length + 1,
                                    index + 1):
            res = res + str[i - 1]
 
    return res

def addpos(a: tuple[int,int], b: tuple[int,int]) -> tuple[int,int]:
    return (a[0]+b[0],a[1]+b[1])

def cleaningrobot(program: list[int]):

    vm = IntCodeVM(program)
    vm.run()

    outdata = []
    while not vm.output_buffer.empty():
        outdata.append(vm.output_buffer.get_nowait())

    outtext = "".join(list(map(chr, outdata)))

    grid = Grid(outtext.split())
    print(grid)

    score = 0

    startpos = None

    #Find all intersections
    for x, y, tile in grid.enumerate():

        if tile not in "#^v<>": continue

        #Found start pos
        if tile in "^v<>":
            #print(f"Found start position '{tile}' at ({x},{y})")
            startpos = (x,y,tile)

        #Intersections cannot be on the edge (needs four neighbours)
        if x==0 or x==grid.size_x-1 or y==0 or y==grid.size_y-1: continue

        isintersection = True
        for _, _, neighbour in grid.neighbours(x, y):
            if neighbour not in "#^v<>":
                isintersection = False
                break

        if not isintersection: continue

        #print(f"Found intersection at ({x},{y})")
        score += x*y

    #print("Part 1:", score)

    assert startpos is not None, "No start position found"
    
    #Let's assume input data is nice and we always start going to either side. Otherwise first move might be just a number, or "R,R,number"

    x,y,dir = startpos

    path: list[tuple[str,int]] = []

    while True:
        #Check if we're going left or right
        xl,yl = x+left[dir][0], y+left[dir][1]
        xr,yr = x+right[dir][0], y+right[dir][1]

        if grid.inbounds(xl,yl) and grid[xl,yl] in "#^v<>":
            turn = "L"
            dir = leftturn[dir]
        elif grid.inbounds(xr,yr) and grid[xr,yr] in "#^v<>":
            turn = "R"
            dir = rightturn[dir]
        else: #We must have reached the end
            break

        #move ahead as far as we can go
        steps = 0
        sx,sy = ahead[dir]

        while grid.inbounds(x+sx,y+sy) and grid[x+sx,y+sy] in "#^v<>":
            #Mark and move
            grid[x,y] = dir
            x,y = x+sx,y+sy
            steps += 1

        path.append( (turn, steps))

    pathstr = ",".join([f"{turn},{str(dir)}" for turn,dir in path])
    print(pathstr)

    commands = {}

    #Try all reasonable lengths of a (max 20 chars)
    for alen in range(3,21):
        A = pathstr[:alen]
        if A[-1]=="," or pathstr[alen] != ",": continue #Only end on a "full symbol"
        
        apath = pathstr.replace(A, "A")
        apath2 = apath.lstrip("A,")

        #Try B on whatever comes after the first chunk of As
        for blen in range(3,21):
            B = apath2[:blen]
            if "A" in B: break #Gone too far!
            if B[-1]=="," or apath2[blen] != ",": continue #Only end on a "full symbol"

            bpath = apath.replace(B, "B")
            #print(bpath, A, B)

            #After removing all leading A's and B's, C has to be whatever is at the start up until the first A or B (minus the comma before it)
            bpath2 = bpath.lstrip("AB,")
            #maxc = min(bpath2.find("A"),bpath2.find("B")) - 1

            for clen in range(3,21):
                C = bpath2[:clen]
                if "A" in C or "B" in C: break
                if C[-1]=="," or bpath2[clen] != ",": continue #Only end on a "full symbol"
            
                if len(C) > 20: continue

                cpath = bpath.replace(C, "C")

                if len(cpath) > 20: continue

                #Make sure there's only "ABC," in it
                if len(cpath.lstrip("ABC,")) > 0: continue

                #Try building original path and make sure it matches
                origpath = cpath.replace("A",A).replace("B",B).replace("C",C)
                assert origpath == pathstr
                commands = {
                    "main": cpath,
                    "A": A,
                    "B": B,
                    "C": C
                }
                
    

    print()
    #print(grid)
    commands["printout"]="n"
    print(commands)

    #Start over with a new VM
    assert program[0]==1
    program[0]=2
    vm = IntCodeVM(program)

    def sendcommand(command: str):

        while not vm.output_buffer.empty():
            char = vm.output_buffer.get_nowait()
            print(chr(char), end="")
        
        for char in command:
            vm.input_buffer.put_nowait(ord(char))
        vm.input_buffer.put_nowait(10)
        print(f"\033[1m{command}\033[0m")
        vm.run()

    for command in ["main", "A", "B", "C", "printout"]:
        sendcommand(commands[command])

    dust = None
    while not vm.output_buffer.empty():
        c = vm.output_buffer.get_nowait()
        if c < 256: print(chr(c), end="")
        dust = c
    
    print("Part 1:", score)
    print("Part 2:", dust)


if __name__ == "__main__":
    program = [int(x) for x in sys.stdin.readline().strip().split(",")]
    cleaningrobot(program)

