#!/usr/bin/env python3


example = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""






import sys
import re


def gamepower(game):
    max = {"red": 0, "green": 0, "blue": 0}
    (meta, lista) = game.strip().split(":")
    delar = re.split('\s*,|;\s*', lista)
    for c in delar:
        c = c.strip()
        b = c.split(" ")
        count = int(b[0])
        color= b[1]
        if count > max[color]:
            max[color] = count
        
    #Returnera game id
    id = int(meta.strip().split(" ")[1])

    power = max["red"] * max["green"] * max["blue"]
    return id, power

data = example.strip().split("\n")
#with open("input.txt", "r") as fp:
#    data = fp.readlines()
    
totalpower = 0

for line in data:
    id, power = gamepower(line)
    print(id, power)
    totalpower += power

print(totalpower)