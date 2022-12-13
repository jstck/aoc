#!/usr/bin/env python3

import sys
import argparse
import re
import functools
import math

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
        "input": "FILE:sample.txt",
        "output": 71,
        "output2": None #No value given
    }
]

def parse(input):
    c = chunks(input)

    intervals = {}

    for row in c[0]:
        matches = re.match(r"^([a-z ]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$", row)
        label = matches.group(1)
        start1 = int(matches.group(2))
        end1 = int(matches.group(3))
        start2 = int(matches.group(4))
        end2 = int(matches.group(5))

        assert(label not in intervals)

        intervals[label] = ((start1, end1), (start2, end2))

    myticket = [int(x) for x in c[1][1].split(",")]

    tickets = []

    for row in c[2][1:]:
        ticket = [int(x) for x in row.split(",")]
        tickets.append(ticket)

    return(intervals, myticket, tickets)

def findValue(val, ranges):
    for (a, b) in ranges:
        if val >= a and val <= b:
            return True
    return False

def validateTicket(ticket, ranges):
    for val in ticket:
        if not findValue(val, ranges):
            return False
    return True

def matchTicket(ticket, intervals):
    candidates_labels = {}
    candidates_fields = {}

    for (label, ints) in intervals.items():
        for (i, val) in enumerate(ticket):
            if findValue(val, ints):
                #A candidate
                if not label in candidates_labels:
                    candidates_labels[label] = set()
                candidates_labels[label].add(i)

                if not i in candidates_fields:
                    candidates_fields[i] = set()
                candidates_fields[i].add(label)


    all_fields = range(len(ticket))

    for l in intervals.keys():
        if not l in candidates_labels:
            print(f"{l} not matched")
        if len(candidates_labels[l])==1:
            print(f"Only one candidate for {l}")
    for f in all_fields:
        if not f in candidates_fields:
            print(f"Field {f:3} not matched")
        if len(candidates_fields[f])==1:
            print(f"Only one candidate for {f}")

    return (candidates_labels, candidates_fields)


def intersect_tickets(t1, t2):
    labels = {}
    fields = {}
    
    (labels1, fields1) = t1
    (labels2, fields2) = t2

    for label in labels1.keys():
        s1 = labels1[label]
        s2 = labels2[label]

        s = s1 & s2
        labels[label] = s

    for field in fields1.keys():
        s1 = fields1[field]
        s2 = fields2[field]

        s = s1 & s2
        fields[field] = s

    return (labels, fields)


def part1(input):
    (intervals, myticket, tickets) = parse(input)

    allranges = []
    for interval_list in intervals.values():
        allranges.extend(interval_list)

    allticketvalues = []
    for ticket in tickets:
        allticketvalues.extend(ticket)

    error = 0
    for val in allticketvalues:
        if not findValue(val, allranges):
            error += val

    return error


def part2(input):
    (intervals, myticket, tickets) = parse(input)

    #All ranges, for filtering invalid tickets
    allranges = []
    for interval_list in intervals.values():
        allranges.extend(interval_list)

    validtickets = [t for t in tickets if validateTicket(t, allranges)]

    print(f"{len(validtickets)}/{len(tickets)} valid tickets")

    ticket_fields = []

    for ticket in validtickets:
        (labels, fields) = matchTicket(ticket, intervals)
        ticket_fields.append((labels, fields))
        #print(fields)

    intersection = functools.reduce(intersect_tickets, ticket_fields)

    (labels, fields) = intersection

    known_labels = {}
    

    hit = True
    while hit:
        hit = False

        #Find labels with only one field
        for (label, fields) in labels.items():
            if fields is None or len(fields)==0:
                continue
            if len(fields) == 1:
                hit = True
                single_field = fields.pop()
                known_labels[label] = single_field

                #Remove this field from all other labels
                for fields in labels.values():
                    fields.discard(single_field)

        #Could do the inverse as well (find fields with only one label), but it seems not needed

    d_labels = [x for x in known_labels.keys() if x.startswith("departure ")]
    print(d_labels)
    d_values = [myticket[known_labels[l]] for l in d_labels]
    print(d_values)

    return math.prod(d_values)




def fixInput(raw):
    lines = [x.strip() for x in raw.split("\n")]

    #Remove trailing blank lines
    while len(lines[-1]):
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