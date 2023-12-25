#!/usr/bin/env python3
from functools import reduce
from operator import mul
import sys
import networkx as nx

G = nx.Graph()

for line in sys.stdin.readlines():
    a, b = line.strip().split(":")
    c = b.strip().split()
    for d in c:
        G.add_edge(a,d)

cuts = nx.minimum_edge_cut(G)
print("Cut edges:", cuts)
for (a,b) in cuts:
    G.remove_edge(a,b)

sizes = [len(G.subgraph(c)) for c in nx.connected_components(G)]
print(f"Found {len(sizes)} subgraphs of sizes {', '.join(map(str,sizes))}")
print("THE ANSWER:", reduce(mul, sizes))
