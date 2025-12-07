#!/usr/bin/env python3

import sys

sys.path.append("../..")
from lib.aoc import *

if __name__ == "__main__":
    input = readinput()

    beams = [0] * len(input[0])
    splits = 0

    for line in input:
        assert len(line) == len(beams)
        newbeam = [0] * len(beams)

        for i in range(len(beams)):
            beam = beams[i]
            splitter = line[i]

            if splitter == "S":
                newbeam[i] += 1
            elif splitter == "^":
                if beam >= 1:
                    splits += 1
                newbeam[i-1] += beam
                newbeam[i+1] += beam
            elif splitter == ".":
                newbeam[i] += beam
            else:
                print("UNKNOWN INPUT", splitter)
                assert False
        beams = newbeam
        print(line)
        print("".join([str(x) for x in beams]))

    print("Part 1:",splits)
    print("Part 2:", sum(beams))
