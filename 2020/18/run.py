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
        "input": "1 + 2 * 3 + 4 * 5 + 6",
        "output": 71,
        "output2": 231
    },
    {
        "input": "1 + (2 * 3) + (4 * (5 + 6))",
        "output": 51,
        "output2": 51
    },
    {
        "input": "2 * 3 + (4 * 5)",
        "output": 26,
        "output2": 46
    },
    {
        "input": "5 + (8 * 3 + 9 + 3 * 4 * 3)",
        "output": 437,
        "output2": 1445
    },
    {
        "input": """
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
""",
        "output": 12240+13632,
        "output2": 669060+23340
    },
]

def evaluate(expr):

    for (i, e) in enumerate(expr):

        #Evaluate all subexpressions recursively
        if isinstance(e,list):
            sub = evaluate(e)
            expr[i] = sub

    s = " ".join([str(i) for i in expr])

    while len(expr)>1:
        for i in range(1, len(expr)-1):
            if expr[i] == '+':
                r = expr[i-1] + expr[i+1]
                expr = expr[:i-1] + [r] + expr[i+2:]
                break
            if expr[i] == '*':
                r = expr[i-1] * expr[i+1]
                expr = expr[:i-1] + [r] + expr[i+2:]
                break
    return expr[0]


def evaluate2(expr):

    for (i, e) in enumerate(expr):

        #Evaluate all subexpressions recursively
        if isinstance(e,list):
            sub = evaluate2(e)
            expr[i] = sub

    s = " ".join([str(i) for i in expr])

    #All additions
    dostuff = True
    while dostuff:
        dostuff = False
        for i in range(1, len(expr)-1):
            if expr[i] == '+':
                r = expr[i-1] + expr[i+1]
                expr = expr[:i-1] + [r] + expr[i+2:]
                dostuff = True
                break



    #All multiplications
    while len(expr)>1:
        for i in range(1, len(expr)-1):
            if expr[i] == '*':
                r = expr[i-1] * expr[i+1]
                expr = expr[:i-1] + [r] + expr[i+2:]
                break
    return expr[0]

def tokenize(text):
    #turn parens into brackets
    text = text.replace('(', '[').replace(')', ']')
    #quote operators
    text = text.replace('+', '"+"').replace('*','"*"')
    #put commas between shit
    text = text.replace(' ',',')
    #Make it a list
    text = "[" + text + "]"
    expr = eval(text)
    return expr
    

def part1(input):
    sum=0
    for line in input:
        expr = tokenize(line)
        r = evaluate(expr)
        sum += r

        print(line, " => ", r)

    return sum

def part2(input):
    sum=0
    for line in input:
        expr = tokenize(line)
        r = evaluate2(expr)
        sum += r

        print(line, " => ", r)

    return sum



def fixInput(raw):
    lines = [x.strip() for x in raw.strip().split("\n")]

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