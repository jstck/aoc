#!/usr/bin/env python3

import sys
import argparse
import re
import functools
import itertools
import collections
from queue import PriorityQueue
import heapq
from dataclasses import dataclass
import math

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
def vprint(*args) -> None:
    if args[0]<= verbosity:
        print(*args[1:])

test_cases = [
    {
        "input": ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>",
        "output": 3068,
        "output2": 1514285714288
    }
]

class ShapeFactory():
    _rawshapes = [
    "####",

    """
    .#.
    ###
    .#.
    """,

    """
    ..#
    ..#
    ###
    """,

    """
    #
    #
    # 
    #
    """,


    """
    ##
    ##
    """
    ]

    def __init__(self, count=0):
        self._shapes = []
        for rs in self._rawshapes:
            shape = []
            for rawrow in rs.strip().split("\n"):
                row = [".", "."] + list(rawrow.strip().replace("#","@"))
                l = len(row)
                if l < 7:
                    pad = ["."] * (7-l)
                row.extend(pad)
                shape.append(row)
            shape.reverse()
            self._shapes.append(shape)
        self.size = len(self._shapes)
        self.count = count

    def getPos(self):
        return self.count % self.size

    def getShape(self):
        s = self._shapes[self.getPos()]
        self.count += 1

        #Make a copy
        return [list(row) for row in s]

    def atStart(self) -> bool:
        return self.count % self.size == 0

class MoveFactory:
    def __init__(self, input, count=0):
        self._moves = list(input.strip())
        self.size = len(self._moves)
        self.count = count

    def getPos(self) -> int:
        return self.count % self.size

    def getMove(self) -> str:
        p = self.getPos()
        self.count += 1
        return self._moves[p]

    def atStart(self) -> bool:
        return self.count % self.size == 0


def printTower(tower):
    for i in range(len(tower)-1, -1, -1):
        row = tower[i]
        print("|" + "".join(row) + "|")
    print("+-------+") 

@dataclass(frozen=True)
class State:
    shape: int
    move: int


def rockhits(shape, height, tower, dx=0):
    
    for i in range(len(shape)):
    
        #Check if we're above the tower
        if height+i>=len(tower):
            return False

        rs = shape[i]
        if dx==-1:
            rs = rs[1:] + ["."]
        elif dx==1:
            rs = ["."] + rs[:-1]

        rt = tower[height+i]

        for i in range(len(rs)):
            if rs[i] != "." and rt[i] != ".":
                return True

    return False
        


def bumpleft(shape):
    for r in shape:
        if r[0] != ".":
            return

    for i, r in enumerate(shape):
        shape[i] = r[1:] + ["."]

def bumpright(shape):
    for r in shape:
        if r[-1] != ".":
            return

    for i, r in enumerate(shape):
        shape[i] = ["."] + r[:-1]

def gluerock(tower, shape, height):
    for (i, line) in enumerate(shape):
        h = height+i
        if h > len(tower)-1:
            newline = list("".join(line).replace("@","#"))
            tower.append(newline)
        else:
            #Merge lines
            tl = tower[h]
            newline = []
            for i in range(len(tl)):
                if tl[i] != "." or line[i] != ".":
                    newline.append("#")
                else:
                    newline.append(".")
            tower[h] = newline

def tetris(input, count, tower=[], startstate = State(0, 0), findcycle=False):
    shapes = ShapeFactory(count=startstate.shape)
    moves = MoveFactory(input, count=startstate.move)

    cycle_states: list[State] = []

    while shapes.count < count+startstate.shape:

        if findcycle and shapes.atStart():
            now = State(shapes.count, moves.getPos())
            matching_states = [x for x in cycle_states if x.move==now.move]
            if len(matching_states)>0:
                #A cycle found
                return (tower, matching_states[-1], now)
            #No cycle yet
            cycle_states.append(now)

        shape = shapes.getShape()

        #print("===== NEW SHAPE =====")
        #printTower(shape)
        #print()

        height = len(tower)+3 #Starting height

        #print("H: ", height)
        #printTower(shape)

        while True:
            move = moves.getMove()
                
            #Move left/right
            if move == "<":
                if not rockhits(shape, height, tower, -1):
                    bumpleft(shape)
            elif move == ">":
                if not rockhits(shape, height, tower, 1):
                    bumpright(shape)

            #Move down
            if height>0 and not rockhits(shape, height-1, tower, 0):
                height-=1
                #print("H: ", height)
                #printTower(shape)
            else:
                #Rock lands
                #print("Glue shape at h=", height)
                #printTower(shape)
                #print()
                
                gluerock(tower, shape, height)

                #print(f"=== After {shapes.count} rocks / {moves.count} moves, rock lands at {height} ===")
                #printTower(tower)

                break
    return tower

def part1(input: str):
    return len(tetris(input, 2022))

            


    

def part2(input: str):
    totalmoves = 1_000_000_000_000
    (tower, cycle_start, cycle_end) = tetris(input, totalmoves, findcycle=True)

    print(f"Cycle found from {cycle_start.shape} to {cycle_end.shape} with move={cycle_start.move}")

    cycle_length = cycle_end.shape - cycle_start.shape

    start_length = cycle_start.shape

    n_cycles = (totalmoves - start_length) // cycle_length
    final_steps = (totalmoves - start_length) % cycle_length

    print(f"Start is {start_length} steps, {n_cycles} cycles of {cycle_length} moves + {final_steps}")

    assert start_length + n_cycles*cycle_length + final_steps == totalmoves

    #Run one cycle on top of tower to figure out how much it adds
    start_height = len(tower)
    tower = tetris(input, cycle_length, tower, startstate=cycle_end)

    cycle_height = len(tower)-start_height

    print(f"Cycle builds {cycle_height}")
    print(f"Start stuff: {len(tower)-2*cycle_height}")

    a = len(tower)

    #Final run of stuff at end
    tower = tetris(input, final_steps, tower, startstate=cycle_end)

    print(f"End stuff: {len(tower)-a}")

    #Toer now consists of the start run, two cycles, and the end segment.

    height = len(tower) + (n_cycles-2)*cycle_height

    print("Tower built with 2 cycles:", len(tower))
    print("Length of more cycles:", (n_cycles-2)*cycle_height)
    
    print("TOTAL HEIGHT:", height)

    FACIT=1594842406882

    if(height != FACIT): print(f"WRONG diff {height-FACIT}")

    return height


def fixInput(raw: str) -> list[str]:
    lines = [x.strip() for x in raw.split("\n")]

    #Remove trailing blank lines
    while len(lines[-1])==0:
        lines.pop()
    return lines

if tests:

    success = True

    for case in test_cases:
        rawinput = case["input"]

        match = re.search(r'^FILE:([\S]+)$', rawinput.strip())
        if match:
            filename = match.group(1)
            print("Loading", filename)
            with open(filename, "r") as fp:
                rawinput = fp.read()

        input = rawinput.strip()
        

        if run1 and "output" in case and case["output"] is not None:
            output = part1(input)
            if output != case["output"]:
                print(f"Test part 1failed for input:\n====\n{case['input'].strip()}\n====\n.\n\nGot:\n{output}\n\nExpected:\n{case['output']}\n")
                success = False

        if run2 and "output2" in case and case["output2"] is not None:
            output = part2(input)
            if output != case["output2"]:
                print(f"""Test part 2 failed:
Got:      {output}
Expected: {case['output2']}
Diff:     {output-case['output2']}
""")
                success = False

    if success:
        print("All tests passed successfully!")

else:
    try:
        fp = open(input_file, "r")
    except FileNotFoundError:
        print("Input file not found, using stdin")
        fp = sys.stdin
    
    input = fp.read().strip()

    if run1:
        print("Running part 1")
        result1 = part1(input)
    if run2:
        print("Running part 2")
        result2 = part2(input)

    print()

    if run1:
        print("PART 1")
        print("======")
        print(result1)

    if run1 and run2:
        print()

    if run2:
        print("PART 2")
        print("======")
        print(result2)