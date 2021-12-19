#!/usr/bin/env python3

import sys
import argparse
import re

match = re.search(r'aoc/?(\d+)/(\d+)', __file__)
if match:
    descr = "Advent of Code " + match.group(1) + ":" + match.group(2)
else:
    descr = "Advent of some kind of Code"

parser = argparse.ArgumentParser(description = descr)

parser.add_argument('-1', action='store_true', help="Do part 1")
parser.add_argument('-2', action='store_true', help="Do part 2")
parser.add_argument('--verbose', '-v', action='count', default=0, help="Increase verbosity")

args = parser.parse_args()

part2 = vars(args)["2"]
part1 = vars(args)["1"] or not part2 #Do part 1 if not part 2 specified
verbosity = vars(args)["verbose"]

#Print controlled by verbosity level
def vprint(*args):
    if args[0]<= verbosity:
        print(*args[1:])

input = [l.strip() for l in sys.stdin.readlines()]

def explode(expr, stack = [], path = []):
    if type(expr) is not list:
        print("obegripligt: ", expr)

    int0 = type(expr[0]) is int
    int1 = type(expr[1]) is int

    if not int0:
        exploded = explode(expr[0], stack+[expr], path + [0])
        if exploded: return exploded
    
    if not int1:
        exploded = explode(expr[1], stack+[expr], path + [1])
        if exploded: return exploded

    if int0 and int1:
        if len(stack)>=4:
            #print("Explode", expr, path)

            (l,r) = expr

            #Left explosion. Backtrack path until a 1 (meaning there's something to the left)
            for i in range(len(path)-1,-1,-1):
                if path[i] == 1:
                    pos = stack[i]
                    #print("Leftplosion", i, pos, l)

                    if type(pos[0]) is int:
                        pos[0]+= l
                    else:
                        pos = pos[0]
                        while type(pos[1]) is not int:
                            pos = pos[1]
                        pos[1] += l
                    break
                        

            #Right explosion. Backtrack path until a 0 (meaning there's something to the right
            for i in range(len(path)-1,-1,-1):
                if path[i] == 0:
                    pos = stack[i]
                    #print("Rightplosion", i, pos, r)

                    if type(pos[1]) is int:
                        pos[1]+= r
                    else:
                        pos = pos[1]
                        while type(pos[0]) is not int:
                            pos = pos[0]
                        pos[0] += r
                    break
            
            #Zero out this pair
            stack[-1][path[-1]] = 0

                        
            return True
        
    return False

def splitnum(x):
    l = x//2
    r = (x+1)//2
    return [l, r]

def split(expr):

    if type(expr) is int:
        print("ERROR: split called on int", expr)
        sys.exit(0)
        return

    (l,r) = expr

    if type(l) is int:
        if l > 9:
            expr[0] = splitnum(l)
            return True
    else:
        if split(expr[0]):
            return True

    if type(r) is int:
        if r > 9:
            expr[1] = splitnum(r)
            return True
    else:
        if split(expr[1]):
            return True

    return False


def magnitude(expr):
    if type(expr[0]) is int:
        mag = 3*expr[0]
    else:
        mag = 3*magnitude(expr[0])

    if type(expr[1]) is int:
        mag += 2*expr[1]
    else:
        mag += 2*magnitude(expr[1])

    return mag


def process(expr):
    while True:
            if explode(expr):
                vprint(1, "Exploded:", expr)
                continue

            if split(expr):
                vprint(1, "Split:", expr)
                continue
            break


#print(input)

if part1:
    a = eval(input.pop(0))

    while len(input)>0:
        b = eval(input.pop(0))

        a = [a, b]

        process(a)

    print("Final result:")
    print(a)
    print("Magnitude:", magnitude(a))


def foo():
    a = [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    b = [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]

    e = [a,b]

    print(a)
    print(b)
    print(e)
    process(e)
    print(e)

    print(magnitude(e))

if part2:
    best = 0
    for x in range(len(input)):
        for y in range(len(input)):
            if x==y:
                continue
            a = eval(input[x])
            b = eval(input[y])
            e = [a, b]
            #print(e)
            process(e)
            m = magnitude(e)

            if m > best:
                print("New best %d+%d: %d" % (x, y, m))
                best = m

    print("Highest result:", best)