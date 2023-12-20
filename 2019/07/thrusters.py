#!/usr/bin/env python3

import sys
import argparse
import re
from IntCodeVM import IntCodeVM
import itertools
from typing import Literal

match = re.search(r'aoc/?(\d+)/(\d+)', __file__)
if match:
    descr = "Advent of Code " + match.group(1) + ":" + match.group(2)
else:
    descr = "Advent of some kind of Code"

def simStep(program, phase, input):
    vm = IntCodeVM(program, [phase, input], False)
    vm.run()
    return vm.get_output()

def simRun(program, phases):
    signal = 0
    for phase in phases:
        signal = simStep(program, phase, signal)
    return signal


#Print controlled by verbosity level
def vprint(*args):
    if args[0]<= verbosity:
        print(*args[1:])

def part1(program: list[int]) -> tuple[int, tuple[int]]:

    maxsignal = -1
    bestphases = (0,0,0,0,0)

    for phases in itertools.permutations((0, 1, 2, 3, 4)):
        val = simRun(program, phases)
        if val > maxsignal:
            maxsignal = val
            bestphases = phases
            #print("New highscore:", val)
            #print(phases)
            #print()

    return (maxsignal, bestphases) # type: ignore

def part2(program: list[int]) -> tuple[int, tuple[int]]:
    phasesettings = (5, 6, 7, 8, 9)
    maxsignal = 0
    bestphases = (0, 0, 0, 0, 0)

    for phases in itertools.permutations(phasesettings):
        lastsignal = signal = 0
        #print(phases)
        vms: list[IntCodeVM]= []
        for phase in phases:
            vm = IntCodeVM(program, [phase], False)
            vm.halt_output(True)
            vms.append(vm)

        runs = 0
        halted = False
        while not halted:
            runs += 1
            #if runs % 1000 == 0:
            #  print(f"Run {runs} signal {signal}")
            for i in range(len(vms)):
                vms[i].add_input(signal)
                #print(vms[i].input_buffer)
                vms[i].run()
                #If a VM halted, break here (no output will happen)
                if vms[i].state == IntCodeVM.STATE_HALT:
                    halted = True
                    break

                signal = vms[i].get_output()
            lastsignal = signal #Only record output from last VM as "record signal"
                
        #print("Phases", str(phases), runs, "runs")

        if lastsignal > maxsignal:
            #print(f"New record signal {lastsignal} phases {str(phases)} afer {runs} runs")
            maxsignal = lastsignal
            bestphases = phases

    return (maxsignal, bestphases) # type: ignore


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = descr)

    parser.add_argument('-1', action='store_true', help="Do part 1")
    parser.add_argument('-2', action='store_true', help="Do part 2")
    parser.add_argument('--verbose', '-v', action='count', default=0, help="Increase verbosity")
    #parser.add_argument('--test', '-t', action='store_true', help="Run test")

    args = parser.parse_args()

    p2 = vars(args)["2"]
    p1 = vars(args)["1"] or not p2 #Do part 1 if nothing else specified
    verbosity = vars(args)["verbose"]


    #for line in sys.stdin.readlines():
    #    pass


    programs = []
    for p in sys.stdin.readlines():
        programs.append([int(i.strip()) for i in p.split(',')])


    if p1:
        for program in programs:
            (signal, phases) = part1(program)
            print(f"Max signal: {signal}, phases {str(phases)}")

            
    if p2:
        for program in programs:
            (signal, phases) = part2(program)
            print(f"Max signal: {signal}, phases {str(phases)}")        

            


