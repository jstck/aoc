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

def symbol(c):
    if c=='w': return 0
    if c=='x': return 1
    if c=='y': return 2
    if c=='z': return 3
    print("UNKNOWN SYMBOL:",c)
    sys.exit(0)

def run(segment, input, z = None):
    vars = [0,0,0,z]

    for statement in program[segment]:
        instr = statement[0]
        a = symbol(statement[1])
        
        if instr == 'inp':
            if input is not None:
                vars[a] = input
                input = None
            else:
                print("INPUT BUFFER UNDERRUN")
                sys.exit(0)
        else:
            b = statement[2]
            if isinstance(b, str):
                b = vars[symbol(b)]

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

    return vars[3]

m = [int(i) for i in list("13579246899999")]


states = []
print(states)
for i in range(14):
    if i == 0:
        prevstates = {0: []}
    newstates = {}
    print("####### I",i)
    print(len(prevstates), "previous states")
    for (oldz, oldinput) in prevstates.items():

        #The two parts have different orderings (to store "highest path" or "lowest path" to a given z,
        #as well as making assumptions of what the first digit will be to save time

        #part 1:
        #for d in range(9,0,-1):
        #    if i==0 and d!=9:
        #        continue

        #part 2:
        for d in range(1,10):
            if i==0 and d!=2:
                continue
            z = run(i,d,oldz)
            if not z in newstates:
                #print("New state, i=%d d=%d z=%d" % (i,d,z))
                newstates[z] = (oldinput + [d])

    states.append(newstates)
    prevstates = newstates
        
print(states[-1][0])
print("".join(str(x) for x in states[-1][0]))