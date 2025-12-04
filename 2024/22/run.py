#!/usr/bin/env python3

import functools
from functools import cache
from itertools import combinations
import itertools
import collections
from queue import PriorityQueue
import heapq
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Union, Optional, Iterator

import math
import re
import sys


sys.path.append("../..")
from lib.aoc import *

def part1(input: list[str]):
    return ""

def part2(input: list[str]):
    return ""

def newsecret(secret: int) -> int:
    x = ((secret * 64) ^ secret) % 16777216
    x = (( x // 32) ^ x) % 16777216
    x = (( x * 2048) ^ x) % 16777216

    return x

def secret2000(secret: int) -> int:
    for _ in range(2000):
        secret = newsecret(secret)
    return secret

def pricesequence(secret: int) -> Iterator[int]:
    yield secret % 10
    count = 0
    while count < 2000:
        count += 1
        secret = newsecret(secret)
        yield secret%10

def bananasequence(secret: int) -> Iterator[tuple[int, int]]:
    #First one has no change, return something bananas
    yield (secret%10, 17)
    oldprice = secret%10
    count = 0
    while count < 2000:
        count += 1
        secret = newsecret(secret)
        newprice = secret % 10
        yield (newprice, newprice-oldprice)
        oldprice=newprice

#Make all valid sequences of length 4
def generatesequences() -> Iterator[list[int]]:
    for x1 in range(-9,10):
        for x2 in range(-9,10):
            #Discard any sequences that would take price outside 0-9 (sum is outside -9 - +9)
            s2 = x1+x2
            if s2<-9 or s2>9: continue

            for x3 in range(-9,10):
                s3 = s2 + x3
                if s3<-9 or s3>9: continue
            
                for x4 in range(-9,10):
                    s4 = s3 + x4
                    if s4<-9 or s4>9: continue
            
                    yield [x1,x2,x3,x4]

def findsequence(secret: int, sequence: list[int]) -> int:

    seqlen = len(sequence)
    buf = []
    for price, change in bananasequence(secret):
        buf.append(change)
        if buf[-seqlen:] == sequence:
            #print("Found at price", price)
            return price

    #Didn't sell anything
    #print("Did not find", sequence, "with secret", secret)
    return 0

if __name__ == "__main__":
    input = readinput()

    sum1 = 0
    sum2 = 0

    secrets = []

    allprices = {}
    allchanges = {}
    #Cache of first occurence of all sequences of changes for a secret
    sequencecache: dict[int,dict[tuple[int,int,int,int],int]] = {}

    for i in input:
        secret = int(i)
        sum1 += secret2000(secret)

        #Save stuff for part 2
        secrets.append(secret)
        prices, changes = zip(*bananasequence(secret))
        allprices[secret] = prices
        allchanges[secret] = changes
        sequencecache[secret] = {}
        for i in range(5,len(changes)):
            seq = tuple(changes[i-4:i])
            if seq not in sequencecache[secret]:
                sequencecache[secret][seq] = i

    print("Part 1:", sum1)

    allsequences = [tuple(s) for s in generatesequences()]
    print("There are", len(allsequences), "sequences")

    best = -1

    c = 0
    #allsequences = [(-2,1,-1,3)]
    for seq in allsequences:
        c += 1
        if c % 100 == 0:
            print(c, seq)
            pass
        
        bananas = 0
        for secret in secrets:
            if seq in sequencecache[secret]:
                pos = sequencecache[secret][seq]
                price = allprices[secret][pos-1]
                #print(f"Secret {secret} price {price} at pos {pos}")
                bananas += price

        if bananas > best:
            print("New best sequence", seq, "gives", bananas, "bananas")
            best = bananas
    
    #1799: too low!
    print("Part 2:", best)