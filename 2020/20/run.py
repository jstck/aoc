#!/usr/bin/env python3

import sys
import argparse
import re

verbosity: int = 0


test_cases = [
    {
        "input": "FILE:sample.txt",
        "output": 20899048083289,
        "output2": 273
    }
]

#Print controlled by verbosity level
def vprint(*args) -> None:
    if args[0]<= verbosity:
        print(*args[1:])

def chunks(input: list[str], ints: bool=False) -> list[list[str]]:
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


def part1(input: list[str]):
    import solution
    return solution.part1(input)

def part2(p1_solution):
    import solution
    return solution.part2(p1_solution)

def fixInput(raw: str) -> list[str]:
    lines = [x.strip() for x in raw.split("\n")]

    #Remove trailing blank lines
    while len(lines)>0 and len(lines[-1])==0:
        lines.pop()
    return lines

def failMsg(name: str, input: str, expected: str, output: str):
    print(f"""Test {name} failed for input:
==== Input:
{input.strip()}
==== Expected:
{expected.strip()}
==== Got:
{output.strip()}
""", file=sys.stderr)


if __name__ == "__main__":
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
    if run2: run1 = True #Need part 1 for part 2
    verbosity = vars(args)["verbose"]
    input_file = vars(args)["input_file"]

    if tests:

        success = True

        for case in test_cases:
            rawinput = case["input"]

            match = re.search(r'^FILE:([\S]+)$', rawinput.strip())
            if match:
                filename = match.group(1)
                print("Loading", filename)
                with open(filename, "r") as fp:
                    rawinput = fp.read()

            input = fixInput(rawinput)
            
            p1_solution = None
            if run1 and "output" in case and case["output"] is not None:
                (output, p1_solution) = part1(input)
                if output != case["output"]:
                    failMsg("part1", str(case['input']), str(case['output']), str(output))
                    success = False

            if run2 and "output2" in case and case["output2"] is not None:
                output = part2(p1_solution)
                if output != case["output2"]:
                    failMsg("part2", str(case['input']), str(case['output2']), str(output))
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

        solution1 = None
        if run1:
            print("PART 1")
            (result1, solution1) = part1(input)
            print("======")
            print(result1)

        if run1 and run2:
            print()

        if run2:
            print("PART 2")
            result2 = part2(solution1)
            print("======")
            print(result2)