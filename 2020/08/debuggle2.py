#!/usr/bin/env python3

import sys
import re

def run_program(instructions):
    pc = 0
    acc = 0

    visited = set()

    while True:

        #print(pc+1,acc)

        if pc >= len(instructions):
            print("Program exited, pc=", pc+1, "acc=", acc)
            return True

        if pc in visited:
            print("Second time at pc=",pc+1)
            print("Acc:", acc)
            return False

        (operand, argument) = instructions[pc]
        visited.add(pc)

        if operand=="acc":
            acc += argument
        elif operand=="nop":
            pass
        elif operand=="jmp":
            pc += argument
            continue #Don't increment PC more
        
        pc += 1


instructions = []

for line in sys.stdin.readlines():
    (operand, argument) = line.split()
    argument = int(argument)

    if not operand in ["acc", "nop", "jmp"]:
        print("Invalid instruction:", line)

    instructions.append((operand, argument))


for i in range(0, len(instructions)):
    (oper, arg) = instructions[i]

    #Don't care about acc instructions
    if oper=="acc":
        continue

    print("Changing instructions at pc", i+1)

    haxxored = instructions.copy()

    if oper=="nop":
        oper="jmp"
    elif oper=="jmp":
        oper="nop"
    else:
        print("SOMETHING BROKEN:", oper, arg, i)
        sys.exit(1)

    haxxored[i] = (oper, arg)

    if(run_program(haxxored)):
        sys.exit(0)