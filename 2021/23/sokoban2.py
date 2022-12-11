#!/usr/bin/env python3

import sys
import argparse
import re
import queue
import random

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
  #A#B#C#D#
  #A#B#C#D#
  #########
"""

sample_start = """
#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########
"""

simple_start = """
#############
#...........#
###A#B#C#D###
  #D#C#B#A#
  #A#B#C#D#
  #A#B#C#D#
  #########
"""

start = """
#############
#...........#
###C#A#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #B#A#D#C#
  #########
"""

#spelplanen har 23 olika giltiga positioner:

#############
#01.2.3.4.56#
###7#b#f#j###
  #8#c#g#k#
  #9#d#h#l#
  #a#e#j#m#
  #########


#Giltiga drag mellan positioner, och kostnaden för dem
forwardmoves = [
    (1,7,2),  #Ner i rum A
    (2,7,2),
    (7,8,1),
    (8,9,1),
    (9,10,1),
    (2,11,2),  #Ner i rum B
    (3,11,2),
    (11,12,1),
    (12,13,1),
    (13,14,1),
    (3,15,2),  #Ner i rum C
    (4,15,2),
    (15,16,1),
    (16,17,1),
    (17,18,1),
    (4,19,2),  #Ner i rum D
    (5,19,2),
    (19,20,1),
    (20,21,1),
    (21,22,1),
    (0,1,1), #Längs överkanten
    (1,2,2),
    (2,3,2),
    (3,4,2),
    (4,5,2),
    (5,6,1),
]

reversemoves = [(b,a,c) for (a,b,c) in forwardmoves]

allmoves = forwardmoves+reversemoves

#Sets of positions where certain creatures are banned
banlist = {
    'A': frozenset((11,12,13,14,15,16,17,18,19,20,21,22)),
    'B': frozenset((7,8,9,10,15,16,17,18,19,20,21,22)),
    'C': frozenset((7,8,9,10,11,12,13,14,19,20,21,22)),
    'D': frozenset((7,8,9,10,11,12,13,14,15,16,17,18,)),
}
homes = {
    'A': [7,8,9,10],
    'B': [11,12,13,14],
    'C': [15,16,17,18],
    'D': [19,20,21,22],
}


#Make a list of "full moves". A dict of all nodes, for each node a dict of all other nodes with a tuple of cost and which
#nodes are visited on the way there.
fullmoves = {}
for p0 in range(23):

    mymoves = {p0: (0,[])}

    remaining = [t for t in allmoves]
    hit = True

    while len(remaining)>0 and hit:
        hit = False
        for i in range(len(remaining)-1,-1,-1):
            (z0,z1,c) = remaining[i]

            if z0 in mymoves.keys() and not z1 in mymoves.keys():
                hit=True
                cost = mymoves[z0][0] + c
                if z0==p0:
                    passingby = mymoves[z0][1]
                else:
                    passingby = mymoves[z0][1] + [z0]
                mymoves[z1] = (cost, passingby)
                del remaining[i]
    del mymoves[p0]
    fullmoves[p0] = mymoves


#Make a dict with a list of all neighbouts for a node, to quickly check if a creature can even move
neighbours = {}
for p0 in range(23):
    myneighbours = []
    for n in [b for (a,b,c) in allmoves if a==p0]:
        myneighbours.append(n)
    neighbours[p0] = myneighbours



visited = set()

class Board:

    def char2piece(c):
        if c in ['A','B','C','D']:
            return c
        return None

    def __str2pos__(text):
        lines = [line.strip() for line in text.strip().split()]

        pos = [None] * 23
        pos[0]  = lines[1][1]
        pos[1]  = lines[1][2]
        pos[2]  = lines[1][4]
        pos[3]  = lines[1][6]
        pos[4]  = lines[1][8]
        pos[5]  = lines[1][10]
        pos[6]  = lines[1][11]

        #Rum A
        pos[7]  = lines[2][3]
        pos[8]  = lines[3][1]
        pos[9]  = lines[4][1]
        pos[10] = lines[5][1]

        #Rum B
        pos[11]  = lines[2][5]
        pos[12]  = lines[3][3]
        pos[13]  = lines[4][3]
        pos[14]  = lines[5][3]

        #Rum C
        pos[15]  = lines[2][7]
        pos[16]  = lines[3][5]
        pos[17]  = lines[4][5]
        pos[18]  = lines[5][5]

        #Rum C
        pos[19]  = lines[2][9]
        pos[20]  = lines[3][7]
        pos[21]  = lines[4][7]
        pos[22]  = lines[5][7]

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
###{0[7]}#{0[11]}#{0[15]}#{0[19]}###
  #{0[8]}#{0[12]}#{0[16]}#{0[20]}#
  #{0[9]}#{0[13]}#{0[17]}#{0[21]}#
  #{0[10]}#{0[14]}#{0[18]}#{0[22]}#
  #########""".format(tuple(['.' if c is None else c for c in self.pos]))

    def makemoves(self, lastmoved):
        global allmoves, fullmoves
        #Find all moves where "from" is occupied and "to" is empty
        #moves = [move for move in allmoves if self.pos[move[0]] is not None and self.pos[move[1]] is None]

        #First just check if any neighbouring cell is available
        for p0 in fullmoves.keys():

            #Never move same thing twice
            if p0 == lastmoved: continue

            if self.pos[p0] == '.': continue #"From" is empty


            closest = neighbours[p0]
            canmove = False
            for n in closest:
                if self.pos[n] == '.':
                    canmove = True
                    break
            if not canmove:
                continue

            mymoves = fullmoves[p0]
            for p1 in mymoves.keys():
                (cost, passing) = mymoves[p1] 

                if self.pos[p1] != '.': continue #"To" is occupied

                #Check to see if path is blocked
                for p in passing:
                    if self.pos[p] != '.': continue

                #Don't move inside of a room (only go "all the way in" or "all the way out")
                if p0 > 6 and p1 > 6: continue

                creature = self.pos[p0]

                #Don't go into a forbidden room:
                if p1 in banlist[creature]:
                    continue

                #Check to see if it is ok to move out of a home position (only if there are other
                #creatures below it
                if p0 in homes[creature]:
                    valid = False
                    homepos = homes[creature].index(p0)
                    rest =  homes[creature][homepos:]
                    for hp in rest:
                        if self.pos[hp] != creature:
                            valid = True
                            break
                    if not valid:
                        continue

                #Check to see if it is ok to move into home position (don't leave empty spaces below)
                if p1 in homes[creature]:
                    homepos = homes[creature].index(p1)
                    rest =  homes[creature][homepos:]
                    for hp in rest:
                        if self.pos[hp] == '.':
                            continue

                                

                #Only move between spaces in "corridor" if something else can move into the
                #spot getting vacated
                #if p0<=6 and p1<=6:
                #    m = [t1 for (t0,t1,_) in allmoves if t0==p0 and t1!=p1 and self.pos[t1]=='.']
                #    if len(m)==0:
                #        continue

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

                yield (cost, p1, newboard)


#print(allmoves)
q = queue.PriorityQueue()

#startpos = Board(simple_start)
startpos = Board(start)
endpos = Board(finish)
distances = {}


q.put((0, -1, startpos))

cycles = 0

while not q.empty():
    cycles+=1

    (cost, lastmoved, pos) = q.get()

    if cycles%100000==0 or cycles < 10:
        print(cycles, cost, q.qsize())
        print(pos)
        print()
        #random.shuffle(allmoves)

    if cycles%1000000==0:
        continue
        oldsize = q.qsize()
        if oldsize > 1000000:
            nq = queue.PriorityQueue()
            while not q.empty():
                (cc, ll, pp) = q.get()
                if not pp in visited:
                    nq.put((cc,ll,pp))

            q = nq

            print("Compacted queue from",oldsize,"to",q.qsize())


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

    for (nextcost, moved, nextpos) in pos.makemoves(lastmoved):
        if nextpos not in visited:
            q.put((cost + nextcost, moved, nextpos))