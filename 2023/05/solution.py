import functools
import itertools
import collections
from queue import PriorityQueue
import heapq
from dataclasses import dataclass
import math
import re
import sys
from typing import List, Union, Tuple


@dataclass(frozen=True, order=True)
class MapItem:
    source: int
    dest: int
    len: int

    def inRange(self, x: int) -> bool:
        return x >= self.source and x < self.source + self.len
    
    def map(self, x: int) -> int:
        return x - self.source + self.dest
    
    #How many more input values are covered by this range?
    def covered(self, x: int) -> int:
        return self.source + self.len - x

    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.dest} {self.source} {self.len} ({self.source} -> {self.source+self.len-1})"
    

class Mapper:
    map: List[MapItem]
    name: str

    def __init__(self, name) -> None:
        self.map = []
        self.name = name

    def remap(self, x: int) -> int:
        for m in self.map:
            if m.inRange(x):
                return m.map(x)
            
        #No match found
        return x
    
    def remapCover(self, x: int) -> Tuple[int, Union[int, None]]:
        for m in self.map:
            if m.inRange(x):
                return (m.map(x), m.covered(x))
            
        #No match found
        #Find next possible map that fits
        minNext = None
        for m in self.map:
            if x < m.source:
                if minNext is None or m.source < minNext:
                    minNext = m.source-x

        return x, minNext

    def __repr__(self):
        return str(self)

    def __str__(self):
        res = [f"{self.name} map:"]
        for m in self.map:
            res.append(str(m))

        return "\n".join(res) + "\n"
    
@dataclass(frozen=True)
class Range:
    start: int
    end: int

    def inRange(self, x) -> bool:
        return x>=self.start and x<=self.end
    
    
def pruneRange(orig: Range, x: Range) -> Union[Range, None]:
    #Range is entirely covered?

    if orig.inRange(x.start) and orig.inRange(x.end):
        return None
    
    #Range is entirely outside?
    if x.start > orig.end or x.end < orig.start:
        return x
    
    #Starts inside
    if orig.inRange(x.start):
        return Range(orig.end+1, x.end)

    #Starts inside
    if orig.inRange(x.end):
        return Range(x.start, orig.start-1)




def parse(input: list[str]) -> Tuple[List[int], List[Mapper]]:
    #Parse input
    input = input.copy()

    #First line is seeds
    line = input.pop(0)

    seedlist = line.split(":")[1].strip()
    seeds = [int(x) for x in seedlist.split()]

    #Blank space baby
    input.pop(0)

    maps: List[Mapper] = []

    #Make sure there's a blank line at the end to not trip things up
    if len(input[-1]) > 0:
        input.append("")

    while len(input) > 0:
        name = input.pop(0).split(" ")[0]
        print(name)
        mapper = Mapper(name)

        line = input.pop(0).strip()
        while len(line) > 0:
            (dest, src, length) = line.split()
            m = MapItem(int(src), int(dest), int(length))
            mapper.map.append(m)

            line = input.pop(0).strip()

        maps.append(mapper)

    return (seeds, maps)

def part1(input: list[str]):
    (seeds, maps) = parse(input)
    locations = []

    for seed in seeds:
        val = seed
        for mapper in maps:
            val = mapper.remap(val)

        locations.append(val)

    print(locations)
    return min(locations)

def part2(input: list[str]):
    (seeds, maps) = parse(input)
    
    if len(seeds)%2 != 0:
        print("DANGER! Odd number of seeds!")

    minloc = None

    while len(seeds) > 0:
        seed1 = seeds.pop(0)
        seed2 = seeds.pop(0) + seed1 - 1

        print()
        print(f"Doing range {seed1} to {seed2}")

        seed = seed1
        while seed is not None:

            val = seed
            skips = []
            for mapper in maps:
                (val, skip) = mapper.remapCover(val)
                skips.append(skip)

            print(f"Doing seed {seed} got location {val}")

            if minloc is None or val < minloc:
                print(f"Best seed {seed} loc {val}")
                minloc = val
                bestseed = seed

            if seed == seed2:
                #Last seed in range
                break

            #print(skips)

            skips = [x for x in skips if x is not None]

            if len(skips) == 0:
                print(f"No more skips at seed {seed}, done with range? **************************")
                seed = None
            else:
                skippy = min(skips)

                if skippy <= 0:
                    print("PANIC")
                    print(skips)
                    sys.exit(1)

                #Some range ends here, still go one step
                if skippy == 0:
                    skippy = 1

                #Don't go past end of range
                seed = min(seed + skippy, seed2)

                print(f"Skipping {skippy} to {seed}")

            #seenseeds.add(seed)

    print(f"Best location {minloc} with seed {bestseed}")

    return minloc
