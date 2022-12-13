#!/usr/bin/env python3

import sys
import re

mask = None

memory = {}


def make_addresses(mask):
    #No X:es left
    if not "X" in mask:
        yield mask
        return

    xpos = mask.index("X")

    head = mask[:xpos]
    tail = mask[xpos+1:]

    alltails = make_addresses(tail)
    for tail in alltails:
        yield head + ["0"] + tail
        yield head + ["1"] + tail

for line in sys.stdin.readlines():
    line = line.strip()
    if len(line)==0:
        continue

    parts = line.split(" ")
    if parts[0] == "mask":
        mask = list(parts[2])
        assert(len(mask)==36)

    elif parts[0][:3] == "mem":
        matches = re.match(r"^mem\[([0-9]+)\] = ([0-9]+)$", line)
        addr = int(matches.group(1))
        val = int(matches.group(2))

        #print(f"Mem {addr} = {val} {''.join(mask)}")

        addr_b = list(f"{addr:036b}")

        #print(f"{addr:036b}")

        for i in range(36):
            if mask[i]=="0":
                pass
            elif mask[i]=="1":
                addr_b[i]="1"
            else:
                addr_b[i]=mask[i] #X
                assert(mask[i]=='X')

        #print("".join(mask))
        #print("".join(addr_b))

        for xaddr in make_addresses(addr_b):
            addr_i = int("".join(xaddr),2)
            #print(f"Write {val} to {addr_i} {''.join(xaddr)}")
            memory[addr_i] = val


result = sum(memory.values())
print(result)