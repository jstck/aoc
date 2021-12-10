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
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


n = 0

allscores = []

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
                #print(n, "Corrupted line")
                stack=[]
                break
        #Any other characters are just ignored.

    #Completed / corrupted lines
    if len(stack)==0:
        continue

    print(n, "incomplete line")
    closer = [pairs[x] for x in reversed(stack)]
    score = 0
    print("".join(closer))
    for c in closer:
        score = score * 5 + scores[c]

    print(score)
    print()
    allscores.append(score)

allscores.sort()

mid = int((len(allscores)-1) / 2)

print(allscores)
print(mid, len(allscores))

print("Middle score:", allscores[mid])