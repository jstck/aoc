import functools
import itertools
import collections
from queue import PriorityQueue
import heapq
from dataclasses import dataclass, field
import math
import re
import sys
from typing import List



def handkey(cards : str) -> str:
    #Replace (A, K, Q, J, T) with (e, d, c, 0, a) for correct sorting (J=low joker)
    repl = {
        "A": "e",
        "K": "d",
        "Q": "c",
        "J": "0",
        "T": "a"
    }

    for i, j in repl.items():
        cards = cards.replace(i, j)

    return cards

def score_plain(cards: str) -> int:
    cards = cards.strip()
    a = list(cards)
    a.sort()


    #Five of a kind
    if a[0] == a[4]:
        return 6
    #Four of a kind
    if a[0] == a[3] or a[1] == a[4]:
        return 5
    
    #Full house
    if (a[0] == a[2] and a[3] == a[4]) or (a[0] == a[1] and a[2]==a[4]):
        return 4
    
    #Three of a kind
    if a[0] == a[2] or a[1] == a[3] or a[2] == a[4]:
        return 3
    
    #Two pair
    for i in range(5):
        a1 = a.copy()
        del a1[i]
        if a1[0] == a1[1] and a1[2] == a1[3]:
            return 2
        
    #One pair
    for i in range(4):
        if a[i] == a[i+1]:
            return 1

    #NOTHING!
    return 0

def score(cards: str) -> str:
    #All "normal" cards
    allcards = list("23456789TQKA")

    key = handkey(cards)
    #Score regular hands as regular
    if not "J" in cards:
        return f"{score_plain(cards)}.{key}"
    
    normalcards = [x for x in list(cards) if x != "J"]

    njokers = 5 - len(normalcards)

    #Special cases for 5 or 4 jokers (always five-of-a-kind)
    if njokers == 5:
        return "6.00000"
    
    if njokers == 4:
        return "6." + key
    
    if njokers == 1:
        best = 0
        for j1 in normalcards:
            newhand = normalcards + [j1]
            s = score_plain("".join(newhand))
            best = max(best, s)

        return f"{best}.{key}"
    
    if njokers == 2:
        best = 0
        for j1 in normalcards:
            for j2 in normalcards:
                newhand = normalcards + [j1, j2]
                s = score_plain("".join(newhand))
                best = max(best, s)

        return f"{best}.{key}"

    if njokers == 3:
        best = 0
        for j1 in normalcards:
            for j2 in normalcards:
                for j3 in normalcards:
                    newhand = normalcards + [j1, j2, j3]
                    s = score_plain("".join(newhand))
                    best = max(best, s)

        return f"{best}.{key}" 

    return "X." + key

@dataclass(order=True)
class Hand:
    sort_index: str = field(init=False)
    cards: str
    bet: int
 
    def __post_init__(self):
        self.sort_index = score(self.cards)

    def __repr__(self):
        stuff = list(self.cards)
        stuff.sort()
        return f"{self.cards:5}  {self.bet:3}  {self.sort_index} {''.join(stuff)}"

def part2(input: list[str]):
    hands: List[Hand] = []
    for row in input:
        (cards, bet) = row.split()
        cards = cards.strip()
        bet = int(bet.strip())

        hand = Hand(cards=cards, bet=bet)

        hands.append(hand)

    hands.sort()
    #hands.reverse()

    total = 0

    for i, hand in enumerate(hands):
        rank = i+1

        print(f"{rank:4} {hand}")

        total += rank * hand.bet


    return total
