#!/usr/bin/env python3

import sys
import re

answers = set()

sum = 0
ln=0

rawin = sys.stdin.read()

groups = rawin.split("\n\n")

sum = 0

for group in groups:
    responses = group.split("\n")
    
    answers = None
    freshbatch = True
    for response in responses:
        if freshbatch:
            answers = set(list(response))
            freshbatch = False
        else:
            answers.intersection_update(set(list(response)))
    sum += len(answers)

print(sum)