#!/usr/bin/env python3

import sys
sys.path.append("../..")
from lib.aoc import *
from collections import defaultdict

def validate_update(rules_before: dict[int,set[int]], rules_after: dict[int,set[int]], update: list[int]) -> bool:

#    print("Validating", update)

    for i in range(len(update)):
        before = update[:i]
        item = update[i]
        after = update[i+1:]

        for b in before:
            if b in rules_after[item]:
#                print(f"Breaks due to {item}|{b}")
                return False
            
        for a in after:
            if a in rules_before[item]:
#                print(f"Breaks due to {a}|{item}")
                return False

    return True


def part1(rules_before: dict[int,set[int]], rules_after: dict[int,set[int]], updates: list[list[int]]) -> int:
    sum = 0
    for update in updates:
        valid = validate_update(rules_before, rules_after, update)
        if(valid):
            middle = update[len(update)//2]
            sum += middle
    return sum

def swapsies(l: list[int], a: int, b: int) -> list[int]:
    l2 = l[:]
    for i, x in enumerate(l):
        if x==a:
            l2[i]=b
        elif x==b:
            l2[i]=a
    return l2

    

def part2(rules_before: dict[int,set[int]], rules_after: dict[int,set[int]], updates: list[list[int]]) -> int:
    sum = 0
    for update in updates:
        valid = validate_update(rules_before, rules_after, update)
        if valid: continue

        print("Transmogrifying", update)
    
        newupdate = update[:]

        fixed = True
        
        while fixed:
            fixed = False
            #Find a rule that is broken, swap elements to fix it
            for i in range(len(newupdate)):
                before = newupdate[:i]
                item = newupdate[i]
                after = newupdate[i+1:]

                for b in before:
                    if b in rules_after[item]:
                        newupdate = swapsies(newupdate, item, b)
                        fixed = True
                        break
                
                if fixed: break
                    
                for a in after:
                    if a in rules_before[item]:
                        newupdate = swapsies(newupdate, item, a)
                        fixed = True
                        break

                if fixed: break

        #Make sure it's good now
        valid = validate_update(rules_before, rules_after, newupdate)

        if not valid:
            print("COULD NOT FIX", update)
        else:
            print("Fixed", update, "to", newupdate)
            middle = newupdate[len(newupdate)//2]
            sum += middle
    return sum

if __name__ == "__main__":

    (rules, updates) = chunks(readinput())


    befores = defaultdict(set)
    afters = defaultdict(set)

    for rule in rules:
        a,b = map(int, rule.split("|"))
        afters[a].add(b)
        befores[b].add(a)


    updates = [list(map(int, u.split(","))) for u in updates]

    print("Rules:", len(rules))
    print("Updates:", len(updates))
    print("Max update:", max(map(len,updates)))


    print("Part 1:", part1(befores,afters,updates))

    print("Part 2:", part2(befores,afters,updates))