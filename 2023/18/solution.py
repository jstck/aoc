#!/usr/bin/env python3

import sys

def move(x,y,dir,dist) -> tuple[int,int]:
    match dir:
        case "R" | "0":
            return (x+dist, y)
        case "D" | "1":
            return (x, y+dist)
        case "L" | "2":
            return (x-dist, y)
        case "U" | "3":
            return (x, y-dist)
        case _:
            assert False

def dig(input: list[str]):

    x1,y1=0,0
    x2,y2=0,0

    l1=l2=0
    a1=a2=b1=b2=0

    px1=py1=px2=py2=0

    for i, row in enumerate(input):

        (dir1, dist1, color) = row.strip().split()
        dist1 = int(dist1)

        dist2 = int(color[2:-2], 16)
        dir2 = color[-2]

        l1 += dist1
        l2 += dist2

        x1,y1 = move(x1,y1,dir1,dist1)
        x2,y2 = move(x2,y2,dir2,dist2)

        if i>0:
            a1 += y1*px1
            b1 += x1*py1
            a2 += y2*px2
            b2 += x2*py2
            
        px1,py1=x1,y1
        px2,py2=x2,y2

    #Circumference//2+1 is added to area to account for the width of the border

    print("Part 1:", abs(a1-b1)//2 +l1//2+1 )
    print("Part 2:", abs(a2-b2)//2 +l2//2+1 )

if __name__ == "__main__":
    dig(sys.stdin.readlines())
