#!/usr/bin/env python3

import sys

moves = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0),
}

def doMove2(rope, move):
    headX = rope[0][0] + move[0]
    headY = rope[0][1] + move[1]

    rope[0] = (headX, headY)

    for i in range(1, len(rope)):
        (headX, headY) = rope[i-1]
        (tailX, tailY) = rope[i]

        dX = headX-tailX
        dY = headY-tailY

        if abs(dX) <= 1 and abs(dY) <= -1:
            pass
        else:

            #Diagonal moves, puts tail diagonally after head
            if tailX < headX-1 and tailY < headY-1:
                tailX = headX-1
                tailY = headY-1
            elif tailX > headX+1 and tailY < headY-1:
                tailX = headX+1
                tailY = headY-1
            elif tailX < headX-1 and tailY > headY+1:
                tailX = headX-1
                tailY = headY+1
            elif tailX > headX+1 and tailY > headY+1:
                tailX = headX+1
                tailY = headY+1

            #Other moves puts tail "straight" behind head
            elif tailX < headX-1:
                tailX = headX-1
                tailY = headY

            elif tailX > headX+1:
                tailX = headX+1
                tailY = headY
            
            elif tailY < headY-1:
                tailY = headY-1
                tailX = headX

            elif tailY > headY+1:
                tailY = headY+1
                tailX = headX

            rope[i] = (tailX, tailY)


def printGrid(visited, rope=[], showTrail = True, showRope = True):
    pX = [p[0] for p in visited] + [p[0] for p in rope]
    pY = [p[1] for p in visited] + [p[1] for p in rope]

    minX = min(pX + [0])
    maxX = max(pX)
    minY = min(pY + [0])
    maxY = max(pY)

    print(minX, maxX, minY, maxY)

    grid = []
    for y in range(minY, maxY+1):
        grid.append(["."] * (maxX-minX+1))

    if showTrail:
        for (x,y) in visited:
            grid[y-minY][x-minX] = "#"

    if showRope:
        for i in range(len(rope)):
            (x, y) = rope[i]
            if grid[y-minY][x-minX] in ["#","."]:
                grid[y-minY][x-minX] = str(i)

    for y in range(len(grid)-1, -1, -1):
        print("".join(grid[y]))
    print()


XMIN, XMAX = (-389, 1)
YMIN, YMAX = (-99, 172)


from PIL import Image

TAIL_COLOR = (0, 255, 0)
ROPE_COLOR = (255, 0, 255)
ROPE_VISITED_COLOR = (120,120,80)
HEAD_COLOR = (255, 255, 255)
HEAD_VISITED_COLOR = (200, 0, 0)

def drawFrame(tail, rope, rope_visited, head_visited):
    frame = Image.new("RGB", (XMAX-XMIN+1, YMAX-YMIN+1), (0, 0, 0))
    pixels = frame.load()
    for (x, y) in rope_visited:
        pixels[x-XMIN, y-YMIN] = ROPE_VISITED_COLOR
    for (x, y) in head_visited:
        pixels[x-XMIN, y-YMIN] = HEAD_VISITED_COLOR
    for (x, y) in tail:
        pixels[x-XMIN, y-YMIN] = TAIL_COLOR
    
    for (x, y) in rope:
        pixels[x-XMIN, y-YMIN] = ROPE_COLOR
    head = rope[0]
    pixels[head[0]-XMIN, head[1]-YMIN] = HEAD_COLOR

    return frame
    


def moveRope(input, length):

    
    frames = []
    count = 0

    rope = [[0, 0]] * length
    visited = set([(0,0)])
    rope_visited = set([(0,0)])
    head_visited = set([(0,0)])

    #frames.append(drawFrame(visited, rope, rope_visited, head_visited))

    for line in input:
        parts = [x.strip() for x in line.split()]
        dir = parts[0]
        dist = int(parts[1])

        for i in range(dist):
            doMove2(rope, moves[dir])

            tail = rope[-1]
            visited.add(tail)

            rope_visited.update(rope)
            head_visited.add(rope[0])

            count += 1
            if count%100 == 0: print("Drawing frame", count)

            frame = drawFrame(visited, rope, rope_visited, head_visited)
            frames.append(frame)
            
            

        frame.save(f"frames/{count:05}.gif", format="GIF")
            
    #lastframe = drawFrame(visited, rope, rope_visited, head_visited)
    lastframe = frames[-1]
            
    #printGrid(visited, rope)
    print("Saving image")
    frames[0].save("animate.gif", format="GIF", append_images=frames, save_all=True, duration=1, loop=0)

    lastframe.save("lastframe.gif", format="GIF")
    
    return len(visited)

def part2(input):
    return moveRope(input, 10)


with open("input.txt", "r") as fp:
    part2(fp.readlines())