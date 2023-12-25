#!/usr/bin/env python3
import sys
from graphviz import Graph

#Make a graphviz dot file so a human can spot the three edges needed to cut

sys.path.append("../..")
from lib.aoc import *

input = readinput()

g = Graph(
    name="aoc202325",
    comment="AoC 2023-25",
    engine="neato",
)

for line in input:
    a, b = line.split(":")
    c = b.strip().split()

    for n in c:
        g.edge(a,n,label=f"{a}-{n}")

g.render(
    outfile="graph.svg",
    format="svg",
    filename="graph.gv",
)

#CLI render with
# dot -Tsvg -Kneato graph.gv > graph.svg