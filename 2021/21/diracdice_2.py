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

#Number of paths for each possible result for 3d3
splits = [
    (3, 1),
    (4, 3),
    (5, 6),
    (6, 7),
    (7, 6),
    (8, 3),
    (9, 1)
]

#Starting positions
#startpos = [4,8]
startpos = [2,5]


#number of paths to reach each possible state, keyed by (s0,s1,p0,p1, t) containing the two scores, positions and whose turn it is
universes = {
    (0,0,startpos[0],startpos[1],0): 1
}

wins = [0,0]


#Queue generated states ordered by the score of the player up next
q = queue.PriorityQueue()
q.put((0,(0,0,startpos[0],startpos[1],0)))

while not q.empty():
    (_,state) = q.get()
    vprint(1, state)
    (s0,s1,p0,p1,t) = state

    score = state[t]
    pos = state[t+2]

    #Grab the number of paths leading here, and remove it because not needed anymore
    n = universes[state]
    del universes[state]

    for (roll,num) in splits:
        newpos = (pos+roll-1)%10+1
        newscore = score + newpos
        n_next = n*num
        if newscore >= 21:
            #WIN
            vprint(1, n_next,"wins for player",t)
            wins[t] += n_next
        else:
            if t==0:
                newstate = (newscore, s1, newpos, p1, 1)
                s_next = s1
            else:
                newstate = (s0, newscore, p0, newpos, 0)
                s_next = s0

            #Update count for next state, or add a new one
            if newstate in universes.keys():
                vprint(1, "Increasing state", newstate)
                universes[newstate] += n_next
            else:
                universes[newstate] = n_next
                q.put((n_next, newstate))
                vprint(1, "Queuing new state", newstate)


vprint(1, "Win tally:",wins)
print("RESULT:",max(wins))