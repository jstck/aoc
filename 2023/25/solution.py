#!/usr/bin/env python3
from __future__ import annotations

from functools import cache
from itertools import combinations, permutations
import collections
from queue import PriorityQueue, SimpleQueue
from collections import defaultdict, deque, Counter, OrderedDict
import heapq
from dataclasses import dataclass
import math
import re
import sys
from typing import TypeAlias, Optional, Iterable, Mapping

import math
import re
import sys
import networkx as nx
import copy


sys.path.append("../..")
from lib.aoc import *

def findcuts(graph: dict[str,set[str]]) -> set[tuple[str,str]]:
    G = nx.Graph()


    for node, neighbours in graph.items():
        for neighbour in neighbours:
            G.add_edge(node, neighbour)

    print(G)

    cuts = nx.minimum_edge_cut(G)

    print("Found cut list of length", len(cuts), ":", cuts)

    return cuts


def cutgraph(graph: dict[str,set[str]], cuts: Iterable[tuple[str,str]]) -> int:

    #Make graph be bidirectional so we find everything easier
    reverse = {}
    for node, neigh in graph.items():
        for n in neigh:
            if n in reverse.keys():
                reverse[n].add(node)
            else:
                reverse[n] = set([node])

    # print("FORWARD:")
    # for k,v in graph.items():
    #     print(k,v)
    # print()
    # print("REVERSE:")
    # for k,v in reverse.items():
    #     print(k,v)
    # print()
    

    for k,v in reverse.items():
        if k in graph:
            graph[k].update(v)
        else:
            graph[k] = v

    # print("FULL GRAPH:")
    # for k,v in graph.items():
    #     print(k,v)

    #Remove cut wires
    for a,b in cuts:
        #print("Cutting", a, b)
        graph[a].remove(b)
        graph[b].remove(a)

    q: SimpleQueue[str] = SimpleQueue()


    subgraph = set()
    #Pick first element to expand subgraph from
    q.put(list(graph.keys())[0])

    while not q.empty():
        node = q.get_nowait()
        if node in subgraph: continue

        subgraph.add(node)

        #Remove neighbours from graph but add them all to queue
        neighbours = graph[node]
        del graph[node]

        for neighbour in neighbours:
            q.put_nowait(neighbour)
            #Remove neighbours link back here
            graph[neighbour].remove(node)

    size1 = len(subgraph)
    size2 = len(graph)

    print("Found subraph of size", size1)
    print("Remains", size2)


    return size1*size2


if __name__ == "__main__":
    input = readinput()

    graph = {}

    for line in input:
        a, b = line.split(":")
        c = b.strip().split()
        assert a not in graph
        graph[a] = set(c)

    cuts = findcuts(graph)

    #Fake cuts for sample
    #if len(input) < 20:
    #    cuts = {("hfx","pzl"), ("bvb", "cmg"), ("nvd", "jqt")}

    answer = cutgraph(graph,cuts)
    print("THE ANSWER:", answer)
