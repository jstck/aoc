#!/usr/bin/env python3

import sys
import argparse
import re
import IntCodeVM
import itertools

match = re.search(r'aoc/?(\d+)/(\d+)', __file__)
if match:
    descr = "Advent of Code " + match.group(1) + ":" + match.group(2)
else:
    descr = "Advent of some kind of Code"

parser = argparse.ArgumentParser(description = descr)

parser.add_argument('-1', action='store_true', help="Do part 1")
parser.add_argument('-2', action='store_true', help="Do part 2")
parser.add_argument('--verbose', '-v', action='count', default=0, help="Increase verbosity")
parser.add_argument('--test', '-t', action='store_true', help="Run test")

args = parser.parse_args()

test = vars(args)["test"]
part2 = vars(args)["2"]
part1 = vars(args)["1"] or not (part2 or test) #Do part 1 if nothing else specified
verbosity = vars(args)["verbose"]

#Print controlled by verbosity level
def vprint(*args):
    if args[0]<= verbosity:
        print(*args[1:])

#for line in sys.stdin.readlines():
#    pass

def simStep(program, phase, input):
    vm = IntCodeVM.vm(program, [phase, input], False)
    vm.run()
    return vm.output_buffer[0]

def simRun(program, phases):
    signal = 0
    for phase in phases:
        signal = simStep(program, phase, signal)
    return signal


if test:
    programs = []
    for p in sys.stdin.readlines():
        programs.append([int(i.strip()) for i in p.split(',')])

    print(programs)
    print(simRun(programs[0], [4, 3, 2, 1, 0]))
    print(simRun(programs[1], [0, 1, 2, 3, 4]))
    print(simRun(programs[2], [1, 0, 4, 3, 2]))
    sys.exit(0)

program = [int(i.strip()) for i in sys.stdin.readline().split(',')]

maxval = 0

if part1:
    for phases in itertools.permutations([0, 1, 2, 3, 4]):
        val = simRun(program, phases)
        if val > maxval:
            maxval = val
            print("New highscore:", val)
            print(phases)
            print()
        
if part2:
    phasesettings = [5, 6, 7, 8, 9]
    maxsignal = 0
    for phases in itertools.permutations(phasesettings):
        signal = 0
        #print(phases)
        vms = [IntCodeVM.vm(program, [phase], True) for phase in phases]
        halted = False
        runs = 0
        while not halted and runs < 2:
            runs += 1
            for i in range(len(vms)):
                vms[i].add_input(signal)
                print(vms[i].input_buffer)
                vms[i].run()
                signal = vms[i].output_buffer.pop()
                halted = halted or (vms[i].state == vms[i].STATE_HALT)
                print("HALTED", i, vms[i].state, signal)
                print()

        print("Phases", str(phases), runs, "runs")

        if signal > maxsignal:
            print("New record signal", signal, "at", str(phases))
            maxsignal = signal
        

            


