#!/usr/bin/env python3

import sys
import math

from IntCodeVM import IntCodeVM

def part1(program: list[int]):

    screen: dict[tuple[int,int],int] = {}

    vm = IntCodeVM(program)
    vm.run()

    blocks = 0

    score = -1

    xmin = xmax = ymin = ymax = 0

    while not vm.output_buffer.empty():
        x = vm.output_buffer.get_nowait()
        y = vm.output_buffer.get_nowait()
        t = vm.output_buffer.get_nowait()
        screen[(x,y)] = t

        if (x,y) == (-1,0):
            score = t
            continue

        xmin = min(xmin,x)
        xmax = max(xmax,x)
        ymin = min(ymin,y)
        ymax = max(ymax,y)

        if t == 2:
            blocks += 1

    #print(f"Score: {score}")
    #for y in range(ymin,ymax+1):
    #    row = []
    #    for x in range(xmin,xmax+1):
    #        c = screen.get((x,y), 5)
    #        row.append(" #*=O."[c])
    #    print("".join(row))
            

    return blocks

def part2(program: list[int]) -> int:
    program[0]=2 #Hack in money

    vm = IntCodeVM(program)

    rounds = 0
    

    screen: dict[tuple[int,int],int] = {}
    paddlepos = None
    ballpos = None
    score = -1
    blocks = 0

    xmin = xmax = ymin = ymax = 0

    showdisplay = False

    while True:
        vm.run()

        while not vm.output_buffer.empty():
            x = vm.output_buffer.get_nowait()
            y = vm.output_buffer.get_nowait()
            t = vm.output_buffer.get_nowait()
            
            if (x,y) == (-1,0):
                score = t
                continue

            screen[(x,y)] = t

            xmin = min(xmin,x)
            xmax = max(xmax,x)
            ymin = min(ymin,y)
            ymax = max(ymax,y)

            if t==3:
                paddlepos = (x,y)
            elif t==4:
                ballpos = (x,y)

        assert paddlepos is not None
        assert ballpos is not None

        curblocks = len([v for _,v in screen.items() if v==2])

        #Display screen
        if showdisplay:
            print()
            print()
            print(f"Round: {rounds:5}   blocks: {curblocks:4}  score: {score:5}")
            for y in range(ymin,ymax+1):
                row = []
                for x in range(xmin,xmax+1):
                    c = screen[(x,y)]
                    row.append(" #*=O"[c])
                print("".join(row))
        
        if curblocks != blocks:
            blocks = curblocks
            #if not showdisplay:
            #    print(f"Round: {rounds:5}   blocks: {curblocks:4}  score: {score:5}")
            
            if curblocks == 0:
                return score
            
        if vm.state == IntCodeVM.STATE_HALT:
            print("HALTED")
            return score

        rounds += 1
        #if rounds > 10:
        #    break

        dx = ballpos[0]-paddlepos[0]
        if dx<0:
            joystick = -1
        elif dx > 0:
            joystick = 1
        else:
            joystick = 0

        vm.input_buffer.put_nowait(joystick)


if __name__ == "__main__":
    program = [int(x) for x in sys.stdin.readline().strip().split(",")]
    print("Part 1:")
    print(part1(program))

    print("Part 2:")
    print(part2(program))

