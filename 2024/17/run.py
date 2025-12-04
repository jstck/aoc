#!/usr/bin/env python3

import functools
from functools import cache
from itertools import combinations
import itertools
import collections
from queue import PriorityQueue
import heapq
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Union, Optional

import math
import re
import sys


sys.path.append("../..")
from lib.aoc import *

def combo(literal: int, registers: tuple[int,int,int]) -> int:
    assert(literal >=0 and literal < 7)

    if literal == 4: return registers[0]
    if literal == 5: return registers[1]
    if literal == 6: return registers[2]

    return literal

def part1(registers: tuple[int,int,int], program: list[int]) -> list[int]:
    assert(len(program)%2==0)

    pc=0
    a,b,c = registers

    output: list[int] = []

    while True:
        #print(f"pc={pc} a={a} b={b} c={c}",)
        if pc >= len(program):
            break
        instr, op_l = program[pc], program[pc+1]

        #print(f"Instruction={instr} op_l={op_l}")
        
        #operand = "literal operand"
        #opval = "combo operator"

        if instr == 0: #adv
            a = a // 2**combo(op_l, (a,b,c))
        elif instr == 1: #bxl
            b = b ^ op_l
        elif instr == 2: #bst
            b = combo(op_l, (a,b,c)) % 8
        elif instr == 3: #jnz
            if a!=0:
                pc = op_l
                continue #Do not pass go
        elif instr == 4: #bxc
            #Operand not used
            b = b ^ c
        elif instr == 5: #out
            output.append(combo(op_l, (a,b,c))%8)
        elif instr == 6: #bdv
            b = a // 2**combo(op_l, (a,b,c))
        elif instr == 7: #cdv
            c = a // 2**combo(op_l, (a,b,c))
        else:
            assert(False)

        pc += 2
        
        
    return output

def part2(registers, program):

    _, b, c = registers

    a=6000000

    while True:
        output = part1((a, b, c), program)

        if output == program:
            break

        if a%10000==0:
            print("A", a, output)

        a += 1

    return a


if __name__ == "__main__":
    input = readinput()

    for line in input:
        line = line.strip()
        if len(line) == 0: continue
        k, v = line.split(":",1)

        if k == "Register A":
            a = int(v.strip())
        elif k == "Register B":
            b = int(v.strip())
        elif k == "Register C":
            c = int(v.strip())
        elif k == "Program":
            program = list(map(int,v.strip().split(",")))

    registers = (a,b,c)

    print(a,b,c)
    print(program)
        

    p1 = part1(registers, program)
    print("Part 1:", ",".join([str(x) for x in p1]))

    p2 = part2(registers, program)
    print("Part 2:", p2)
