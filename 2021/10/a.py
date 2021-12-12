#!/usr/bin/env python3

import sys

lefts = frozenset(('(','[','{','<'))
rights = frozenset((')',']','}','>'))

pairs = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

score = 0

n = 1

for line in sys.stdin.readlines():

    n += 1
    chonk = list(line.strip())
    
    stack = []

    for c in chonk:
        if c in lefts:
            stack.append(c)
        elif c in rights:
            l = stack.pop()
            if not pairs[l] == c:
                print(n, "Expected", pairs[l], "got",c)
                score += scores[c]
                break
        #Any other characters are just ignored.

print("Total score", score)