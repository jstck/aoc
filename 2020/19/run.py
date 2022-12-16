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
        "input": """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb""",
        "output": 2,
        "output2": None
    }
]

def fixtoken(t):
    try:
        x = int(t)
        return x
    except ValueError:
        pass

    if t == "|":
        return t

    #Should be a letter
    assert(len(t)==3)
    return t[1]

def parse(input) -> tuple[list, list]:
    rules = {}
    messages = []

    c = chunks(input)

    for line in c[0]:
        (num,rule) = [p.strip() for p in line.split(":")]
        num = int(num)
        rule = [fixtoken(t) for t in rule.split(" ")]
        rules[num] = rule

    messages = c[1]

    return (rules, messages)


def transmogrify(rules: list, i: int, part2: bool) -> str:

    if part2:
        if i==8:
            return transmogrify(rules, 42, part2) + "+"

        elif i==11:
            return transmogrify(rules, 42, part2) + "+"

    rule = rules[i]
    result = ""

    wrap = False
    for r in rule:
        if isinstance(r, int):
            result += transmogrify(rules, r, part2)
        elif r == "|":
            result += "|"
            wrap = True
        else:
            #String literal
            result += r
    if wrap or len(rule)>1:
        result = "(" + result + ")"

    return result



def part1(input, part2=False):
    rules, messages = parse(input)

    count = 0

    regexp_str = "^" + transmogrify(rules, 0, part2) + "$"

    print(regexp_str)

    regexp = re.compile(regexp_str)

    for message in messages:
        if regexp.match(message):
            print("Match:   ", message)
            count += 1
        else:
            print("No match:", message)

    return count


def part2(input):
    return part1(input, True)



def fixInput(raw):
    lines = [x.strip() for x in raw.split("\n")]

    #Remove trailing blank lines
    while len(lines[-1])==0:
        lines.pop()
    return lines

if tests:

    success = True

    def splitLines(input):
        return 

    for case in test_cases:
        rawinput = case["input"]

        match = re.search(r'^FILE:([\S]+)$', rawinput.strip())
        if match:
            filename = match.group(1)
            print("Loading", filename)
            with open(filename, "r") as fp:
                rawinput = fp.read()

        input = fixInput(rawinput)
        

        if run1 and "output" in case and case["output"] is not None:
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
    
    input = fixInput(fp.read())

    if run1:
        print("Running part 1")
        result1 = part1(input)
    if run2:
        print("Running part 2")
        result2 = part2(input)

    print()

    if run1:
        print("PART 1")
        print("======")
        print(result1)

    if run1 and run2:
        print()

    if run2:
        print("PART 2")
        print("======")
        print(result2)