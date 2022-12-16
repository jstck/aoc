#!/usr/bin/env python3

import sys
import argparse
import re
import functools
import itertools
import collections
from queue import PriorityQueue
import heapq
from dataclasses import dataclass
import math

match = re.search(r'aoc/?(\d+)/(\d+)', __file__)
if match:
    descr = "Advent of Code " + match.group(1) + ":" + match.group(2)
else:
    descr = "Advent of some kind of Code"

parser = argparse.ArgumentParser(description = descr)

parser.add_argument('-1', action='store_true', help="Do part 1")
parser.add_argument('-2', action='store_true', help="Do part 2")
parser.add_argument('-t', action='store_true', help="Run tests")
parser.add_argument('-f', '--input-file', default='input.txt')
parser.add_argument('--verbose', '-v', action='count', default=0, help="Increase verbosity")

args = parser.parse_args()

tests = vars(args)["t"]
run2 = vars(args)["2"]
run1 = vars(args)["1"] or not run2 #Do part 1 if nothing else specified
verbosity = vars(args)["verbose"]
input_file = vars(args)["input_file"]

@dataclass(frozen=True)
class Valve:
    id: str
    flowrate: int
    tunnels: list[str]

@dataclass(frozen=True, eq=True)
class Position:
    location: str
    openvalves: frozenset[str]

    def __repr__(self):
        return "Position(" + self.location + ":" + ",".join(sorted(self.openvalves)) + ")"

    def __lt__(self, other):
        if self.location == other.location:
            return self.__repr__() < other.__repr__()
        return self.location < other.location
        

@dataclass(frozen=True, eq=True, order=True)
class State:
    time: int
    totalflow: int
    pos: Position


#Print controlled by verbosity level
def vprint(*args) -> None:
    if args[0]<= verbosity:
        print(*args[1:])

test_cases = [
    {
        "input": "FILE:sample.txt",
        "output": 1651,
        "output2": 1707
    },
    {
        "input": "FILE:input.txt",
        "output": 1559,
        "output2": None
    }
]

def parse(input: list[str]) -> dict[str,Valve]:
    valves = {}
    rexp = re.compile(r"^Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z ,]+)$")
    for line in input:
        matches = rexp.match(line)
        id = matches.group(1)
        flow = int(matches.group(2))
        tunnels = [x.strip() for x in matches.group(3).split(",")]
        v = Valve(id, flow, tunnels)
        valves[id] = v
    return valves

def sumflow(valves: dict[str,Valve]) -> int:
    return sum([valves[v].flowrate for v in valves])

def makemoves(valves: list[Valve], state: State, visited: set[Position], maxvalves, maxtime):
    t = state.time

    #Time's up, no more moves (any move at t=30 is pointless)
    if t >= maxtime:
        return []

    #If all valves are open, nothing left do to but dance.
    if len(state.pos.openvalves) >= maxvalves:
        return []

    pos: Position = state.pos
    here = pos.location
    valve: Valve = valves[here]

    #Open this valve
    if valve.flowrate > 0 and here not in pos.openvalves:
        moreflow = (maxtime-t-1)*valve.flowrate
        newflow = moreflow + state.totalflow
        newpos = Position(here, pos.openvalves.union({here}))
        if newpos not in visited or visited[newpos] < newflow:
            newstate = State(t+1, newflow, newpos)
            yield newstate

    #Go somewhere else
    for exit in valves[here].tunnels:
        newpos = Position(exit, pos.openvalves)
        if not newpos in visited or visited[newpos] < state.totalflow:
            yield State(t+1, state.totalflow, newpos)


def solve(valves, maxtime):
    
    #Theoretical maximum flow ever, to priority-enqueue on "lower = better" (most flow so far)
    maxrate = sumflow(valves)
    maxflow = maxrate * (maxtime-1)

    #All "useful valves" (flow rate > 0)
    allvalves = [v for v in valves if valves[v].flowrate>0]
    maxvalves = len(allvalves)

    visited: dict[Position, int] = {}

    bestflow = 0

    start = Position("AA", frozenset())

    startstate = State(0, 0, start)

    pq = PriorityQueue()

    pq.put((max, startstate))
    
    while not pq.empty():
        state: State
        (_, state) = pq.get()

        #Been here already
        if state.pos in visited:
            if visited[state.pos] >= state.totalflow:
                continue

        #print("Visiting: ", state)

        if state.totalflow > bestflow:
            bestflow = state.totalflow

        visited[state.pos] = state.totalflow

        #Theoretical best flow reached from this state
        bestpossible = state.totalflow + maxrate*(maxtime-state.time)
        if bestpossible < bestflow:
            continue

        for newstate in makemoves(valves, state, visited, maxvalves, maxtime):
            #Theoretical max flow (every remaining valve opens instantly)
            tmax = newstate.totalflow + (maxtime-newstate.time)*maxrate
            #qval = newstate.time
            qval = maxflow - tmax
            pq.put((qval, newstate))

    return bestflow



def part1(input: list[str]):
    valves = parse(input)
    return solve(valves, 30)
    

def allsubsets(iterable):
    from itertools import chain, combinations
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1,len(s)))

def part2(input: list[str]):
    import time

    valves = parse(input)
    allvalves = set([v for v in valves if valves[v].flowrate>0])

    combos = 2**(len(allvalves)-1)-2

    #Always keep one of the valves for myself, to only have to do half as many iterations
    alwaysmine = allvalves.pop()

    bestflow = 0
    count = 0
    t00 = t0 = time.time()
    
    for myset in allsubsets(allvalves):
        count += 1
        myset = set(myset)
        myset.add(alwaysmine)
        elephantset = allvalves.difference(myset)
    
        myvalves = {}
        elephantvalves = {}
        for v in valves:
            v0 = valves[v]

            if v in myset:
                myvalves[v] = Valve(id=v0.id, flowrate=v0.flowrate, tunnels=v0.tunnels)
            else:
                myvalves[v] = Valve(id=v0.id, flowrate=0, tunnels=v0.tunnels)

            if v in elephantset:
                elephantvalves[v] = Valve(id=v0.id, flowrate=v0.flowrate, tunnels=v0.tunnels)
            else:
                elephantvalves[v] = Valve(id=v0.id, flowrate=0, tunnels=v0.tunnels)


        myflow = solve(myvalves, 26)
        elephantflow = solve(elephantvalves, 26)

        totalflow = myflow + elephantflow

        if count%10==0:
            delta = time.time()-t0
            print(f"{count:5} / {combos}, {count/delta:1.4f}/s")

        if totalflow > bestflow:
            bestflow = totalflow
            print("NEW BEST:", bestflow, myflow, elephantflow, myset, elephantset, count)

    print("Best:", bestflow)
    totaltime = time.time() - t00
    print(f"{count} in {totaltime:.3f}")

    return bestflow






def fixInput(raw: str) -> list[str]:
    lines = [x.strip() for x in raw.split("\n")]

    #Remove trailing blank lines
    while len(lines[-1])==0:
        lines.pop()
    return lines

if tests:

    success = True

    for case in test_cases:
        rawinput = case["input"]

        match = re.search(r'^FILE:([\S]+)$', rawinput.strip())
        if match:
            filename = match.group(1)
            print("Loading", filename)
            with open(filename, "r") as fp:
                rawinput = fp.read()

        input = fixInput(rawinput)
        

        if run1 and "output" in case and case["output"] is not None:
            output = part1(input)
            if output != case["output"]:
                print(f"Test part 1 failed for input:\n====\n{case['input'].strip()}\n====\n.\n\nGot:\n{output}\n\nExpected:\n{case['output']}\n")
                success = False
            else:
                print(f"Test part 1 succeeded for input: {case['input']}")

        if run2 and "output2" in case and case["output2"] is not None:
            output = part2(input)
            if output != case["output2"]:
                print(f"Test part 2 failed for input:\n====\n{case['input'].strip()}\n====\nGot:\n{output}\n\nExpected:\n{case['output2']}\n")
                success = False

    if success:
        print("All tests passed successfully!")

else:
    try:
        fp = open(input_file, "r")
    except FileNotFoundError:
        print("Input file not found, using stdin")
        fp = sys.stdin
    
    input = fixInput(fp.read())

    if run1:
        print("Running part 1")
        result1 = part1(input)
    if run2:
        print("Running part 2")
        result2 = part2(input)

    print()

    if run1:
        print("PART 1")
        print("======")
        print(result1)

    if run1 and run2:
        print()

    if run2:
        print("PART 2")
        print("======")
        print(result2)