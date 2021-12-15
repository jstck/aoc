#!/usr/bin/env python3

import sys
import argparse
import re
import collections, queue

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

tiles = 1
if part2:
    tiles = 5

grid = []

for line in sys.stdin.readlines():
    row = [int(x) for x in line.strip()]
    grid.append(row*tiles) ##Repeat rows with tiling

#Multiply rows
if tiles > 1:
    orig_size = len(grid)
    for r in range(1,tiles):
        for i in range(0,orig_size):
            grid.append(grid[i])


xmax = len(grid[0])
ymax = len(grid)

print("Grid size:", xmax, ymax)

cost = [[-1]*(xmax) for y in range(ymax)] #-1 = infinite
visited = set()

#print(grid)
q = queue.PriorityQueue()

cost[0][0]=0

#Neighbours as tuples of (x, y, cost)
q.put((0, (0, 0)))

#print(cost)
while not q.empty():
    #nq.sort(key=lambda x:x[2]) #Sort by cost
    (c, t) = q.get()
    (x,y) = t

    if x==xmax-1 and y == ymax-1:
        print("Cost to end: ", c)
        sys.exit(0)


    #print(x,y,c, len(nq))
    if not (x,y) in visited:
        ##print("New cell:", x, y)
        visited.add((x,y))
    
    #visited.add((x,y))
    for (dx,dy) in [(-1,0),(1,0),(0,-1),(0,1)]:
        x2,y2 = x+dx,y+dy

        #Outside grid
        if x2<0 or x2>=xmax:
            continue
        if y2<0 or y2>=ymax:
            continue

        #Already been here
        if (x2,y2) in visited:
            continue
            pass

        ncost = c + grid[y2][x2]
        if cost[y2][x2] < 0 or ncost < cost[y2][x2]:
            cost[y2][x2] = ncost
            #print("New best cost for",x2,y2,ncost)
            q.put((ncost,(x2,y2)))

#for line in cost:
#    print(line)
print(cost[ymax][xmax])