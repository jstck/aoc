#!/usr/bin/env python3

from typing import List, TypeAlias, DefaultDict, Iterator

import networkx as nx
import sys


sys.path.append("../..")
from lib.aoc import *

edge: TypeAlias = tuple[str,str]


allnodes: List[str] = []

graph: DefaultDict[str,list[str]] = DefaultDict(list)

#Try make a clique from this using all nodes later in alphabetical order
def expand(nodes: set[str]) -> Iterator[set[str]]:
    lastnode = list(nodes)[-1]
    hit=False

    #Any potential things to add must be a neighbour of all members so far
    potentates = set(allnodes)
    for n in nodes:
        potentates.intersection_update(graph[n])

    for newnode in potentates:
        if newnode <= lastnode: continue

        if newnode in nodes: continue

        #Check that this new node is connected to all existing nodes in set
        neighs = set(graph[newnode])
        if neighs.issuperset(nodes):
            hit=True
            yield from expand(nodes.union([newnode]))

    if not hit:
        #This is as far as we can get with this set
        yield nodes


if __name__ == "__main__":
    input = readinput()

    edges: list[edge] = []

    G = nx.Graph()


    for line in input:
        a,b = sorted(line.strip().split("-"))
        e: edge = (a,b)
        edges.append(e)
        graph[a].append(b)
        graph[b].append(a)
        G.add_edge(a,b)

    cliques: list[tuple[str,str,str]] = []

    allnodes = list(graph.keys())
    allnodes.sort()

    #Go through all pairs of connected nodes
    for node1 in allnodes:
        for node2 in graph[node1]:
            #Do things in alphabetical order to not do duplicate work
            if node2 < node1:
                continue

            #All common neighbours of both node1 and node2
            nodes3 = set(graph[node1]).intersection(set(graph[node2])) - set([node1,node2])
            for node3 in nodes3:
                if node3 < node2:
                    continue
                cliques.append((node1,node2,node3))

    count = 0
    for c1,c2,c3 in cliques:
        if c1[0] == "t" or c2[0] == "t" or c3[0] =="t":
            count += 1

    print("Part 1:", count)

    #Find the maximum size clique. NP hard!
    #maxclique = set()
    #c = 0
    #print("Total nodes:", len(allnodes))
    #for node in allnodes:
    #    c += 1
    #    print(c, node)
    #    for candidate in expand(set([node])):
    #        if len(candidate) > len(maxclique):
    #            print("New best clique of size", len(candidate), ",".join(sorted(list(candidate))))
    #            maxclique = candidate
    
    bestparty = []
    bestlen = 0

    for party in nx.find_cliques(G):
        if len(party) > bestlen:
            bestparty = sorted(list(party))
            bestlen = len(bestparty)
    
    print("Part 2:", ",".join(sorted(list(bestparty))))
