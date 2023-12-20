#!/usr/bin/env python3

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


class Rule:
    def __init__(self, s: str):
        (a,b) = s.split("{")
        self.label = a
        b = b.rstrip("}").split(",")

        self.default = b.pop()

        self.terms = []
        for term in b:
            self.terms.append(term.split(":"))

    def __str__(self):

        stuff = ",".join([f"{t[0]}:{t[1]}" for t in self.terms])

        return f"{self.label}{{{stuff},{self.default}}}"
    
    def __repr__(self):
        return str(self)
    
    def evaluate(self, part: dict[str,int]) -> str:
        for (expr, target) in self.terms:
            if eval(expr, None, part):
                return target
        return self.default
    

if __name__ == "__main__":
    input = readinput()
    rules_in, parts_in = chunks(input)

    rules: dict[str,Rule] = {}
    
    for r in rules_in:
        rule = Rule(r)
        rules[rule.label] = rule

    foundstupid = True
    round = 0

    while foundstupid:
        foundstupid = False
        round += 1
        stupidmap = {}

        newrules: dict[str,Rule] = {}

        print("Round", round)

        for r in rules.values():
            targets = [x[1] for x in r.terms if x[1]!=r.default]
            if len(targets)==0:
                foundstupid = True
                print("STUPID: ",r.label)
                stupidmap[r.label] = r.default
            else:
                newrules[r.label] = r

        if foundstupid:
            #Go through all remaining rules and replace stupid targets
            for r in newrules.values():
                mod = False
                for t in r.terms:
                    if t[1] in stupidmap:
                        t[1] = stupidmap[t[1]]
                        mod = True
                if r.default in stupidmap:
                    r.default = stupidmap[r.default]
                    mod = True
                print("Sanitized rule", r.label)

        rules = newrules
        print()

    for r in rules.values():
        print(r)
                