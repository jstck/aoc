#!/usr/bin/env python3
from __future__ import annotations

import functools
from functools import cache
from itertools import combinations
import itertools
import collections
from collections import defaultdict
from queue import PriorityQueue
import heapq
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

import math
import re
import sys

GATE_BROADCASTER = 0
GATE_FLIPFLOP = 1
GATE_CONJUNCTION = 2


class Gate:
    def __init__(self, id: str, type: int, outputs: list[str]):
        self.id: str = id
        self.type: int = type
        self.outputs: list[str] = outputs
        self.inputs: list[str] = []

        self.state: int = 0
        self.memory: dict[str,int] = {}

    def add_input(self, id: str):
        self.inputs.append(id)

    #Generate list of gates to send a pulse to
    def pulse(self, signal: int, src: str, circuit: dict[str,Gate]) -> tuple[int,list[str]]:
        if self.type == GATE_BROADCASTER:
            
            #Send a low pulse to all destinations
            return (0, self.outputs)
            
        elif self.type == GATE_FLIPFLOP:
            if signal == 0:
                #Flip state
                self.state = int(not self.state)
                
                #Send output pulse with new state
                return (self.state, self.outputs)
            
            else:
                #High input signals are ignored
                return (-1, [])
                
        elif self.type == GATE_CONJUNCTION:
            self.memory[src] = signal

            if sum(self.memory.values()) == len(self.inputs):
                out = 0
            else:
                out = 1

            return (out, self.outputs)

    def reset(self):
        self.state = 0
        self.memory.clear()




sys.path.append("../..")
from lib.aoc import *


def runcircuit(circuit: dict[str,Gate], start: str, count: int, monitor: str = "") -> int:

    #Button pulses
    low_pulses = 0
    high_pulses = 0


    monitorcount = {}

    for i in range(count):
        round = i+1
        if count <= 10: print(f"== ROUND {round} ==")  #Debug print if only a few rounds
        q = PriorityQueue()
        tickseq = defaultdict(lambda: 0)


        if round % 100000 == 0:
            print(f"== ROUND {round} ==")

        #Enqueue things with [tick seq signal, source, destination] so everything gets processed in correct order
        q.put( (0, 0, 0, "button", start) )

        while not q.empty():
            tick, _, signal, source, destination = q.get()

            if destination == monitor and signal == 1:
                monitorcount[source] = round
                print(f"High signal {source} -> {destination} on round {round}")
                
                #Count on being so lucky that all signals loop every N cycles starting from 0
                if len(set(circuit[destination].inputs) - set(monitorcount.keys()))==0:
                    return math.lcm(*monitorcount.values())

            if signal == 0:
                low_pulses += 1
                zig = "low"
            elif signal == 1:
                high_pulses += 1
                zig = "high"
            else:
                assert False, f"Invalid signal: {signal}"

            if count <= 10: print(f"{source} -{zig}-> {destination}")

            #Skip debug/output nodes, having counted the pulse
            if not destination in circuit:
                continue

            gate = circuit[destination]

            #Propagate pulse and enqueue results one tick later
            newsignal, destinations = gate.pulse(signal, source, circuit)
            newtick = tick+1
            
            for dest in destinations:
                seq = tickseq[tick]
                tickseq[tick]+=1

                q.put( (newtick, seq, newsignal, destination, dest))

        if count <= 10: print()

    print("Total low", low_pulses)
    print("Total high", high_pulses)

    return low_pulses * high_pulses


if __name__ == "__main__":
    input = readinput()

    circuit: dict[str,Gate] = {}
    butan = ""

    for row in input:
        id, targets = row.split(" -> ")
        targets = targets.split(", ")

        if id[0] == "%":
            type = GATE_FLIPFLOP
            id = id[1:]
        elif row[0] == "&":
            type = GATE_CONJUNCTION
            id = id[1:]
        else:
            assert butan=="", f"Duplicate broadcasters {butan}, {id}!!"
            type = GATE_BROADCASTER
            butan = id

        gate = Gate(id, type, targets)
        circuit[id] = gate


    #Go through each gates outputs, and tag them with the input (needed for conjunction gates, but everyone gets it)
    for gate in circuit.values():
        for dest in gate.outputs:
            if dest in circuit:
                circuit[dest].add_input(gate.id)


    

    p1 = runcircuit(circuit, butan, 1000)
    print("Part 1:", p1)

    for gate in circuit.values():
        gate.reset()

    #Find the conjunction gate to monitor (has rx in outputs)
    monitor = ""
    for gate in circuit.values():
        if "rx" in gate.outputs:
            monitor = gate.id
            print(f"Monitoring gate {gate.id}, with inputs {', '.join(gate.inputs)}")
            
    if monitor == "":
        print("No monitor gate found for part 2")
    else:
        p2 = runcircuit(circuit, butan, 100_000_000, "zh")
        print("Part 2:", p2)