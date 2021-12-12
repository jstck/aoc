#!/usr/bin/env python3

import sys
import re

instructions = []

for line in sys.stdin.readlines():
    (operand, argument) = line.split()
    argument = int(argument)

    if not operand in ["acc", "nop", "jmp"]:
        print("Invalid instruction:", line)

    instructions.append((operand, argument))


pc = 0
acc = 0

visited = set()

while True:

    print(pc+1,acc)

    if pc in visited:
        print("Second time at pc=",pc+1)
        print("Acc:", acc)
        sys.exit(0)

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
