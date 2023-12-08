import math
from typing import List, Tuple, Dict

def parse(input: list[str]) -> Tuple[List[str],Dict[str,Tuple[str,str]]]:
    moves = input.pop(0)

    moves = list(moves.strip())
    input.pop(0) #I've got a blank line, baby

    graph = {}

    for line in input:
        a, b = line.split("=")

        a = a.strip()

        b = b.strip("() ")

        x, y = b.split(",")
        x = x.strip()
        y = y.strip()

        graph[a] = (x,y)

    return (moves, graph)

def findpath(moves, graph, pos) -> Tuple[int, str]:
    
    count = 0
    nmoves = len(moves)

    while pos[-1] != "Z":
        move = moves[count % nmoves]
        (left, right) = graph[pos]
        if move == "L":
            pos = left
        else:
            pos = right

        count += 1

    return (count, pos)

def part1(input: list[str]) -> int:
    (moves, graph) = parse(input)

    pos = "AAA"

    a = findpath(moves, graph, pos)

    print(f"Got to {a[1]} in {a[0]} moves.")

    return a[0]


def part2(input: list[str]) -> int:
    (moves, graph) = parse(input)

    starts = [x for x in graph.keys() if x[-1] == "A"]

    paths = []

    for pos in starts:
        (c, x) = findpath(moves, graph, pos)
        print(f"{pos} -> {x}: {c}")
        paths.append(c)

    result = math.lcm(*paths)

    return result