#!/usr/bin/env python3

import sys
import argparse
import re
import IntCodeVM

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

program = [int(l.strip()) for l in sys.stdin.readline().split(',')]

if part1:
    vm = IntCodeVM.vm(program, [1], False)
    vm.run()
    print(vm.output_buffer)

if part2:
    vm = IntCodeVM.vm(program, [5], False)
    vm.run()
    print(vm.output_buffer)

