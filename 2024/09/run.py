#!/usr/bin/env python3

import functools
from functools import cache
from itertools import combinations
import itertools
import collections
from queue import PriorityQueue
import heapq
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Union, Optional
from collections.abc import Iterator

import math
import re
import sys


sys.path.append("../..")
from lib.aoc import *


def filemap(stuff: list[int]) -> tuple[dict[int,tuple[int,int]],list[tuple[int,int]]]:
    map = {}
    space = []
    pos = 0
    fileid = 0
    for file, free in zip(stuff[::2], stuff[1::2]):
        map[fileid] = (pos,file)
        if free > 0: space.append((pos+file, free))
        pos += file + free
        fileid += 1

    return map, space

def blockmap(stuff: list[int]) -> Iterator[int]:
    fileid = 0
    for file, free in zip(stuff[::2], stuff[1::2]):
        for _ in range(file):
            yield fileid
        for _ in range(free):
            yield -1
        fileid += 1

def compact(blocks_in: list[int]) -> list[int]:
    blocks = blocks_in[:] #Make a copy to mutilate
    pos = 0
    tail = len(blocks)-1
    while True:
        #print("Boop", pos, tail)
        #Skip ahead until there's a free block
        while blocks[pos]>=0:
            pos += 1
            if pos >= tail:
                #We have met in the middle, this is the compacted result?
                return blocks[:pos+1]

        #Wind back tail until there's a non-free block to move
        while blocks[tail]<0:
            tail -= 1
            if pos >= tail:
                #We have met in the middle, this is the compacted result?
                return blocks[:pos+1]
            
        while blocks[pos]<0 and blocks[tail]>=0:
            blocks[pos] = blocks[tail]
            pos += 1
            tail -= 1
            if pos >= tail:
                #We have met in the middle, this is the compacted result?
                return blocks[:pos+1]
            
        #print("".join([str(c) if c>=0 else "." for c in blocks]))
            

def checksum(blocks: list[int]) -> int:
    sum = 0
    for pos, id in enumerate(blocks):
        if id>=0:
            sum += pos*id
    return sum

def triangle(n: int) -> int:
    if n<= 0: return 0

    return (n*(n+1))//2

def checksum2(filemap: dict[int,tuple[int,int]]) -> int:
    sum = 0

    for fileid, (pos, size) in filemap.items():
        #Instead of summing up each block (it's fileid*position), sum up the blocks of the file and multiply by file id
        #The sum of the "block values" is the triangular number of the last block - triangular number of first-1
        #This works out to the same as firstpos*size*triangular(size)
        #lastblock = pos+size-1
        #blockvalue = triangle(lastblock) - triangle(pos-1)
        blockvalue = pos*size+triangle(size-1)
        sum += fileid*blockvalue
    return sum

def part1(input: list[int]):
    blocks = list(blockmap(input))
    compacted = compact(blocks)
    return checksum(compacted)

def part2(input: list[int]):
    files, freespace = filemap(input)

    #Go through files from the back
    fileids = reversed(sorted(files.keys()))

    for fileid in fileids:
        pos, size = files[fileid]
        #Look for first bit of free space big enough
        for idx, (freepos, freesize) in enumerate(freespace):
            #Can't move file to the right
            if freepos > pos:
                break

            #Gap is too small
            if freesize < size:
                continue

            #Move the file!
            #print(f"Move file {fileid} from {pos} to {freepos}")
            files[fileid] = (freepos, size)
            #Reduce the free space slot (might make it 0 length)
            freespace[idx] = freepos+size, freesize-size
            break



    return checksum2(files)


if __name__ == "__main__":
    input = list(map(int, list(readinput()[0])))

    #Make sure things are "even" (adding "0 free space" at end)
    if len(input)%2 != 0:
        input.append(0)

    p1 = part1(input)
    print("Part 1:", p1)

    p2 = part2(input)
    print("Part 2:", p2)
