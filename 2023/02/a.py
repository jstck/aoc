#!/usr/bin/env python3


example = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


max = {"red": 12, "green": 13, "blue": 14}



import sys
import re


def gamepossible(game):
    (meta, lista) = game.strip().split(":")
    delar = re.split('\s*,|;\s*', lista)
    for c in delar:
        c = c.strip()
        b = c.split(" ")
        count = int(b[0])
        color= b[1]
        if count > max[color]:
            return 0
        
    #Returnera game id
    id = int(meta.strip().split(" ")[1])
    return id

#data = example.strip().split("\n")
with open("input.txt", "r") as fp:
    data = fp.readlines()
    
possible = 0

for line in data:
    possible += gamepossible(line)

print(possible)