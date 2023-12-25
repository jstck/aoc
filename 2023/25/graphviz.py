#!/usr/bin/env python3
import sys

#Make a graphviz dot file so a human can spot the three edges needed to cut

sys.path.append("../..")
from lib.aoc import *

if __name__ == "__main__":
    input = readinput()

    print("digraph {")

    for line in input:
        a, b = line.split(":")
        c = b.strip().split()

        print(f"  {a} -> {{{' '.join(c)}}};")

    print("}")


#Render with
# ./graphviz.py < input.txt > graph.dot
# dot -Tsvg -Kneato graph.dot > graph.svg