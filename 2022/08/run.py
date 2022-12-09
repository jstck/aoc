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
parser.add_argument('-t', action='store_true', help="Run tests")
parser.add_argument('-f', '--input-file', default='input.txt')
parser.add_argument('--verbose', '-v', action='count', default=0, help="Increase verbosity")

args = parser.parse_args()

tests = vars(args)["t"]
run2 = vars(args)["2"]
run1 = vars(args)["1"] or not run2 #Do part 1 if nothing else specified
verbosity = vars(args)["verbose"]
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
        "input": """30373
25512
65332
33549
35390""",
        "output": 21,
        "output2": 8
    }
]

def parsea(input):
    grid = []
    for line in input:
        gridline = [int(x) for x in line]
        grid.append(gridline)

    return grid

def printgrid(grid):
    for line in grid:
        print("".join([str(x) for x in line]))

def part1(input):
    grid = parsea(input)
    visible = []

    for line in grid:
        visline = [0]*len(line)
        visible.append(visline)

    #From left
    for row in range(0, len(grid)):
        seen = -1
        for col in range(0, len(grid[row])):
            tree = grid[row][col]

            if tree > seen:
                seen = tree
                visible[row][col] = 1

    #From right
    for row in range(0, len(grid)):
        seen = -1
        for col in range(len(grid[row])-1, -1, -1):
            tree = grid[row][col]

            if tree > seen:
                seen = tree
                visible[row][col] = 1

    #From top
    for col in range(0, len(grid[0])):
        seen = -1
        for row in range(0, len(grid)):
            tree = grid[row][col]

            if tree > seen:
                seen = tree
                visible[row][col] = 1


    #From bottom
    for col in range(0, len(grid[0])):
        seen = -1
        for row in range(len(grid)-1, -1, -1):
            tree = grid[row][col]

            if tree > seen:
                seen = tree
                visible[row][col] = 1


    printgrid(grid)
    print()
    printgrid(visible)

    return sum([sum(row) for row in visible])



def scenic_score(grid, x, y):

    
    me = grid[y][x]

    #print("I am", me)

    #To left
    left = 0
    for col in range(x-1, -1, -1):
        tree = grid[y][col]
        left += 1
        if tree >= me:
            #print("Saw a", tree, "at", col, y)
            break

    #print("Left", left)


    #To right
    right = 0
    for col in range(x+1, len(grid[y])):
        tree = grid[y][col]
        right += 1
        if tree >= me: break

    #print("Right", right)

    #To top
    up = 0
    for row in range(y-1, -1, -1):
        tree = grid[row][x]
        up += 1
        if tree >= me: break
        
    #print("Up", up)

    #To bottom
    down = 0
    for row in range(y+1, len(grid)):
        tree = grid[row][x]
        down += 1
        if tree >= me: break

    #print("Down", down)

    return left*right*up*down


def part2(input):

    grid = parsea(input)

    max_score = 0

    for x in range(0, len(grid)):
        for y in range(0, len(grid[x])):
            score = scenic_score(grid, x, y)
            max_score = max(max_score, score)

    return max_score





if tests:

    success = True

    def splitLines(input):
        return [x.strip() for x in input.split("\n")]

    for case in test_cases:
        input = splitLines(case["input"])
        if run1:
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