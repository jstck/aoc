#!/usr/bin/env python3

import sys
import re

answers = set()

sum = 0
ln=0

rawin = sys.stdin.read()

rules = rawin.split("\n")

#What may be inside a certain colored bag
contents = {}

#What may contain a certain colored bag
containers = {}

colors = set()

for rule in rules:
    words = rule.split()
    container = " ".join(words[0:2]).strip()
    if len(container) == 0:
        continue #Something's broken, it's your fault

    colors.add(container)
    rule_contents = " ".join(words[4:]).rstrip(".")

    if not container in contents:
        contents[container] = []

    if rule_contents == "no other bags":
        continue

    rule_parts = rule_contents.split(", ")

    for part in rule_parts:
        n = int(part.split()[0])
        content = " ".join(part.split()[1:3])

        colors.add(content)

        
        contents[container].append((n, content))

        if not content in containers:
            containers[content] = set([container])
        else:
            containers[content].add(container)


def process_bag(color):
    count = 1 #Count this bag
    contains = contents[color]
    print("Processing", color, ":", contains)
    for (n, c) in contains:
        print(color, "contains", n, c, "bags")
        count += n * process_bag(c)
    print("this makes", color, "total", count, "bags")
    return count

print(process_bag("shiny gold")-1)
