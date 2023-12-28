#!/usr/bin/env python3

from IntCodeVM import IntCodeVM

import sys


argcount = {
    IntCodeVM.OP_ADD  :  3,
    IntCodeVM.OP_MULT :  3,
    IntCodeVM.OP_IN   :  1,
    IntCodeVM.OP_OUT  :  1,
    IntCodeVM.OP_BNE  :  2,
    IntCodeVM.OP_BEQ  :  2,
    IntCodeVM.OP_LT   :  3,
    IntCodeVM.OP_EQ   :  3,
    IntCodeVM.OP_BASE :  1,
    IntCodeVM.OP_HALT :  0,
}

def parse_op(opcode):
        op = opcode%100
        mode1 = (opcode // 100) % 10
        mode2 = (opcode // 1000) % 10
        mode3 = (opcode // 10000) % 10
        return (op, mode1, mode2, mode3)

def disasm_instr(program: list[int], pc: int):
    pass    

def disasm(program: list[int]):
    pc = 0
     
    while pc<len(program):
        addr = pc
        opcode = program[pc]
        pc += 1

        (op, mode1, mode2, mode3) = parse_op(opcode)

        if not op in IntCodeVM.opcodes:
            print(f"{addr:3}: {opcode:5} [UNKNOWN]")
        else:
            n_args = argcount[op]
            args = program[:n_args]
            pc += n_args
            pargs = []
            for (arg, mode) in zip(args,[mode1,mode2,mode3]):
                if mode==0:
                    #position mode
                    p = f"@{arg}"
                elif mode==1:
                    #parameter mode (immediate)
                    p = f"={arg}"
                elif mode==2:
                    #relative mode
                    p = f"%{arg}"
                else:
                    #Unknown mode
                    p = f"{mode}?{arg}"
                pargs.append(p)
            print(f"{addr:3}: {IntCodeVM.opcodes[op]:4} {', '.join(pargs)}")

if __name__ == "__main__":
    programs = [list(map(int,line.strip().split(","))) for line in sys.stdin.readlines()]

    for program in programs:
        disasm(program)
        print()
        