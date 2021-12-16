#!/usr/bin/env python3

import sys
import argparse
import re
from functools import reduce

match = re.search(r'aoc/?(\d+)/(\d+)', __file__)
if match:
    descr = "Advent of Code " + match.group(1) + ":" + match.group(2)
else:
    descr = "Advent of some kind of Code"

parser = argparse.ArgumentParser(description = descr)

parser.add_argument('-1', action='store_true', help="Do part 1")
parser.add_argument('-2', action='store_true', help="Do part 2")
parser.add_argument('--verbose', '-v', action='count', default=0, help="Increase verbosity")

args = parser.parse_args()

part2 = vars(args)["2"]
part1 = vars(args)["1"] or not part2 #Do part 1 if not part 2 specified
verbosity = vars(args)["verbose"]

#Print controlled by verbosity level
def vprint(*args):
    if args[0]<= verbosity:
        print(*args[1:])


#unencode bit list to int
def uncode(bits):
    return int(''.join([str(b) for b in bits]),2)

def bstr(bits):
    return "".join([str(b) for b in bits])

def dprint(*args):
    if verbosity<2:
        return
    p = "--" * int(args[0])
    print(p,*args[1:])

def boolbit(bool):
    if bool:
        return 1
    else:
        return 0

version_sum = 0

def decode(bits, depth=0):
    global version_sum

    dprint(depth, bstr(bits))
    if(len(bits)<8):
        #print less than 8 bits at the end can only be filler, right?
        dprint(depth,"Discarded end filler:", bstr(bits))
        return (0, [])

    version = uncode(bits[0:3])
    version_sum += version
    typeid = uncode(bits[3:6])

    dprint(depth,"Ver:", version, "Type:", typeid)

    if typeid == 4: #Literal
        cont = True
        pos = 6
        val = []
        while cont:
            chunk = bits[pos:pos+5]
            cont = (chunk[0] == 1)
            val += chunk[1:]
            pos+=5    
        
        val = uncode(val)
        dprint(depth, "Literal", val, "bits used", pos)

        return (val, bits[pos:])

    else: #Operator
        length_typeid = uncode(bits[6:7])

        values = []

        rest = []

        if length_typeid == 0:  #15 bits length of subpackets
            length = uncode(bits[7:7+15])
            subpackets = bits[22:22+length]
            dprint(depth,"Operator, %d bits subpackets:" % (length), bstr(subpackets))

            rest = bits[22+length:]
            while len(subpackets) > 0:
                (v, subpackets) = decode(subpackets, depth+1)
                values.append(v)
            
        else:                   #11 bits number of subpackets
            packets = uncode(bits[7:7+11])
            rest = bits[18:]
            dprint(depth,"Operator, %d subpackets:" % (packets), bstr(rest))
            for p in range(packets):
                dprint(depth, "Subpacket",p)
                (v, rest) = decode(rest, depth+1)
                values.append(v)

        if typeid == 0: #SUM
            result = sum(values)
        elif typeid == 1: #PRODUCT
            result = reduce(lambda a,b: a*b, values)
        elif typeid == 2: #MIN
            result = min(values)
        elif typeid == 3: #MAX
            result = max(values)
        elif typeid == 5: #GREATER THAN
            result = boolbit(values[0] > values[1])
        elif typeid == 6: #LESS THAN
            result = boolbit(values[0] < values[1])
        elif typeid == 7: #EQUAL TO
            result = boolbit(values[0] == values[1])


        return (result, rest)

for line in sys.stdin.readlines():
    hex = line.strip()

    vprint(1, hex)
    bitstring = bin(int(hex,16))[2:]
    
    #Pad bit string with leading 0's
    pad = "0" * (len(hex*4)-len(bitstring))
    bitstring = pad + bitstring

    bits = [int(x) for x in bitstring]

    (v, stuff ) = decode(bits)
    print("RESULT:",v)
    print("VERSION SUM:",version_sum)
    print("REMAINING CRAP:", stuff)
    print()

# input = [l.strip() for l in sys.stdin.readlines()]