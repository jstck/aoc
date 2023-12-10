#!/usr/bin/env python3

import sys
from typing import List, Tuple, Set

def parse(input: List[str]) -> Tuple[List[int],List[int]]:

    input = [x.strip() for x in input if len(x.strip())>0]
    size = len(input)//2

    player1 = [int(x) for x in input[1:size] ]
    player2 = [int(x) for x in input[size+1:]]

    assert(len(player1)==len(player2))

    return (player1, player2)


def play(player1: List[int], player2: List[int], recurse=False) -> Tuple[List[int],List[int]]:

    seengames: Set[Tuple[Tuple[int, ...], Tuple[int, ...]]] = set()

    while len(player1)>0 and len(player2)>0:

        p1 = player1[0]
        p2 = player2[0]

        fingerprint = (tuple(player1), tuple(player2))
        if fingerprint in seengames:
            #print("Infinity-forfeiting game:", player1, player2)
            #Score player1 win
            player1 = player1[1:] + [p1, p2]
            player2 = player2[1:]
            continue

        seengames.add(fingerprint)

        player1 = player1[1:]
        player2 = player2[1:]

        l1 = len(player1)
        l2 = len(player2)

        if recurse and p1 <= l1 and p2 <= l2:
            rp1 = player1[0:p1]
            rp2 = player2[0:p2]
            #print("Recursing", rp1, rp2)
            (r1, r2) = play(rp1, rp2, True)
            if len(r1) > 0:
                #print("P1 wins")
                player1 = player1 + [p1, p2]
            elif len(r2) > 0:
                #print("P2 wins")
                player2 = player2 + [p2, p1]
            else:
                print("NO CARDS LEFT, WHAT HAPPEN?")
                sys.exit(1)
        
        elif p1>p2:
            #print("P1 wins")
            player1 = player1 + [p1, p2]
        elif p2>p1:
            #print("P2 wins")
            player2 = player2 + [p2, p1]
        else:
            print("A DRAW WHAT HAPPEN?")
            sys.exit(1)

    return (player1, player2)


def score(player1: List[int], player2: List[int]) -> int:
    winninghand = player1 + player2
    winninghand.reverse()

    sum = 0
    for i, x in enumerate(winninghand):
        sum += (i+1)*x

    return sum



if __name__ == "__main__":
    (player1, player2) = parse(sys.stdin.readlines())

    (p1, p2) = play(player1, player2)
    
    part1 = score(p1, p2)

    print("Part 1:", part1)
    print()

    (p1, p2) = play(player1, player2, True)

    part2 = score(p1, p2)

    print("Part 2:", part2)
