#!/usr/bin/env python3

from queue import PriorityQueue
import sys
from ortools.linear_solver import pywraplp

sys.path.append("../..")
from lib.aoc import *

def l2s(lights: list[bool]) -> str:
    return "".join(["#" if light else "." for light in lights])

def bfs1(lights: list[bool], buttons: list[tuple[int,...]]) -> int:

    q: PriorityQueue[tuple[int, list[bool]]] = PriorityQueue()

    n = len(lights)
    start = [False]*n

    q.put((0, start))

    seen: set[tuple[bool,...]] = set()

    def presbutan(lights: list[bool], butan: tuple[int,...]) -> list[bool]:
        newlights = lights[:]
        for i in butan:
            newlights[i] = not newlights[i]
        return newlights
    
    while not q.empty():
        cost, state = q.get_nowait()
        if state == lights:
            return cost

        if tuple(state) in seen:
            continue

        #print(f"{cost}: {l2s(state)}")

        seen.add(tuple(state))

        for button in buttons:
            newlights = presbutan(state, button)
            if not tuple(newlights) in seen:
                q.put((cost+1, newlights))

    #No path found
    return -1

#Warning: Does not finish in at least one forever for real input, works for examples.
def bfs2(counters: list[int], buttons: list[tuple[int,...]]) -> int:

    q: PriorityQueue[tuple[int, list[int]]] = PriorityQueue()

    n = len(counters)
    start = [0]*n

    q.put((0, start))

    seen: set[tuple[int,...]] = set()
    queued: set[tuple[int,...]] = set() #Extra set of same stuff just to avoid all the multiple paths to same state

    maxcost = sum(counters)

    def presbutan2(counters: list[int], butan: tuple[int,...]) -> list[int]:
        newcounters = counters[:]
        for i in butan:
            newcounters[i] += 1
        return newcounters
    
    while not q.empty():
        cost, state = q.get_nowait()

        if state == counters:
            return cost

        if tuple(state) in seen:
            continue

        print(f"At {cost}, {state}, l={q.qsize()}")


        if cost > maxcost:
            return -1

        #print(f"{cost}: {l2s(state)}")

        seen.add(tuple(state))

        for button in buttons:
            #print(f"Lights: {l2s(lights)}, pressing {button}")
            newcounters = presbutan2(state, button)
            #print(f"qing: {cost}, {l2s(newlights)}")

            #No point going anywhere where a counter is exceeded
            if min([a-b for a,b in zip(counters,newcounters)]) < 0:
                continue

            if not tuple(newcounters) in seen:
                ns = tuple([cost+1] + newcounters)
                if not ns in queued:
                    queued.add(ns)
                    q.put((cost+1, newcounters))
                
    #No path found
    return -1

def lpsolve(counters: list[int], buttons: list[tuple[int,...]]) -> int:
    nbounds = len(counters)
    nbuttons = len(buttons)

    solver = pywraplp.Solver.CreateSolver("SAT")

    infinity = solver.infinity()

    x = {}

    objective = solver.Objective()

    for i in range(nbuttons):
        x[i] = solver.IntVar(0.0, infinity, f"x{i}")
        objective.SetCoefficient(x[i], 1)

    objective.SetMinimization()

    for i in range(nbounds):
        row = [0] * nbuttons

        constraint = solver.RowConstraint(counters[i],counters[i], f"c{i}")
        for j in range(nbuttons):
            if i in buttons[j]:
                constraint.SetCoefficient(x[j], 1)

    #print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = round(solver.Objective().Value())
        # print("Objective value =", solver.Objective().Value())
        # for j in range(nbuttons):
        #     print(x[j].name(), " = ", x[j].solution_value())
        # print()
        # print(f"Problem solved in {solver.wall_time():d} milliseconds")
        # print(f"Problem solved in {solver.iterations():d} iterations")
        # print(f"Problem solved in {solver.nodes():d} branch-and-bound nodes")
        return result
    else:
        # print("The problem does not have an optimal solution.")
        return -1


if __name__ == "__main__":
    input = readinput()

    p1 = 0
    p2 = 0

    for line in input:
        bits = line.split(" ")

        lights = bits[0]
        buttons = bits[1:-1]
        joltages = bits[-1]
        

        blights = [c=="#" for c in lights[1:-1]] #Get rid of brackets, turn to list of bools
        buttons = [eval(x) for x in buttons]
        buttons = [(x,) if isinstance(x, int) else x for x in buttons]
        joltages = eval("[" + joltages[1:-1] + "]")

        cost1 = bfs1(blights, buttons)

        assert cost1 > 0

        cost2 = lpsolve(joltages, buttons)

        assert cost2 > 0

        #print(f"{cost1} {cost2}")
        #print()

        p1 += cost1
        p2 += cost2

    print("Part 1:", p1)
    print("Part 2:", p2)
