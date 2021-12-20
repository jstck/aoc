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

#for line in sys.stdin.readlines():
#    pass

input = [l.strip() for l in sys.stdin.readlines()]

def c2b(c):
    if c=="#":
        return 1
    return 0

def b2c(b):
    if b==1:
        return '#'
    return '.'

def b2c2(b):
    if b==1:
        return '[]'
    return ' .'

def printImage(image):
    for line in image:
        print(''.join([b2c(c) for c in line]))
    y = len(image)
    x = len(image[0])
    print(x,"X",y,":",pixelCount(image))
    print()

infinity=0

def getPixelBounded(image,x,y):
    global infinity
    if y<0 or y>=len(image):
        return infinity
    line = image[y]
    if x<0 or x>=len(line):
        return infinity
    return line[x]

def getPixelIndex(image,x,y):
    index = 0
    for dy in [-1,0,1]:
        for dx in [-1,0,1]:
            index = index*2 + getPixelBounded(image,x+dx,y+dy)
    return index

def enhance(image, expand=1):
    global algo
    output = []
    xmax = len(image[0])
    ymax = len(image)
    for y in range(-expand,ymax+expand):
        line = []
        for x in range(-expand,xmax+expand):
            idx = getPixelIndex(image,x,y)
            px = algo[idx]
            line.append(px)
        output.append(line)
    return output

def chomp(image, border=2):
    return [line[border:-border] for line in image[border:-border]]

def pixelCount(image):
    return sum([sum(row)  for row in image])

algo = [c2b(c) for c in input[0]]

infinity = 0

image = [[c2b(c) for c in row] for row in input[2:]]

iterations = 2

if part2:
    iterations = 50

for iter in range(iterations):
    print(iter,infinity)
    image = enhance(image)
    infinity = algo[-infinity]


printImage(image)
