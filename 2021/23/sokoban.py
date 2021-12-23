#!/usr/bin/env python3

import sys
import argparse
import re
import queue

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

finish = """
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
"""

sample_start = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""

start = """
#############
#...........#
###C#A#B#D###
  #B#A#D#C#
  #########
"""

#spelplanen har 14 olika giltiga positioner:

#############
#01.2.3.4.56#
###7#9#b#d###
  #8#a#c#e#
  #########


#Giltiga drag mellan positioner, och kostnaden för dem
forwardmoves = [
    (0,1,1), #Längs överkanten
    (1,2,2),
    (2,3,2),
    (3,4,2),
    (4,5,2),
    (5,6,1),
    (1,7,2),  #Ner i rum A
    (2,7,2),
    (7,8,1),
    (2,9,2),  #Ner i rum B
    (3,9,2),
    (9,10,1),
    (3,11,2),  #Ner i rum C
    (4,11,2),
    (11,12,1),
    (4,13,2),  #Ner i rum D
    (5,13,2),
    (13,14,1),        
]

reversemoves = [(b,a,c) for (a,b,c) in forwardmoves]

#Sets of positions where certain creatures are banned
banlist = {
    'A': frozenset((9,10,11,12,13,14)),
    'B': frozenset((7,8,11,12,13,14)),
    'C': frozenset((7,8,9,10,13,14)),
    'D': frozenset((7,8,9,10,11,12)),
}

allmoves = forwardmoves+reversemoves

visited = set()


class Board:

    def char2piece(c):
        if c in ['A','B','C','D']:
            return c
        return None

    def __str2pos__(text):
        lines = [line.strip() for line in text.strip().split()]

        pos = [None] * 15
        pos[0]  = lines[1][1]
        pos[1]  = lines[1][2]
        pos[2]  = lines[1][4]
        pos[3]  = lines[1][6]
        pos[4]  = lines[1][8]
        pos[5]  = lines[1][10]
        pos[6]  = lines[1][11]
        pos[7]  = lines[2][3]
        pos[8]  = lines[3][1]
        pos[9]  = lines[2][5]
        pos[10] = lines[3][3]
        pos[11] = lines[2][7]
        pos[12] = lines[3][5]
        pos[13] = lines[2][9]
        pos[14] = lines[3][7]

        return tuple([c if c in ['A','B','C','D'] else '.' for c in pos])


    def __init__(self, pos, parent=None):
        self.parent = parent
        if isinstance(pos, tuple):
            self.pos = pos
        elif isinstance(pos,str):
            self.pos = Board.__str2pos__(pos)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.pos == other.pos
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.pos < other.pos
    def __le__(self, other):
        return self.pos <= other.pos
    def __gt__(self, other):
        return self.pos > other.pos
    def __ge__(self, other):
        return self.pos >= other.pos

    def __hash__(self):
        return hash(self.pos)
        if self.parent is None:
            return hash(self.pos)
        else:
            return hash(self.pos) ^ hash(self.parent.pos)

    def __repr__(self):
        return 'cave{'+''.join(['.' if c is None else c for c in self.pos]) + '}'

    def __str__(self):
        return """#############
#{0[0]}{0[1]}.{0[2]}.{0[3]}.{0[4]}.{0[5]}{0[6]}#
###{0[7]}#{0[9]}#{0[11]}#{0[13]}###
  #{0[8]}#{0[10]}#{0[12]}#{0[14]}#
  #########""".format(tuple(['.' if c is None else c for c in self.pos]))

    def makemoves(self):
        #Find all moves where "from" is occupied and "to" is empty
        #moves = [move for move in allmoves if self.pos[move[0]] is not None and self.pos[move[1]] is None]
        
        for (p0,p1,cost) in allmoves:
            
            if self.pos[p0] == '.': continue #"From" is empty

            if self.pos[p1] != '.': continue #"To" is occupied
            creature = self.pos[p0]
            if p1 in banlist[creature]:
                if p0 not in banlist[creature]:
                    continue #Going into a banned room
                if p1 > p0:
                    continue #Going downwards within a banned room

            newpos = list(self.pos)
            newpos[p0] = '.'
            newpos[p1] = creature

            if creature == 'B':
                cost *= 10
            elif creature == 'C':
                cost *= 100
            elif creature == 'D':
                cost *= 1000

            newboard = Board(tuple(newpos), self)
            if newboard in visited:
                continue
            
            yield (cost, newboard)





q = queue.PriorityQueue()

startpos = Board(start)
endpos = Board(finish)
distances = {}

q.put((0, Board(sample_start)))

end = Board(finish)

while not q.empty():
    (cost, pos) = q.get()
    if pos in visited:
        continue #Already been here through some better means

    distances[pos]=cost
    visited.add(pos)

    if pos == endpos:
        lista = []
        p = pos
        while p is not None:
            lista.append(p)
            p = p.parent
        lista.reverse()

        for p in lista:
            print(p,distances[p])

        
        print("FINISHED!", cost)
        break

    for (nextcost, nextpos) in pos.makemoves():
        if nextpos not in visited:
            q.put((cost + nextcost, nextpos))