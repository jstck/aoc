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
        continue

    colors.add(container)
    rule_contents = " ".join(words[4:]).rstrip(".")
    
    if rule_contents == "no other bags":
        continue

    rule_parts = rule_contents.split(", ")

    for part in rule_parts:
        n = int(part.split()[0])
        content = " ".join(part.split()[1:3])

        colors.add(content)

        if not container in contents:
            contents[container] = set([content])
        else:
            contents[container].add(content)

        if not content in containers:
            containers[content] = set([container])
        else:
            containers[content].add(container)


my_containers = set()

process_stuff = list(containers["shiny gold"])

while len(process_stuff) > 0:
    a = process_stuff.pop()
    if a not in my_containers:
        my_containers.add(a)
        if a in containers:
            for c in containers[a]:
                process_stuff.append(c)

print(my_containers)
print(len(my_containers))
