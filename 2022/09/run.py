#!/usr/bin/env python3

import sys
import argparse
import re

match = re.search(r'aoc/?(\d+)/(\d+)', __file__)
if match:
    descr = "Advent of Code " + match.group(1) + ":" + match.group(2)
else:
    descr = "Advent of some kind of Code"

parser = argparse.ArgumentParser(description = descr)

parser.add_argument('-1', action='store_true', help="Do part 1")
parser.add_argument('-2', action='store_true', help="Do part 2")
parser.add_argument('-t', '--test', action='store_true', help="Run tests")
parser.add_argument('-f', '--input-file', default='input.txt')
parser.add_argument('--verbose', '-v', action='count', default=0, help="Increase verbosity")

args = parser.parse_args()

tests = vars(args)["test"]
run2 = vars(args)["2"]
run1 = vars(args)["1"] or not run2 #Do part 1 if nothing else specified
verbosity = vars(args)["verbose"] or 0
input_file = vars(args)["input_file"]


#Print controlled by verbosity level
def vprint(*args):
    if args[0]<= verbosity:
        print(*args[1:])

def chunks(input, ints=False):
    chunk = []
    chunky = []
    for line in input:
        if len(line) == 0:
            chunky.append(chunk)
            chunk = []
        else:
            if ints:
                chunk.append(int(line))
            else:
                chunk.append(line)

    if len(chunk)>0:
        chunky.append(chunk)
    return chunky



test_cases = [
    {
        "input": """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""",
        "output": 13,
        "output2": 1
    },
    {
        "input": """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""",
        "output": 88,
        "output2": 36
    }
]

moves = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0),
}


def doMove(headX, headY, tailX, tailY, move):
    headX += move[0]
    headY += move[1]

    #visited.add((headX, headY))

    if tailX < headX-1:
        tailX = headX-1
        tailY = headY

    elif tailX > headX+1:
        tailX = headX+1
        tailY = headY
    
    elif tailY < headY-1:
        tailY = headY-1
        tailX = headX

    elif tailY > headY+1:
        tailY = headY+1
        tailX = headX

    #print(headX, headY, tailX, tailY)

    return (headX, headY, tailX, tailY)


def doMove2(rope, move):
    headX = rope[0][0] + move[0]
    headY = rope[0][1] + move[1]

    rope[0] = (headX, headY)

    for i in range(1, len(rope)):
        (headX, headY) = rope[i-1]
        (tailX, tailY) = rope[i]

        dX = headX-tailX
        dY = headY-tailY

        if abs(dX) <= 1 and abs(dY) <= -1:
            pass
        else:

            #Diagonal moves, puts tail diagonally after head
            if tailX < headX-1 and tailY < headY-1:
                tailX = headX-1
                tailY = headY-1
            elif tailX > headX+1 and tailY < headY-1:
                tailX = headX+1
                tailY = headY-1
            elif tailX < headX-1 and tailY > headY+1:
                tailX = headX-1
                tailY = headY+1
            elif tailX > headX+1 and tailY > headY+1:
                tailX = headX+1
                tailY = headY+1

            #Other moves puts tail "straight" behind head
            elif tailX < headX-1:
                tailX = headX-1
                tailY = headY

            elif tailX > headX+1:
                tailX = headX+1
                tailY = headY
            
            elif tailY < headY-1:
                tailY = headY-1
                tailX = headX

            elif tailY > headY+1:
                tailY = headY+1
                tailX = headX

            rope[i] = (tailX, tailY)


def printGrid(visited, rope=[], showTrail = True, showRope = True):
    pX = [p[0] for p in visited] + [p[0] for p in rope]
    pY = [p[1] for p in visited] + [p[1] for p in rope]

    minX = min(pX + [0])
    maxX = max(pX)
    minY = min(pY + [0])
    maxY = max(pY)

    grid = []
    for y in range(minY, maxY+1):
        grid.append(["."] * (maxX-minX+1))

    if showTrail:
        for (x,y) in visited:
            grid[y-minY][x-minX] = "#"

    if showRope:
        for i in range(len(rope)):
            (x, y) = rope[i]
            if grid[y-minY][x-minX] in ["#","."]:
                grid[y-minY][x-minX] = str(i)

    for y in range(len(grid)-1, -1, -1):
        print("".join(grid[y]))
    print()


def moveRope(input, length):
    rope = [[0, 0]] * length
    visited = set()
    visited.add((0, 0))

    for line in input:
        parts = [x.strip() for x in line.split()]
        dir = parts[0]
        dist = int(parts[1])

        for i in range(dist):
            doMove2(rope, moves[dir])

            tail = rope[-1]
            visited.add(tail)
            
        if(verbosity>=2):
            print(line)
            printGrid(visited, rope)
            print()
        

    if(verbosity>=1):
        printGrid(visited)

    return len(visited)

def part1(input):
    a = moveRope(input, 2)
    return a

def part2(input):
    return moveRope(input, 10)

if tests:

    success = True
    print("Verbo", verbosity)

    def splitLines(input):
        return [x.strip() for x in input.split("\n")]

    for case in test_cases:
        input = splitLines(case["input"])
        if run1 and "output" in case and case["output"] is not None:
            output = part1(input)
            if output != case["output"]:
                print(f"Test part 1failed for input:\n====\n{case['input'].strip()}\n====\n.\n\nGot:\n{output}\n\nExpected:\n{case['output']}\n")
                success = False

        if run2 and "output2" in case and case["output2"] is not None:
            output = part2(input)
            if output != case["output2"]:
                print(f"Test part 2 failed for input:\n====\n{case['input'].strip()}\n====\nGot:\n{output}\n\nExpected:\n{case['output2']}\n")
                success = False

    if success:
        print("All tests passed successfully!")

else:
    try:
        fp = open(input_file, "r")
    except FileNotFoundError:
        print("Input file not found, using stdin")
        fp = sys.stdin
    
    input = [x.strip() for x in fp.readlines()]

    if run1:
        print("PART 1")
        print("======")
        print(part1(input))

    if run1 and run2:
        print()

    if run2:
        print("PART 2")
        print("======")
        print(part2(input))