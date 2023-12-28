#!/usr/bin/env python3

import sys

from IntCodeVM import IntCodeVM


turns = {
    "u": ["l","r"],
    "l": ["d","u"],
    "d": ["r","l"],
    "r": ["u","d"]
}

moves = {
    "u": (0,-1),
    "l": (-1,0),
    "d": (0,1),
    "r": (1,0)
}



def paint(program: list[int], starttile: int) -> dict[tuple[int,int],int]:

    tiles: dict[tuple[int,int],int] = {}
    x,y=0,0
    direction = "u"

    vm = IntCodeVM(program, [starttile], False)

    while True:
        vm.run()  #Will halt on input, usually
        
        color = vm.output_buffer.get_nowait()
        turn = vm.output_buffer.get_nowait()

        assert color in [0,1]
        assert turn in [0,1]

        #Paint
        tiles[(x,y)] = color

        #Move
        direction = turns[direction][turn]
        dx,dy = moves[direction]
        x+=dx
        y+=dy

        if vm.state == IntCodeVM.STATE_HALT:
            break

        assert vm.state == IntCodeVM.STATE_HALT_INPUT

        #Input color
        vm.input_buffer.put_nowait(tiles.get((x,y), 0))

    return tiles

def part1(program: list[int]):
    tiles = paint(program, 0)
    return len(tiles)

def part2(program: list[int]):
    tiles = paint(program, 1)
    xmin,xmax,ymin,ymax=0,0,0,0

    for (x,y) in tiles.keys():
        xmin = min(xmin,x)
        xmax = max(xmax,x)
        ymin = min(ymin,y)
        ymax = max(ymax,y)

    for y in range(ymin,ymax+1):
        row = []
        for x in range(xmin,xmax+1):
            c = tiles.get((x,y), 0)
            s = " #"[c]
            row.append(s)
        print("".join(row))





if __name__ == "__main__":
    program = [int(x) for x in sys.stdin.readline().strip().split(",")]
    print("Part 1:")
    print(part1(program))

    print("Part 2:")
    part2(program)
