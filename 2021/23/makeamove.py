#!/usr/bin/env python3

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

neighbours = {}

for p0 in range(23):
    myneighbours = []
    for n in [b for (a,b,c) in allmoves if a==p0]:
        myneighbours.append(n)
    neighbours[p0] = myneighbours
print(neighbours)