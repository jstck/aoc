#!/usr/bin/env python3

from queue import PriorityQueue
from dataclasses import dataclass

import re
import sys

sys.path.append("../..")
from lib.aoc import *


@dataclass(frozen=True)
class Problem:
    ax: int
    ay: int
    bx: int
    by: int
    px: int
    py: int

    def parts(self) -> list[int]:
        return [self.ax,self.ay,self.bx,self.by,self.px,self.py]
    
#Plain BFS, which is overkill but works well enough on P1
def bfs(problem: Problem) -> int:
    pq = PriorityQueue()
    visited = set()

    #Queue on cost,x,y
    pq.put((0, 0, 0))

    while not pq.empty():
        (cost,x,y) = pq.get()
        if (x,y) in visited: continue
        visited.add((x,y))

        if x > problem.px or y > problem.py: continue

        if x == problem.px and y == problem.py:
            return cost
        
        #Press each button
        pq.put((cost+3,x+problem.ax,y+problem.ay))
        pq.put((cost+1,x+problem.bx,y+problem.by))

    #No path found
    return -1

#"Correct-first-search". Check the gradient (x/y) to the solution, and only press buttons
#that go closer the target gradient. Works on P1, but not at all on P2.
def cfs(problem: Problem) -> int:
    pq = PriorityQueue()
    visited = set()

    #Queue on cost,x,y
    pq.put((0, 0, 0))

    #target gradient (almost the angle)
    tg = problem.py/problem.px

    while not pq.empty():
        (cost,x,y) = pq.get()
        if (x,y) in visited: continue
        visited.add((x,y))

        if x > problem.px or y > problem.py: continue

        if x == problem.px and y == problem.py:
            return cost
        
        cg = (problem.py-y)/(problem.px-x)

        for (dc, dx, dy) in [(3,problem.ax,problem.ay), (1,problem.bx,problem.by)]:
            x1,y1 = x+dx,y+dy

            #If we found solution, break here already to avoid division by zero
            if x1 == problem.px and y1 == problem.py:
                return cost+dc
            
            #No really, don't divide by zero
            if x1 == problem.px:
                continue

            ng = (problem.py-y1)/(problem.px-x1)

            if abs(ng) <= abs(cg):
                #print("Qing",x1,y1)
                pq.put((cost+dc,x1,y1))

    #No path found
    return -1

#Solve linear equation system, check for integer solution. If there is one, it's all good.
def justDoMath(problem: Problem)-> int:
    x1,y1,x2,y2,x3,y3 = problem.parts()

    try:
        if (x3*y2-x2*y3)%(x1*y2-x2*y1) != 0:
            return -1
        if (x3*y1-x1*y3)%(x2*y1-x1*y2) != 0:
            return -1
    except ZeroDivisionError:
        return -1 #Some edge case, will not have a solution (no input has x/y=0)

    a = (x3*y2-x2*y3)//(x1*y2-x2*y1)
    b = (x3*y1-x1*y3)//(x2*y1-x1*y2)

    assert a>0
    assert b>0

    return a*3+b


if __name__ == "__main__":

    p1 = 0
    p2 = 0

    part_2_badness = 10000000000000

    for chunk in chunks(readinput()):
        (ax,ay) = re.findall(r"Button A: X\+(\d+), Y\+(\d+)", chunk[0])[0]
        (bx,by) = re.findall(r"Button B: X\+(\d+), Y\+(\d+)", chunk[1])[0]
        (px,py) = re.findall(r"Prize: X=(\d+), Y=(\d+)", chunk[2])[0]

        (ax,ay,bx,by,px,py) = map(int, (ax,ay,bx,by,px,py))

        problem1 = Problem(ax,ay,bx,by,px,py)
        problem2 = Problem(ax,ay,bx,by,px+part_2_badness,py+part_2_badness)

        ag = ax/ay
        bg = bx/by
        pg = px/py

        #print(problem1)

        #cost = bfs(problem1)
        #cost = cfs(problem1)
        cost = justDoMath(problem1)
        cost2 = justDoMath(problem2)

        if cost >= 0:
            p1 += cost

        if cost2 >= 0:
            p2 += cost2

    print("Part 1:", p1)
    print("Part 2:", p2)
