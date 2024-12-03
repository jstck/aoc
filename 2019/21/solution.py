#!/usr/bin/env python3

import sys
import math

from IntCodeVM import IntCodeVM

def dump_output(vm) -> int:
    while vm.has_output():
        c = vm.get_output()
        if c<256:
            print(chr(c), end="")
        else:
            return c
    return -1

def springbot(os: list[int], springscript: str) -> int:
    vm = IntCodeVM(os)

    springscript = springscript.strip() + "\n"

    vm.run()
    dump_output(vm)

    assert vm.state == vm.STATE_HALT_INPUT

    for char in springscript:
        vm.add_input(ord(char))

    vm.run()
    return dump_output(vm)

    
if __name__ == "__main__":
    springbot_os = [int(x) for x in sys.stdin.readline().strip().split(",")]

    springscript_p1 = """
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
"""

    print("Part 1")
    p1 = springbot(springbot_os, springscript_p1)

    springscript_p2 = """
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
RUN
"""

    print("Part 2")
    p2 = springbot(springbot_os, springscript_p2)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")