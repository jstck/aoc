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
parser.add_argument('--verbose', '-v', action='count', default=0, help="Increase verbosity")

args = parser.parse_args()

part2 = vars(args)["2"]
part1 = vars(args)["1"] or not part2 #Do part 1 if not part 2 specified
verbosity = vars(args)["verbose"]

#Print controlled by verbosity level
def vprint(*args):
    if args[0]<= verbosity:
        print(*args[1:])

#for line in sys.stdin.readlines():
#    pass

program = []
fullprogram = []
chunk = []
for l in sys.stdin.readlines():
    l = l.strip()
    if l[:3] == 'inp':
        if len(chunk)>0:
            program.append(chunk)
            chunk = []

    statement = l.split()
    if len(statement)>2:
        if statement[2] not in ['w','x','y','z']:
            statement[2] = int(statement[2])

    chunk.append(statement)
    fullprogram.append(statement)

if len(chunk)>0:
    program.append(chunk)



model_number = [9,2,3,4,5,6,7,8,9,1,2,3,4,5]


def all_modelnumbers():
    s = [9] * 14

def run(segment, input, variables = None):
    if variables is None:
        vars = {
            'w': 0,
            'x': 0,
            'y': 0,
            'z': 0
        }
    else:
        vars = variables.copy()

    for statement in program[segment]:
        instr = statement[0]
        a = statement[1]
        
        if instr == 'inp':
            vars[a] = input
        else:
            b = statement[2]
            if isinstance(b, str):
                b = vars[b]

            if instr == 'add':
                vars[a] += b
            elif instr == 'mul':
                vars[a] *= b
            elif instr == 'div':
                va = vars[a]
                vars[a] = -(-va // b) if va < 0 else va // b
            elif instr == 'mod':
                vars[a] %= b
            elif instr == 'eql':
                if vars[a] == b:
                    vars[a] = 1
                else:
                    vars[a] = 0
            else:
                print("INVALID INSTRUCTION", statement)
    return vars

v = run(0, 9)
vs = ", ".join(["%c:%s"%(k,v) for (k,v) in v.items()])
print(vs)

for i0 in range(9,0,-1):
    state0 = run(0,i0,None)

    for i1 in range(9,0,-1):
        state1 = run(1,i1,state0)

        for i2 in range(9,0,-1):
            state2 = run(2,i2,state1)

            for i3 in range(9,0,-1):
                state3 = run(3,i3,state2)

                for i4 in range(9,0,-1):
                    state4 = run(4,i4,state3)

                    for i5 in range(9,0,-1):
                        state5 = run(5,i5,state4)

                        for i6 in range(9,0,-1):
                            state6 = run(6,i6,state5)

                            for i7 in range(9,0,-1):
                                state7 = run(7,i7,state6)

                                for i8 in range(9,0,-1):
                                    print("".join(str(i) for i in [i0, i1, i2, i3, i4, i5, i6, i7, i8]))

                                    state8 = run(8,i8,state7)

                                    for i9 in range(9,0,-1):
                                        state9 = run(9,i9,state8)

                                        for i10 in range(9,0,-1):
                                            state10 = run(10,i10,state9)

                                            for i11 in range(9,0,-1):
                                                state11 = run(11,i11,state10)

                                                for i12 in range(9,0,-1):
                                                    state12 = run(12,i12,state11)

                                                    for i13 in range(9,0,-1):
                                                        state13 = run(13,i13,state12)

                                                        if state13['z'] == 0:
                                                            print("FINISH!!")
                                                            print("".join(str(i) for i in [i0, i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13]))
                                                            sys.exit(0)
    print(i)