#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from queue import PriorityQueue
from collections import defaultdict
import heapq


mazelines = sys.stdin.readlines()

sample_start = """
############# . 0
#...........# . 1
###B#C#B#D### . 2
  #D#C#B#A# .   3
  #D#B#A#C# .   4
  #A#D#C#A# .   5
  #########
   3 5 7 9
"""


maze = [0] * 23

solution = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]
solution_t = tuple(solution)

#Corridor
idx_corridor = [1, 2, 4, 6, 8, 10, 11]
for pos in range(7):
    idx = idx_corridor[pos]
    ampC = mazelines[1][idx]
    ampI = ".ABCD".index(ampC)
    maze[pos] = ampI

#Rooms
for row in range(0,4):
    textrow = mazelines[row + 2]
    for room in range(0,4):
        textcol = 3+2*room

        pos = 7+room*4+row

        ampC = textrow[textcol]
        ampI = ".ABCD".index(ampC)
        maze[pos] = ampI

print(maze)


def printMaze(maze):
    templ = [
"#############",
"#%%.%.%.%.%%#",
"###%#%#%#%###",
"  #%#%#%#%#  ",
"  #%#%#%#%#  ",
"  #%#%#%#%#  ",
"  #########  "
    ]
    result = []
    cells = [".ABCD"[x] for x in maze]
    for i in range(len(templ)):
        s = templ[i].replace("%","{}")

        if i==1:
            s = s.format(*cells[0:7])
        elif i==2:
            s = s.format(cells[7], cells[11], cells[15], cells[19])
        elif i==3:
            s = s.format(cells[8], cells[12], cells[16], cells[20])
        elif i==4:
            s = s.format(cells[9], cells[13], cells[17], cells[21])
        elif i==5:
            s = s.format(cells[10], cells[14], cells[18], cells[22])

        result.append(s)

    return "\n".join(result)

#print(printMaze(maze))
#print(printMaze(solution))

#spelplanen har 23 olika giltiga positioner (0-23):

#############
#01.2.3.4.56#
###7#b#f#j###
  #8#c#g#k#
  #9#d#h#l#
  #a#e#j#m#
  #########

#Rum A = 7-10
#Rum B = 11-14
#Rum C = 15-18
#Rum D = 19-22

def inRoom(pos, amp):
    if amp==1:
        return pos in [7, 8, 9, 10]
    if amp==2:
        return pos in [11, 12, 13, 14]
    if amp==3:
        return pos in [15, 16, 17, 18]
    if amp==4:
        return pos in [19, 20, 21, 22]
    return False

def roomAmp(pos):
    if 0 <= pos <= 6: return 0
    if 7 <= pos <= 10: return 1
    if 11 <= pos <= 14: return 2
    if 15 <= pos <= 18: return 3
    if 19 <= pos <= 22: return 4
    print("INVALID POSITION", pos)
    assert(False)

#Positions below a position in a room
roomsBelow = {
    7: [8, 9, 10],
    8: [9, 10],
    9: [10],

    11: [12, 13, 14],
    12: [13, 14],
    13: [14],
    
    15: [16, 17, 18],
    16: [17, 18],
    17: [18],
    
    19: [20, 21, 22],
    20: [21, 22],
    21: [22],
}
    
#roomsBelow = defaultdict(list, roomsBelow)


#Vettiga drag för varje cell till varje korridorscell, kostnad, och vilka celler man måste passera (dest, cost, pass)
moves = {
#Rum A:
    7: [
        (0, 3, (1,)),
        (1, 2, ()),
        (2, 2, ()),
        (3, 4, (2,)),
        (4, 6, (2, 3)),
        (5, 8, (2, 3, 4)),
        (6, 9, (2, 3, 4, 5)),
    ],
#Rum B:
    11: [
        (0, 5, (1, 2)),
        (1, 4, (2,)),
        (2, 2, ()),
        (3, 2, ()),
        (4, 4, (3,)),
        (5, 6, (3, 4)),
        (6, 7, (3, 4, 5)),
    ],
#Rum C:
    15: [
        (0, 7, (1, 2, 3)),
        (1, 6, (2, 3)),
        (2, 4, (3,)),
        (3, 2, ()),
        (4, 2, ()),
        (5, 4, (4,)),
        (6, 5, (4, 5)),
    ],
#Rum D:
    19: [
        (0, 9, (1, 2, 3, 4)),
        (1, 8, (2, 3, 4)),
        (2, 6, (3, 4)),
        (3, 4, (4,)),
        (4, 2, ()),
        (5, 2, ()),
        (6, 3, (5,)),
    ],
}

#Add moves for all "subrooms" to corridor
for room in [8, 12, 16, 20]:
    for subroom in [0, 1, 2]:
        here = room+subroom
        r = moves[here-1]
        moves[here] = []
        for (dest, cost, through) in r:
            newcost = cost+1
            newthrough = through + (here-1,)
            moves[here].append((dest, newcost, newthrough))

#Add all reverse moves
reverse = {}
for (room, routes) in moves.items():
    for (dest, cost, through) in routes:
        if not dest in reverse:
            reverse[dest] = []

        reverse[dest].append((room, cost, through))

moves |= reverse

import pprint
pp = pprint.PrettyPrinter(indent=2)

def generatemoves(state):
    costs = [0, 1, 10, 100, 1000]
    occupied = [x for x in range(23) if state[x]!=0]
    occupied_s = set(occupied)
    #available = [x for x in range(23) if state[x]==0]

    for src in occupied:
        me = state[src]
        #meC = ".ABCD"[me]
        mycost = costs[me]
        for (dest, cost, through) in moves[src]:
            #print(f"Considering move from {src}:{meC} to {dest}")
            #Destination is occupied
            if state[dest] != 0:
                #print("Destination occupied")
                continue

            valid = True
            #Any position the move passes through is occupied
            for p in through:
                if p in occupied_s:
                    valid = False
                    break
            if not valid:
                #print("Path blocked")
                continue

            #Check that it's not going into someone elses room
            resident = roomAmp(dest)
            if resident != 0 and resident != me:
                #print("Not my room")
                continue

            #Check that if going into a room, all cells below contain the proper resident
            if dest in roomsBelow:
                for r in roomsBelow[dest]:
                    if state[r] != resident:
                        valid = False
                        break
            if not valid:
                #print("Other stuff below in my room")
                continue

            #Do not move out of a room if it's only residents below
            if src in roomsBelow and resident == me:
                valid = False
                for r in roomsBelow[src]:
                    if state[r] != me:
                        #print(f"{r} has {state[r]} in it, cool to move.")
                        valid = True
                        break
            if not valid:
                #print("Not moving out of proper room")
                continue

            #It seems to be a valid move
            newstate = list(state)
            newstate[src] = 0
            newstate[dest] = me

            newcost = cost * mycost

            yield (newcost, tuple(newstate))



#pq = PriorityQueue()
hq = []

#Enqueue starting position
#pq.put((0, maze))
heapq.heappush(hq, (0, tuple(maze)))

#Upper limit for solution (or any paths)
solution_score = 100000


solution_found = False
visited = set()

print("==== START ====")
print(printMaze(maze))


#sys.exit(0)
count = 0
already_seen = 0

debug = 1000000000

while len(hq): #not pq.empty():
    #(cost, state) = pq.get()
    (cost, state) = heapq.heappop(hq)
    count += 1

    lastcost = cost

    if count % debug == 0:
        print("Processed", count)
        print("Cost", cost)
        #print("Queue length", pq.qsize())
        print("Queue length", len(hq))
        print("Visited:", len(visited))
        print("Duplicate moves:", already_seen)
        print(printMaze(state))


    if state == solution_t:
        solution_found = True
        solution_score = min (solution_score, cost)
        print("Solution found, cost", cost)
        print(count, "states processed")
        break

    if state in visited:
        continue

    #Skip paths past upper limit or best score
    if cost >= solution_score:
        continue

    #tstate = tuple(state)
    #visited.add(tstate)
    visited.add(state)

    statecount = 0
    for (movecost, newstate) in generatemoves(state):
        if not newstate in visited:
            statecount += 1
            newcost = cost+movecost
            #pq.put((cost+movecost, newstate))
            heapq.heappush(hq, (newcost, newstate))
        else:
            already_seen += 1
    if count % debug == 0:
        print(f"Generated {statecount} new moves")
        print()

    if statecount == 0:
        #print("Dead end found at cost ", cost)
        #print(printMaze(state))
        pass

if solution_found:
    print("Best solution:", solution_score)
else:
    print("No solution found below", solution_score)
    print("Cost of last move:", lastcost)
print("Processed:", count)
print("Visited:", len(visited))
print("Duplicate moves:", already_seen)