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
parser.add_argument('-t', action='store_true', help="Run tests")
parser.add_argument('-f', '--input-file', default='input.txt')
parser.add_argument('--verbose', '-v', action='count', default=0, help="Increase verbosity")

args = parser.parse_args()

tests = vars(args)["t"]
run2 = vars(args)["2"]
run1 = vars(args)["1"] or not run2 #Do part 1 if nothing else specified
verbosity = vars(args)["verbose"]
input_file = vars(args)["input_file"]


#Print controlled by verbosity level
def vprint(*args):
    if args[0]<= verbosity:
        print(*args[1:])

def chunks(input, ints=False):
    chunk = []
    chunky = []
    for line in input:
        if len(line) == 0:
            chunky.append(chunk)
            chunk = []
        else:
            if ints:
                chunk.append(int(line))
            else:
                chunk.append(line)

    if len(chunk)>0:
        chunky.append(chunk)
    return chunky



test_cases = [
    {
        "input": """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""",
        "output": 95437,
        "output2": 24933642
    }
]

FILES = "_FILES_"
SUM = "_SUM_"

def makedir(tree, pwd):
    node = tree

    for p in pwd:
        if not p in node:
            node[p] = {}
        node = node[p]

def addfile(tree, pwd, name, size):
    #CD
    node = tree
    for p in pwd:
        node = node[p]

    if not FILES in node:
        node[FILES] = {}
    node[FILES][name] = size

def sumdir(node):
    vprint(2, node)
    sum = 0
    if FILES in node:
        for size in node[FILES].values():
            sum += size

    for (dir, tree) in node.items():
        if dir != FILES and dir != SUM and isinstance(tree, dict):
            sum += sumdir(tree)
    node[SUM] = sum
    return sum

def findsmaller(name, node, limit):
    mysize = node[SUM]
    if mysize <= limit:
        yield (name, mysize)
    for (dir, tree) in node.items():
        if dir != FILES and dir != SUM and isinstance(tree, dict):
            yield from findsmaller(dir, tree, limit)

def findlarger(name, node, limit):
    mysize = node[SUM]
    if mysize >= limit:
        yield (name, mysize)
    for (dir, tree) in node.items():
        if dir != FILES and dir != SUM and isinstance(tree, dict):
            yield from findlarger(dir, tree, limit)
    

def parse(input):

    pwd = []

    tree = {}

    for line in input:
        if len(line) == 0: continue
        if line[0] == "$":
            cmd = line.split(" ")
            vprint(2, cmd)
            if cmd[1] == "cd":
                p = cmd[2]
                if p == "..": pwd = pwd[:-1]
                elif p == "/": pwd = []
                else: pwd.append(p)
                vprint(2, pwd)
                makedir(tree, pwd)
            elif cmd[1] == "ls":
                pass
            else:
                print(f"UNKNOWN COMMAND: '{line}'")
                assert(false)
        else:
            f = [x.strip() for x in line.split(" ")]
            t = f[0]
            name = f[1]
            if t == "dir":
                makedir(tree, pwd + [name])
            else:
                size = int(t)
                addfile(tree, pwd, name, size)

    sumdir(tree)
    vprint(2, tree)
    return tree

def part1(input):
    tree = parse(input)

    l = findsmaller("/", tree, 100000)
    sum = 0
    for (k, v) in l:
        vprint(2, k, v)
        sum += v
    
    return sum

def part2(input):
    tree = parse(input)

    totalsize = tree[SUM]

    spaceneeded = totalsize - (70000000 - 30000000)

    vprint(1, "Total FS usage:", totalsize)
    vprint(1, "Space needed:", spaceneeded)

    l = list(findlarger("/", tree, spaceneeded))
    l.sort(key=lambda t: t[1])
    vprint(1, l)

    return l[0][1]

if tests:

    success = True

    def splitLines(input):
        return [x.strip() for x in input.split("\n")]

    for case in test_cases:
        input = splitLines(case["input"])
        if run1:
            output = part1(input)
            if output != case["output"]:
                print(f"Test part 1failed for input:\n====\n{case['input'].strip()}\n====\n.\n\nGot:\n{output}\n\nExpected:\n{case['output']}\n")
                success = False

        if run2 and "output2" in case and case["output2"] is not None:
            output = part2(input)
            if output != case["output2"]:
                print(f"Test part 2 failed for input:\n====\n{case['input'].strip()}\n====\nGot:\n{output}\n\nExpected:\n{case['output2']}\n")
                success = False

    if success:
        print("All tests passed successfully!")

else:
    try:
        fp = open(input_file, "r")
    except FileNotFoundError:
        print("Input file not found, using stdin")
        fp = sys.stdin
    
    input = [x.strip() for x in fp.readlines()]

    if run1:
        print("PART 1")
        print("======")
        print(part1(input))

    if run1 and run2:
        print()

    if run2:
        print("PART 2")
        print("======")
        print(part2(input))