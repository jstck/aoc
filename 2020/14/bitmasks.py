#!/usr/bin/env python3

import sys
import re

def read_input():

    mask = None
    instructions = []

    for line in sys.stdin.readlines():
        line = line.strip()
        if len(line)==0:
            continue

        parts = line.split(" ")
        if parts[0] == "mask":
            if mask is not None and len(instructions) > 0:
                yield (mask, instructions)
                mask = None
                instructions = []

            mask = parts[2]

        if parts[0][:3] == "mem":
            matches = re.match(r"^mem\[([0-9]+)\] = ([0-9]+)$", line)
            addr = int(matches.group(1))
            val = int(matches.group(2))
            instructions.append((addr, val))

    if mask is not None and len(instructions) > 0:
                yield (mask, instructions)

def apply_mask(value, mask):
    assert(len(mask)==36)

    mem_b = ['W'] * 36 #list(f"{mem:036b}")
    val_b = list(f"{value:036b}")
    mask_a = list(mask)

    for i in range(36):
        if mask_a[i]=="X":
            mem_b[i] = val_b[i]
        else:
            mem_b[i] = mask[i]
    output = int("".join(mem_b), 2)

    #print(f"val    {''.join(val_b)} ({value}))")
    #print(f"mask   {mask}")
    #print(f"result {output:036b} ({output})")

    return output


memory = {}

for (mask, inst) in read_input():
    #print("Mask:", mask)
    for (addr, val) in inst:
        #print("Mem:", addr, val)
        result = apply_mask(val, mask)
        #print(f"Val:{val} Addr:{addr} -> {result}")
        memory[addr] = result

result = sum(memory.values())
print(result)