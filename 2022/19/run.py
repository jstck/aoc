#!/usr/bin/env python3

import sys
import argparse
import re
import functools
from collections import deque
from dataclasses import dataclass
from enum import Enum
from pprint import PrettyPrinter
from typing import Iterator, Union

if __name__ == "__main__":

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


pp = PrettyPrinter(indent=2)


#Print controlled by verbosity level
def vprint(*args) -> None:
    if args[0]<= verbosity:
        print(*args[1:])



test_cases = [
    {
        "input": "FILE:sample.txt",
        "output": 33,
        "output2": 56*62
    }
]

class Material(Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.name}"

@dataclass(frozen=True, order=True)
#Geodes are not kept in resource/bot inventory, but stored separately
class Inventory:
    ore: int
    clay: int
    obsidian: int

    def __add__(self, other):
        return Inventory(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian)

    def __sub__(self, other):
        return Inventory(
            self.ore - other.ore,
            self.clay - other.clay,
            self.obsidian - other.obsidian)

    def __str__(self):
        return f"Ore:{self.ore} Clay:{self.clay} Obs:{self.obsidian}"

    def key(self):
        return (self.ore, self.clay, self.obsidian)


@dataclass
class Blueprint:
    id: int
    items: dict[Material, Inventory]
    maxcost: Inventory

    @staticmethod
    def nameToMaterial(s: str) -> Material:
        s = s.lower()

        if s == "ore": return Material.ORE
        if s == "clay": return Material.CLAY
        if s == "obsidian": return Material.OBSIDIAN
        if s == "geode": return Material.GEODE

        assert False



@dataclass(frozen=True, order=True)
class State:
    time: int
    geodes: int
    robots: Inventory
    resources: Inventory
    parent: Union['State',None]
    
    def __str__(self):
        return f"""State at t={self.time}, {self.geodes} geodes
Resources: {self.resources}
Bots:      {self.robots}
"""

    #"Key" for equivalence (ignoring heritage)
    def key(self):
        return (self.time, self.geodes, self.robots, self.resources)

    def printHistory(self):
        if self.parent is not None:
            self.parent.printHistory()
            print()
        print(self)

    def maxgeodes(self, timelimit: int) -> int:
        """Theoretical max number of geodes, if one geode bot is created every round after this one

At t=16, limit=23
16 current state
17 0 < bot 1 created now
18 6 < bot 1 mines 6 geodes from here on
19 5
20 4
21 3
22 2 < bot 5 mines 2 geodes, bot 6 created
23 1 < bot 6 mines 1 geode
triangular number for 6 = 21 more geodes
"""
        roundsleft = timelimit - self.time

        return self.geodes + (roundsleft*(roundsleft+1))//2





def makeMoves(current: State, blueprint: Blueprint, timelimit: int=24) -> Iterator[State]:
    #Mine more resources
    newstuff = current.resources + current.robots

    t1 = current.time+1
    geodes = current.geodes

    #We're already out of time, shouldn't have gotten here.
    if t1 > timelimit:
        return []

    def canAfford(r: Material):
        if blueprint.items[r].ore > current.resources.ore: return False
        if blueprint.items[r].clay > current.resources.clay: return False
        if blueprint.items[r].obsidian > current.resources.obsidian: return False
        return True


    timeleft = timelimit-t1
    botsMade = False

    #maxOreUse = timeleft*blueprint.maxcost.ore #The most ore we can ever use from here
    #needMoreOre = current.resources.ore + timeleft*current.robots.ore < maxOreUse
    #needMoreObsidian = current.resources.obsidian + timeleft*current.robots.obsidian < timeleft*blueprint.items[Material.GEODE].obsidian #Enough obsidian to make one geode bot per turn
    #needMoreClay = needMoreObsidian and current.resources.clay + timeleft * current.robots.clay < timeleft*blueprint.items[Material.OBSIDIAN].clay #Enough clay to make one obsidian bot per turn
    
    #needMoreOre = current.robots.ore < blueprint.maxcost.ore
    #needMoreObsidian = current.robots.obsidian < blueprint.items[Material.GEODE].obsidian
    #needMoreClay = current.robots.clay < blueprint.items[Material.OBSIDIAN].clay
        
    yield State(t1, geodes, current.robots, newstuff, current)

    #Make geode bot
    if canAfford(Material.GEODE):
        #Number of geodes made by this robot until the end of time
        geodesmade = timeleft+1
        yield State(t1, geodes + geodesmade, current.robots, newstuff - blueprint.items[Material.GEODE], current)
        botsMade = True

    #Make obsidian bot
    if timeleft>=1 and current.robots.obsidian < blueprint.items[Material.GEODE].obsidian and canAfford(Material.OBSIDIAN):
        yield State(t1, geodes, current.robots + Inventory(0,0,1), newstuff - blueprint.items[Material.OBSIDIAN], current)
        botsMade = True

    #Make clay bot
    if timeleft>=1 and current.robots.clay < blueprint.items[Material.OBSIDIAN].clay and canAfford(Material.CLAY):
        yield State(t1, geodes, current.robots + Inventory(0, 1, 0), newstuff-blueprint.items[Material.CLAY], current)
        botsMade = True

    #Make ore bot
    if timeleft >= 1 and current.robots.ore < blueprint.maxcost.ore and canAfford(Material.ORE):
        yield State(t1, geodes, current.robots + Inventory(1, 0, 0), newstuff-blueprint.items[Material.ORE], current)
        botsMade = True

    #"Do nothing" is only meaningful if no bots are made
    #if not botsMade:
    #    yield State(t1, geodes, current.robots, newstuff, current)






def dfs(blueprint: Blueprint, timelimit: int=24) -> int:

    #print(f"Processing blurprint {blueprint.id}")
    #print(blueprint)
    
    q: deque[State] = deque()

    #Visited states
    visited: set[tuple] = set()

    #Best geode amount at each point in time
    best: dict[int, int] = {i: 0 for i in range(timelimit+1)}
    beststate: dict[int, State] = {}

    startstate = State(1, 0, Inventory(1,0,0), Inventory(0,0,0), None)

    q.append(startstate)

    queued = 1

    processed = 0
    

    while len(q):

        processed += 1

        cur: State = q.pop()

        if cur.time > timelimit:
            #Borken state
            print("BORK STATE")
            continue

        cur_key = cur.key()
        if not cur_key in visited:
            visited.add(cur_key)
        else:
            continue

        geodes = cur.geodes

        #Check if some other path has a better result than we theoretically can reach from here
        if cur.time > 20 and best[timelimit] > cur.maxgeodes(timelimit):
            #print(f"Best is {best[timelimit]}, I can only do {cur.maxgeodes(timelimit)}")
            #print(cur)
            continue

        if geodes > best[cur.time]:
            #Improved best so far
            best[cur.time] = geodes
            beststate[cur.time] = cur
            #print("New best", cur)

        for next in makeMoves(cur, blueprint, timelimit):

            #Don't queue states where better already exists
            if not next.key() in visited:
                q.append(next)
                queued += 1

        #if processed % 10000 == 0:
        #    print(f"{processed} states processed, {queued-processed} in queue", best[timelimit])


    print(f"{processed} states processed")


    #for (t, s) in beststate.items():
    #    print(f"{t:2d} {s}")
    print(f"Blueprint {blueprint.id}: {best[timelimit]}")
    if verbosity >= 1:
        if timelimit in beststate:
            solution = beststate[timelimit]
            solution.printHistory()
        else:
            print("No solution found")
    return best[timelimit]



    

def parse(input: list[str]) -> list[Blueprint]:

    bloops = []

    for line in input:

        (bp, stuff) = line.split(": ", 1)
        
        (_, bpn) = bp.split(" ", 1)
        bpid = int(bpn)

        robots = stuff.split(". ")

        botcosts: dict[Material, Inventory] = {}

        for robot in robots:
            (target, costs) = robot.split(" costs ", 1)
            costs = costs.strip(".")
            target = Blueprint.nameToMaterial(target.split(" ")[1])
            costs = costs.split(" and ")

            itemcosts = {}

            for cost in costs:
                (amount, item) = cost.split(" ")
                amount = int(amount)
                itemcosts[item] = amount

            robotcost = Inventory(
                itemcosts.get("ore",0),
                itemcosts.get("clay",0),
                itemcosts.get("obsidian",0)
            )

            botcosts[target] = robotcost

        #Helper to figure out max cost of any item
        def maxcost(a: Inventory, b: Inventory) -> Inventory:
            return Inventory(
                max(a.ore,b.ore),
                max(a.clay,b.clay),
                max(a.obsidian,b.obsidian))

        

        maxcosts: Inventory = functools.reduce(maxcost, botcosts.values())
        bloop: Blueprint = Blueprint(bpid, botcosts, maxcosts)
        bloops.append(bloop)
    return bloops


def part1(input: list[str]):


    blueprints = parse(input)


    totalscore = 0

    for blueprint in blueprints:
        #print(f"Blueprint {blueprint.id}")
        best = dfs(blueprint, 24)
        #print("Best", best)
        totalscore += blueprint.id * best
   

    return totalscore

def part2(input: list[str]):
    blueprints = parse(input)

    totalscore = 1

    for blueprint in blueprints[0:3]:
        #print(f"Blueprint {blueprint.id}")
        best = dfs(blueprint, 32)
        #print("Best", best)
        totalscore *= best
   

    return totalscore



def fixInput(raw: str) -> list[str]:
    return [x.strip() for x in raw.strip().split("\n")]


if __name__ == "__main__":

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
                    print(f"Test part 1failed for input:\n====\n{case['input'].strip()}\n====\n.\n\nGot:\n{output}\n\nExpected:\n{case['output']}\n")
                    success = False

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