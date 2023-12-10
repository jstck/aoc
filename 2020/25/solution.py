#!/usr/bin/env python3

import sys


def findloop(key: int, subject: int) -> int:
    MAXLOOPS = 100_000_000

    loops = 0
    value = 1
    while loops < MAXLOOPS:
        value = (value*subject)%20201227
        loops += 1

        if value == key:
            return loops
        
    print(f"No loop found for key {key} subject {subject}")
    return -1

def transform(subject: int, loops: int) -> int:
    value = 1
    for _ in range(loops):
        value = (value*subject)%20201227

    return value


if __name__ == "__main__":
    input = sys.stdin.readlines()

    card_pub = int(input[0].strip())
    door_pub = int(input[1].strip())

    card_loop = findloop(card_pub, 7)
    print("Card loopsize:", card_loop)

    door_loop = findloop(door_pub, 7)
    print("Door loopsize:", door_loop)

    key1 = transform(door_pub, card_loop)
    key2 = transform(card_pub, door_loop)
    if key1==key2:
        print("Part 1:", key1)
    else:
        print("Different values:", key1, key2)
