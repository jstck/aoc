#!/usr/bin/env python3
from __future__ import annotations

import functools
from functools import cache
from itertools import combinations
import itertools
import collections
from queue import PriorityQueue
import heapq
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

import math
import re
import sys


sys.path.append("../..")
from lib.aoc import *


class Range:
    def __init__(self, parts: list[tuple[int,int]]):
        self.parts: list[tuple[int,int]] = []
        for p in parts:
            assert p[0] <= p[1]
            self.parts.append(p)

        self.parts.sort()

    def __len__(self) -> int:
        l = 0
        for p in self.parts:
            l += p[1]-p[0] + 1
        return l
    
    def __str__(self) -> str:
        return ", ".join([f"({p[0]}-{p[1]})" for p in self.parts])
    
    def __repr__(self) -> str:
        return self.__str__()

    #Return all sub-ranges < an upper bound
    def reducemax(self, maxval) -> Range:
        newparts = []
        for p in self.parts:
            if p[1]<maxval: #Range untouched
                newparts.append(p)
            elif p[0] >= maxval: #Range completely outside
                continue
            else: #Truncate upper end
                newparts.append((p[0], maxval-1))

        return Range(newparts)
    
    #Return all sub-ranges >= a lower bound
    def reducemin(self, minval) -> Range:
        newparts = []
        for p in self.parts:
            if p[0]>=minval:
                newparts.append(p)
            elif p[1] < minval:
                continue
            else:
                newparts.append((minval, p[1]))
        return Range(newparts)
    
class RangeSet:
    def __init__(self, ranges: dict[str,Range]):
        self.ranges: dict[str,Range] = ranges

    def score(self) -> int:
        s = 1
        for range in self.ranges.values():
            s *= len(range)
        return s

    def reduceLT(self, var: str, val: int) -> tuple[RangeSet,RangeSet]:
        set1 = {} #Lower
        set2 = {} #Upper

        for v, r in self.ranges.items():
            if v != var:
                set1[v] = r
                set2[v] = r
            else:
                lower = r.reducemax(val)
                upper = r.reducemin(val)
                if len(lower) > 0:
                    set1[v] = lower
                if len(upper) > 0:
                    set2[v] = upper

        return (RangeSet(set1), RangeSet(set2))
    
    def reduceGT(self, var: str, val: int) -> tuple[RangeSet,RangeSet]:

        # x > y => ! (y <= x) => ! (y < x+1)

        a,b = self.reduceLT(var, val+1)
        return (b,a)


#Given a range set, map out the score for applying a rule and everything behind it (recursively applying sub-rules)
def mapCondition(rule: str, term: int, ranges: RangeSet, rules: dict[str,Rule]) -> int:
    r = rules[rule]

    if term >= len(r.terms):
        #Hit the "default" choice
        if r.default == "R":
            return 0
        elif r.default == "A":
            return ranges.score()
        else:
            return mapCondition(r.default, 0, ranges, rules)
    else:
        #Map the first term of the rule
        (var, op, val, iftrue) = r.terms[term]
        if op == "<":
            (truerange, falserange) = ranges.reduceLT(var, val)
        else: # >
            (truerange, falserange) = ranges.reduceGT(var, val)

        #The true value is A, R, or another rule
        if iftrue=="A":
            truescore = truerange.score()
        elif iftrue=="R":
            truescore = 0
        else:
            #Short-circuit right away if range is empty
            if truerange.score() > 0:
                truescore = mapCondition(iftrue, 0, truerange, rules)
            else:
                truescore = 0

        #Keep mapping for next term in rule
        if falserange.score() > 0:
            falsescore = mapCondition(rule, term+1, falserange, rules)
        else:
            falsescore = 0

        return truescore + falsescore
        
    

class Rule:
    def __init__(self, s: str):
        (a,b) = s.split("{")
        self.label = a
        b = b.rstrip("}").split(",")

        self.default = b.pop()

        self.terms = []
        for term in b:
            c, dest = term.split(":")
            var = c[0]
            op = c[1]
            val = int(c[2:])

            assert var in "xmas"
            assert op in "<>"
            self.terms.append([var, op, val, dest])

    def __str__(self):

        stuff = ", ".join([f"{t[0]} -> {t[1]}" for t in self.terms]) + "; " + self.default

        return f"{self.label} - {stuff}"
    
    def __repr__(self):
        return str(self)
    
    def evaluate(self, part: dict[str,int]) -> str:
        for (var, op, val, dest) in self.terms:
            if op == "<":
                if part[var]<val:
                    return dest
            else:
                if part[var]>val:
                    return dest
        return self.default
    
def parsepart(s: str) -> dict[str,int]:
    bits = s.strip("{}").split(",")

    p = {}

    for b in bits:
        (x,y) = b.split("=")
        p[x] = int(y)

    return p

def unstupidify(rules: dict[str,Rule]) -> dict[str,Rule]:
    foundstupid = True
    round = 0

    while foundstupid:
        foundstupid = False
        round += 1
        stupidmap = {}

        newrules: dict[str,Rule] = {}

        #print("Round", round)

        for r in rules.values():
            targets = [x[3] for x in r.terms if x[3]!=r.default]
            if len(targets)==0:
                foundstupid = True
                #print("STUPID: ",r.label)
                stupidmap[r.label] = r.default
            else:
                newrules[r.label] = r

        if foundstupid:
            #Go through all remaining rules and replace stupid targets
            for r in newrules.values():
                mod = False
                for t in r.terms:
                    if t[3] in stupidmap:
                        t[3] = stupidmap[t[3]]
                        mod = True
                if r.default in stupidmap:
                    r.default = stupidmap[r.default]
                    mod = True
                
                if mod:
                    pass
                    #print("Sanitized rule", r.label)

        rules = newrules
    return rules

def part1(rules, parts):

    score = 0

    for part in parts:
        pos = "in"
        steps = [pos]
        while pos not in ["A", "R"]:
            pos = rules[pos].evaluate(part)
            steps.append(pos)

        #print("->".join(steps))

        if pos == "A":
            score += sum(part.values())

    return score

def part2(rules):
    allvalues = {
        "x": Range([(1, 4000)]),
        "m": Range([(1, 4000)]),
        "a": Range([(1, 4000)]),
        "s": Range([(1, 4000)]),
    }

    return mapCondition("in", 0, RangeSet(allvalues), rules)

unstupid = False

if __name__ == "__main__":
    input = readinput()
    rules_in, parts_in = chunks(input)

    rules: dict[str,Rule] = {}
    parts: list[dict[str,int]] = []

    for r in rules_in:
        rule = Rule(r)
        rules[rule.label] = rule
    
    #Optionally "unstupidify" rules (find rules like lnx{m>1548:A,A} where all outcomes are the same, and then replace all references to "lnx" with "A" )
    if unstupid:
        a = len(rules)
        rules = unstupidify(rules)
        b = len(rules)

        if b!=a:
            print(f"Sanitized {a} rules to {b}.")

        for p in parts_in:
            parts.append(parsepart(p))

    p1 = part1(rules, parts)
    print("Part 1:", p1)

    p2 = part2(rules)
    print("Part 2:", p2)