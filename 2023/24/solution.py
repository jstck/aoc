#!/usr/bin/env python3

from itertools import combinations
import sympy
import random
import sys


sys.path.append("../..")
from lib.aoc import *

def intersection2d(lineA: tuple[int,...], lineB: tuple[int,...], xymin, xymax) -> bool:

    x1,y1,_,dxa,dya,_ = lineA
    x3,y3,_,dxb,dyb,_ = lineB
    
    #print(f"Hailstone A: {x1}, {y1}, {z1} @ {dxa}, {dya}, {dza}")
    #print(f"Hailstone B: {x3}, {y3}, {z3} @ {dxb}, {dyb}, {dzb}")

    #Parallel lines
    if dya/dxa == dyb/dxb:
        #print("Parallel")
        #print()
        return False
    
    x2,y2 = x1+dxa,y1+dya
    x4,y4 = x3+dxb,y3+dyb

    #Yes, I got this off of wikipedia.
    denom = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
    assert denom != 0.0

    px = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/denom
    py = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/denom
    #print(f"Intersection at x={px:.4f}, y={py:.4f}")
    if px < xymin or px > xymax or py<xymin or py>xymax:
        #print("Outside test area")
        #print()
        return False

    tA = (px-x1)/dxa
    tB = (px-x3)/dxb
    #pastA = (px>x1 ^ dxa>0)
    #pastB = (px>x3 ^ dxb>0)
    pastA = tA<0
    pastB = tB<0
    if pastA:
        #print("In past for A")
        #print()
        return False
    if pastB:
        #print("In past for B")
        #print()
        return False
    #print("Valid")
    #print()
    
    return True
    
def part1(lines: list[tuple[int,...]]):

    count = 0

    #Sample data
    xymin=7
    xymax=27

    if len(lines)>10:
        xymin = 200000000000000
        xymax = 400000000000000

    for l1,l2 in combinations(lines, 2):
        if intersection2d(l1,l2,xymin,xymax):
            count += 1

    return count

def part2(hail: list[tuple[int,...]]):

    #pick any three hailstones, enough to solve the equations
    #hail3 = hail[:3]
    hail3 = random.choices(hail, k=3)

    #Sympy symbols
    wanted = x0, y0, z0, vx0, vy0, vz0 = sympy.symbols("x0 y0 z0 vx0 vy0 vz0")
    tsyms = sympy.symbols("t1 t2 t3")
    unknowns = wanted+tsyms

    eq = []
    for hailstone, t in zip(hail3, tsyms):
        (x1, y1, z1, vx1, vy1, vz1) = hailstone
        #Equations to match at x, y, z at some point in time
        #(hailstone position - rock position = 0)
        eq.append(x1+t*vx1 - x0+t*vx0)
        eq.append(y1+t*vy1 - y0+t*vy0)
        eq.append(z1+t*vz1 - z0+t*vz0)

    solutions = sympy.solve(eq, unknowns, dict=True)

    assert len(solutions)==1
    solution = solutions[0]
    #print(solution)

    return solution[x0]+solution[y0]+solution[z0]


if __name__ == "__main__":
    input = readinput()

    hail = []

    for line in input:
        parts = tuple([int(p.rstrip(",")) for p in line.split() if p != "@"])
        hail.append(parts)
        

    p1 = part1(hail)
    print("Part 1:", p1)

    p2 = part2(hail)
    print("Part 2:", p2)